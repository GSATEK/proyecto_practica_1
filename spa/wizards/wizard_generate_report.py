from odoo import api, fields, models, _

class WizardGenerateReport(models.TransientModel):
    _name = "wizard.generate.employee.report"
    _description = "Wizard para generar reportes de servicios por empleado"

    report_type = fields.Selection([
        ('employee', 'Reporte por Empleado'),
        ('global', 'Reporte Global de Todos los Empleados')
    ], string="Tipo de Reporte", default='employee', required=True)
    
    employee_id = fields.Many2one('hr.employee', string="Empleado", required=False)
    date_from = fields.Date(string="Fecha Desde", required=True)
    date_to = fields.Date(string="Fecha Hasta", required=True)
    
    hr_service_record_ids = fields.Many2many(
        comodel_name="hr.employee.services.record",
        string="Registros de Servicio",
        compute="_compute_hr_service_record_ids",
        help="Registros de servicio relacionados con el empleado y el rango de fechas.",
    )

    @api.depends('report_type', 'employee_id', 'date_from', 'date_to')
    def _compute_hr_service_record_ids(self):
        for record in self:
            domain = []
            
            if record.date_from:
                domain.append(('date', '>=', record.date_from))
            if record.date_to:
                domain.append(('date', '<=', record.date_to))
            
            if record.report_type == 'employee' and record.employee_id:
                domain.append(('employee_id', '=', record.employee_id.id))
            
            record.hr_service_record_ids = self.env['hr.employee.services.record'].search(domain)
    
    @api.onchange('report_type')
    def _onchange_report_type(self):
        """Limpiar empleado cuando se selecciona reporte global"""
        if self.report_type == 'global':
            self.employee_id = False

    def action_print_report(self):
        return self.env.ref('spa.action_report_services').report_action(self)