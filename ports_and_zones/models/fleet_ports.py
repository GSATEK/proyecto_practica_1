from odoo import models, fields, api
from datetime import datetime


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
        required=True,
    )

    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehículo", required=True)

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
