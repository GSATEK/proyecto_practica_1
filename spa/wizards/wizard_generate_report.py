from odoo import api, fields, models, _

class WizardGenerateReport(models.TransientModel):
    _name = "wizard.generate.employee.report"
    _description = "Wizard para generar reportes de servicios por empleado"

    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    date_from = fields.Date(string="Fecha Desde", required=True)
    date_to = fields.Date(string="Fecha Hasta", required=True)
    
    hr_service_record_ids = fields.Many2many(
        comodel_name="hr.employee.services.record",
        string="Registros de Servicio",
        compute="_compute_hr_service_record_ids",
        help="Registros de servicio relacionados con el empleado y el rango de fechas.",
    )

    def action_print_report(self):
        return self.env.ref('spa.action_report_services').report_action(self)
    
    def _compute_hr_service_record_ids(self):
        for record in self:
            record.hr_service_record_ids = self.env['hr.employee.services.record'].search([
                ('employee_id', '=', record.employee_id.id),
                ('date', '>=', record.date_from), 
                ('date', '<=', record.date_to)
            ])