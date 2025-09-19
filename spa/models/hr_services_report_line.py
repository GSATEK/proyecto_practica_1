from odoo import fields, models, api

class HrServicesReportLine(models.Model):
    _name = 'hr.services.report.line'
    _description = 'HR Services Report Line'

    service_id = fields.Many2one('hr.services.report', string='Service', help='Related HR service')
    quantity = fields.Integer('Quantity', default=1, help='Quantity of the service')
    unit_price = fields.Float('Unit Price', help='Price per unit of the service')