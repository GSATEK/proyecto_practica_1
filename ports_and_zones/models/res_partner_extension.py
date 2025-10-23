from odoo import fields, models
import qrcode
import base64
from io import BytesIO


class ResParteExtension(models.Model):
    _inherit = "res.partner"

    qr_code = fields.Binary(
        "QR code", compute="_compute_qr_code", store=False, readonly=True
    )

    def _compute_qr_code(self):
        for record in self:
            qr = qrcode.QRCode(
                version=1, error_correction=qrcode.ERROR_CORRECT_L, box_size=3, border=4
            )
            qr.add_data(str(record.id))
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            record.qr_code = qr_image
