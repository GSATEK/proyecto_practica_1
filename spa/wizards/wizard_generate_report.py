from odoo import api, fields, models, _

class WizardGenerateReport(models.TransientModel):
    _name = "wizard.generate.employee.report"
    _description = "Wizard para generar reportes de servicios por empleado"

    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    date_from = fields.Date(string="Fecha Desde", required=True)
    date_to = fields.Date(string="Fecha Hasta", required=True)

    def action_generate_report(self):
        self.ensure_one()
        domain = [
            ('employee_id', '=', self.employee_id.id),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
        ]
        records = self.env['hr.employee.services.record'].search(domain)
        return {
            'name': _('Service Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee.services.record',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': {'default_employee_id': self.employee_id.id},
            'target': 'current',
        }