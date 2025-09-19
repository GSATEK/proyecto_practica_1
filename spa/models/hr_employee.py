from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    def open_service_wizard(self):
        """Open the service addition wizard for the selected employee."""
        return {
            'name': 'Add Service',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.add.service',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_id': self.id,
            },
        }