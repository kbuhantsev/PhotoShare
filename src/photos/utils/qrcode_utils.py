import qrcode
from src.services.cloudinary_utils import upload_file
from qrcode.image.svg import SvgPathImage
import io


def create_qr_code(url: str) -> dict | None:

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img: SvgPathImage = qr.make_image(fill_color="black", back_color="white", image_factory=SvgPathImage)

    img_io = io.BytesIO()
    img.save(img_io)
    img_io.seek(0)

    asset = upload_file(file=img_io, folder="qrcodes")

    if asset:
        return asset
    else:
        return None
