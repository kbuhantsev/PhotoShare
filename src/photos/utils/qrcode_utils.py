import qrcode
from src.services.cloudinary_utils import upload_file
from qrcode.image.pure import PyPNGImage


def create_qr_code(url: str) -> dict | None:

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white", image_factory=PyPNGImage)

    asset = upload_file(file=img, folder="qrcodes")

    if asset:
        return asset
    else:
        return None
