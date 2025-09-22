from odoo import api, fields, models, _

class WizardAddEmployeeService(models.TransientModel):
    _name = "wizard.add.employee.service"
    _description = "Wizard para agregar servicios a un cliente"

    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    line_ids = fields.One2many(
        'wizard.add.employee.service.line', 
        'wizard_id',
        string="Líneas de Servicio",
        required=False,
    )

    def action_add_service(self):
        self.ensure_one()
        report_vals = {
            'name': _('Service Report - %s') % (self.partner_id.display_name or ''),
            'employee_id': self.employee_id.id,
            'partner_id': self.partner_id.id,
        }
        self.env['hr.employee.services.report'].create(report_vals)
        return {'type': 'ir.actions.act_window_close'}

class WizardAddEmployeeServiceLine(models.TransientModel):
    _name = "wizard.add.employee.service.line"
    _description = "Wizard Linieas para agregar servicios a un cliente"
    
    product_id = fields.Many2one('product.template', string='Producto', required=True)
    quantity = fields.Float('Cantidad', default=1.0)
    
    wizard_id = fields.Many2one('wizard.add.employee.service', string='Wizard', required=True, ondelete='cascade')
    