from odoo import models, fields


class FleetPortLog(models.Model):
    _name = 'fleet.port.log'
    _description = 'Log de cambios de plazas'

    port_id = fields.Many2one('fleet.port', string='Plaza', required=True)
    timestamp = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    is_occupied = fields.Boolean(string='Ocupada')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo')
