import qrcode
import io
import base64
from flask import url_for
from app import db
from app.models import QRLink
from flask_login import current_user

def generate_qr_code(link):
    """Generate a QR code for a given link and return it as a base64-encoded string."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Convert the image to a base64 string
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return 'data:image/png;base64,' + base64.b64encode(buffered.getvalue()).decode('utf-8')

def generate_qr_code_with_tracking(link):
    """Generate a QR code with a tracking URL and return it as a base64-encoded string."""
    formatted_link = ensure_absolute_url(link)
    qr_link = QRLink.query.filter_by(link=formatted_link).first()
    if qr_link:
        tracking_url = url_for('main.track_qr_link', qr_link_id=qr_link.id, _external=True)
        print(f"Tracking URL: {tracking_url}")  # Debug print
        return generate_qr_code(tracking_url)
    print("QR Link not found.")  # Debug print
    return None


from urllib.parse import urlparse, urlunparse

def ensure_absolute_url(url):
    """Ensure the URL includes the scheme and domain, defaulting to https://."""
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        # Default to 'https://' if scheme is missing
        url = f"https://{url}"
    elif parsed_url.scheme not in ['http', 'https']:
        # Optionally handle other schemes if necessary
        url = urlunparse(parsed_url._replace(scheme='https'))
    return url

def check_qr_code_limit(user_id):
    """Check if the user has reached the limit of 10 QR codes."""
    qr_count = QRLink.query.filter_by(user_id=user_id).count()
    return qr_count < 10

def save_qr_link(link, tracking):
    """Save the QR link to the database."""
    user_id = current_user.id if current_user.is_authenticated else None
    # check if user has already generated 10 links
    if user_id and not check_qr_code_limit(user_id):
        raise ValueError("QR code limit of 10 reached. Cannot add more.")
    # 
    tracking_value = tracking if user_id is not None else None
    formatted_link = ensure_absolute_url(link)
    
    qr_link = QRLink(
        link=formatted_link,
        user_id=user_id,
        tracking=tracking_value
    )
    db.session.add(qr_link)
    db.session.commit()



# def save_qr_link(link, tracking="yes"):
#     """Save the QR link to the database."""
#     user_id = current_user.id if current_user.is_authenticated else None
#     # Set tracking to None if user_id is None
#     tracking_value = tracking if user_id is not None else None
    
#     qr_link = QRLink(
#         link=link,
#         user_id=user_id,
#         tracking=tracking_value
#     )
#     db.session.add(qr_link)
#     db.session.commit()
