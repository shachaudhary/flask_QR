from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.utils import generate_qr_code, save_qr_link, generate_qr_code_with_tracking
from app import db
from app.models import User, QRLink, QRLinkVisit
from app.forms import RegistrationForm, QRCodeForm
from app.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from urllib.parse import urlparse, urlunparse


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = QRCodeForm()
    qr_code_url = None
    if request.method == 'POST':
        link = request.form.get('link')
        if link:
            qr_code_url = generate_qr_code(link)
            save_qr_link(link, qr_code_url)

    return render_template('index.html', form=form, qr_code_url=qr_code_url)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        
        # Create a new user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        # Flash a success message
        flash('Your account has been created!', 'success')
        
        return redirect(url_for('main.index'))
    
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Check your email and/or password.', 'danger')
    
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = QRCodeForm()
    qr_code_image = None
    qr_links = QRLink.query.filter_by(user_id=current_user.id).order_by(QRLink.created_at.desc()).limit(10).all()
    
    if request.method == 'POST':
        link = request.form.get('link')
       
        # save_qr_link(link, tracking='yes')  # Save link with tracking
        try:
            save_qr_link(link, tracking='yes')  # Save link with tracking
            qr_code_image = generate_qr_code_with_tracking(link)  # Generate QR code with tracking URL
            flash('QR code generated and link saved!', 'success')
        except ValueError as e:
            flash(str(e), 'danger')
      
        qr_links = QRLink.query.filter_by(user_id=current_user.id).order_by(QRLink.created_at.desc()).limit(10).all()

    return render_template('dashboard.html', form=form, qr_code_image=qr_code_image, qr_links=qr_links)


def ensure_absolute_url(url):
    parsed_url = urlparse(url)
    # Check if the URL is missing scheme and netloc
    if not parsed_url.scheme or not parsed_url.netloc:
        return urlunparse(('http', 'example.com', url, '', '', ''))
    return url

@main.route('/track/<int:qr_link_id>')
def track_qr_link(qr_link_id):
    qr_link = QRLink.query.get_or_404(qr_link_id)
    
    # Log the visit
    visit = QRLinkVisit(qr_link_id=qr_link.id, ip_address=request.remote_addr)
    db.session.add(visit)
    db.session.commit()
    
    # Ensure the URL is absolute
    redirect_url = ensure_absolute_url(qr_link.link)

    # Debug output
    print(f"Redirecting to: {redirect_url}")

    return redirect(redirect_url)


@main.route('/delete_qr_link/<int:qr_link_id>', methods=['POST'])
@login_required
def delete_qr_link(qr_link_id):
    qr_link = QRLink.query.get_or_404(qr_link_id)

    # Ensure the user is the owner of the QR code
    if qr_link.user_id != current_user.id:
        flash('You are not authorized to delete this QR code.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Delete related visits first
    QRLinkVisit.query.filter_by(qr_link_id=qr_link_id).delete()

    # Delete the QR code
    db.session.delete(qr_link)
    db.session.commit()
    flash('QR code deleted successfully.', 'success')

    return redirect(url_for('main.dashboard'))






