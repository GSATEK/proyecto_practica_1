from odoo import models, fields, api


class FleetPort(models.Model):
    _name = 'fleet.port'
    _description = 'Plaza de carga'

    name = fields.Char(string='Nombre', required=True)
    sequence = fields.Integer(string='Secuencia')
    qr_code = fields.Char(string='QR Code')
    is_occupied = fields.Boolean(string='Ocupada', default=False)
    current_vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo')
    last_updated = fields.Datetime(string='Última actualización')

    @api.model
    def update_from_qr(self, qr_code, vehicle_vals=None):
        """Actualizar estado de plaza a partir de QR. vehicle_vals es diccionario con info del vehículo."""
        port = self.search([('qr_code', '=', qr_code)], limit=1)
        if not port:
            port = self.create({'name': qr_code, 'qr_code': qr_code})
        if vehicle_vals:
            # asociar vehículo si se pasa
            vehicle = None
            if vehicle_vals.get('license_plate'):
                vehicle = self.env['fleet.vehicle'].search([('license_plate', '=', vehicle_vals['license_plate'])], limit=1)
                if not vehicle:
                    vehicle = self.env['fleet.vehicle'].create({
                        'name': vehicle_vals.get('name', vehicle_vals.get('license_plate')),
                        'license_plate': vehicle_vals.get('license_plate')
                    })
            if vehicle:
                port.current_vehicle_id = vehicle.id
                port.is_occupied = True
        else:
            # marcar libre
            port.current_vehicle_id = False
            port.is_occupied = False
        port.last_updated = fields.Datetime.now()
        # registrar log
        self.env['fleet.port.log'].create({
            'port_id': port.id,
            'is_occupied': port.is_occupied,
            'vehicle_id': port.current_vehicle_id.id if port.current_vehicle_id else False,
        })
        return port
