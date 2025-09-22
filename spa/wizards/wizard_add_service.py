from odoo import api, fields, models, _

class WizardAddEmployeeService(models.TransientModel):
    _name = "wizard.add.employee.service"
    _description = "Wizard para agregar servicios a un cliente"

    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)

    def action_add_service(self):
        self.ensure_one()
        report_vals = {
            'name': _('Service Report - %s') % (self.partner_id.display_name or ''),
            'employee_id': self.employee_id.id,
            'partner_id': self.partner_id.id,
        }
        self.env['hr.employee.services.report'].create(report_vals)
        return {'type': 'ir.actions.act_window_close'}