from odoo import fields, models, api

class HrServicesReport(models.Model):
    _name = 'hr.services.report'
    _description = 'HR Services Report'

    name = fields.Char('Service Name', help='Name of the HR service')
    description = fields.Text('Description', help='Description of the HR service')

