from odoo import models, fields


class FleetPortHistory(models.Model):
    _name = "fleet.ports.history"
    _description = "Historial de Asignaciones de Puertos y Vehículos"
    _order = "time_in desc"

    port_id = fields.Many2one(
        "fleet.ports", string="Puerto", ondelete="cascade", required=True
    )
    vehicle_id = fields.Many2one(
        "fleet.vehicle", string="Vehículo Asignado", required=True
    )
    time_in = fields.Datetime(
        string="Tiempo de Asignación", default=fields.Datetime.now, readonly=True
    )
    time_out = fields.Datetime(string="Tiempo de Desasignación", readonly=True)

    # Campo calculado para mostrar el tiempo total de permanencia (opcional)
    # duration = fields.Float(compute='_compute_duration', store=True, string='Duración (horas)')
