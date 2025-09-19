from odoo import api, fields, models, _

class wizardAddService(models.TransientModel):
    _name = "wizard.add.service"
    _description = "Wizard para agregar servicios a un cliente"

    exemple_field = fields.Char(string="Campo de Ejemplo", help="Este es un campo de ejemplo para el wizard.")
    employee_id = fields.Many2one('hr.employee', string="Empleado", help="Seleccione el empleado asociado al servicio.")

    def action_add_service(self):
        report = self.env['hr.services.report']
        value = {
            'name': self.exemple_field,
            'employee_id': self.employee_id.id,
        }
        report.create(value)