from odoo import api, fields, models, _

class WizardAddEmployeeService(models.TransientModel):
    _name = "wizard.add.employee.service"
    _description = "Wizard para agregar servicios a un cliente"

    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    description = fields.Text('Descripción')
    date = fields.Datetime(string="Fecha", required=True, default=fields.Datetime.now)
    line_ids = fields.One2many(
        'wizard.add.employee.service.line', 
        'wizard_id',
        string="Líneas de Servicio",
        required=False,
    )

    def action_add_service(self):
        self.ensure_one()
        report_vals = {
            'employee_id': self.employee_id.id,
            'partner_id': self.partner_id.id,
            'line_ids': [(0, 0, {
            'product_id': line.product_id.id,
            'quantity': line.quantity,
            'unit_price': line.unit_price,
            'description': self.description,
        }) for line in self.line_ids],
        }
        report = self.env['hr.employee.services.record'].create(report_vals)
        return {
            'name': _('Service Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee.services.record', 
            'view_mode': 'form',
            'res_id': report.id,
            'target': 'current',
        }

class WizardAddEmployeeServiceLine(models.TransientModel):
    _name = "wizard.add.employee.service.line"
    _description = "Wizard Linieas para agregar servicios a un cliente"
    
    product_id = fields.Many2one('product.template', string='Producto', required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env['res.currency'].search([('name', '=', 'EUR')], limit=1).id
    )
    quantity = fields.Float('Cantidad', default=1.0)
    unit_price = fields.Monetary('Unit Price', currency_field='currency_id')
    subtotal = fields.Monetary(
        'Subtotal', compute='_compute_subtotal', currency_field='currency_id', store=True)
    
    wizard_id = fields.Many2one('wizard.add.employee.service', string='Wizard', required=True, ondelete='cascade')
    
    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = (line.quantity or 0.0) * (line.unit_price or 0.0)