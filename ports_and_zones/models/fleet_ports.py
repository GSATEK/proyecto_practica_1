from odoo import models, fields, api
from datetime import datetime
import qrcode
import base64
from io import BytesIO


class FleetPorts(models.Model):
    _name = "fleet.ports"
    _description = "Gestión de puertos para los vehículos"

    port_id = fields.Char(
        string="Puerto ID",
        # default=lambda self: self.env["ir.sequence"].next_by_code("increment_port_id"),
    )
    port_name = fields.Char(string="Nombre Puerto", required=True)
    port_zone = fields.Selection(
        [("sud", "Sud"), ("norte", "Norte"), ("este", "Este"), ("oeste", "Oeste")],
        string="Zona Puerto",
        required=True,
    )
    port_status = fields.Selection(
        [("ocupado", "Ocupado"), ("libre", "Libre")],
        string="Estado Puerto",
        default="libre",
        required=True,
    )

    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehículo", required=True)

    qr_code = fields.Binary(
        "QR Code", compute="_compute_qr_code", store=False, readonly=True
    )

    history_ids = fields.One2many(
        "fleet.ports.history", "port_id", string="Historial de Asignaciones"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("port_id", "/") == "/":
                vals["port_id"] = (
                    self.env["ir.sequence"].next_by_code("increment_port_id") or "Nuevo"
                )

        records = super(FleetPorts, self).create(vals_list)

        for record in records:
            if record.vehicle_id:
                self.env["fleet.ports.history"].create(
                    {
                        "port_id": record.id,
                        "vehicle_id": record.vehicle_id.id,
                    }
                )

        return records

    def write(self, vals):
        if "vehicle_id" in vals:
            current_time = datetime.now()
            new_vehicle_id = vals.get("vehicle_id")

            for port in self:
                old_vehicle = port.vehicle_id

                if old_vehicle:
                    last_history = self.env["fleet.ports.history"].search(
                        [
                            ("port_id", "=", port.id),
                            ("vehicle_id", "=", old_vehicle.id),
                            ("time_out", "=", False),
                        ],
                        limit=1,
                        order="time_in desc",
                    )

                    if last_history:
                        last_history.write({"time_out": current_time})

                if new_vehicle_id:
                    self.env["fleet.ports.history"].create(
                        {
                            "port_id": port.id,
                            "vehicle_id": new_vehicle_id,
                        }
                    )

        return super(FleetPorts, self).write(vals)

    @api.depends("port_id")
    def _compute_qr_code(self):
        for record in self:
            if not record.port_id:
                record.qr_code = False

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(record.port_id)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = BytesIO()
            img.save(buffer, "PNG")
            record.qr_code = base64.b64encode(buffer.getvalue())
