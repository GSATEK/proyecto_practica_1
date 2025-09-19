from odoo import fields, models, api

class HrServicesReport(models.Model):
    _name = 'hr.services.report'
    _description = 'HR Services Report'

    name = fields.Char('Service Name', help='Name of the HR service')
    description = fields.Text('Description', help='Description of the HR service')
    employee_id = fields.Many2one('hr.employee', string='Employee', help='Employee associated with the service')
    partner_id = fields.Many2one('res.partner', string='Client', help='Client associated with the service')

