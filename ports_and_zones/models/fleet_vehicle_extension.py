from odoo import models, fields
import qrcode
import base64
from io import BytesIO


class FleetVehicleExtension(models.Model):
    _inherit = "fleet.vehicle"

    qr_code = fields.Binary(
        "QR Code", compute="_compute_qr_code", store=False, readonly=True
    )

    driver_qr_code = fields.Binary(
        "QR Code del Conductor",
        related="driver_id.qr_code",
        readonly=True,
        store=False,
    )

    def _compute_qr_code(self):
        for record in self:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_L,
                box_size=3,
                border=4,
            )
            qr.add_data(str(record.id))
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, "PNG")
            qr_image = base64.b64encode(temp.getvalue())

            record.qr_code = qr_image


# https://www.cybrosys.com/blog/how-to-generate-a-qr-code-in-odoo-17-erp
