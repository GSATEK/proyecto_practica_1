from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    def open_service_wizard(self):
        """Open the service addition wizard for the selected employee."""
        return {
            'name': 'Añadir Servicio',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.add.employee.service',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_id': self.id,
            },
        }
    def get_line_ids(self):
        self.ensure_one()
        line_obj = self.env['hr.service.records']
        return line_obj.search([('employee_id', '=', self.id)])