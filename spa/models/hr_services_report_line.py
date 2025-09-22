from odoo import fields, models, api

class HrEmployeeServicesReportLine(models.Model):
    _name = 'hr.employee.services.report.line'
    _description = 'HR Services Report Line'

    report_id = fields.Many2one(
        'hr.employee.services.report', 
        string='Service Report',
        required=True,
        ondelete='cascade',
    )
    
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', default=1.0)
    unit_price = fields.Monetary('Unit Price', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='report_id.currency_id',
        store=False, readonly=True
    )
    subtotal = fields.Monetary(
        'Subtotal',
        compute='_compute_subtotal',
        currency_field='currency_id',
        store=True
    )
    
    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = (line.quantity or 0.0) * (line.unit_price or 0.0)