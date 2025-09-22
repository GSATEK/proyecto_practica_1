from odoo import fields, models, api

class HrServicesReport(models.Model):
    _name = 'hr.services.report'
    _description = 'HR Services Report'

    # Basic fields
    name = fields.Char('Reference', help='Reference of the service report')
    description = fields.Text('Description')
    date_report = fields.Datetime('Report Date', default=fields.Datetime.now)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    partner_id  = fields.Many2one('res.partner', string='Client', required=True)
    line_ids = fields.One2many(
        'hr.services.report.line',
        'report_id',
        string="Service Lines",
    )
    commission_rate = fields.Float('Commission', help='Commission for the service')
    total_amount = fields.Monetary(
        'Total Amount',
        compute='_compute_total_amount',
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id
    )
    
    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('subtotal'))