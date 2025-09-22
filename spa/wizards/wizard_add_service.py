from odoo import api, fields, models, _

class WizardAddEmployeeService(models.TransientModel):
    _name = "wizard.add.employee.service"
    _description = "Wizard para agregar servicios a un cliente"

    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)

    line_ids = fields.One2many(
        'wizard.add.employee.service.line', 'wizard_id',
        string="Líneas", help="Productos y cantidades a agregar al reporte"
    )

    def action_add_service(self):
        self.ensure_one()
        report_vals = {
            'name': _('Service Report - %s') % (self.partner_id.display_name or ''),
            'employee_id': self.employee_id.id,
            'partner_id': self.partner_id.id,
        }
        report = self.env['hr.employee.services.report'].create(report_vals)  # usa tu modelo existente :contentReference[oaicite:1]{index=1}

        line_commands = []
        for wl in self.line_ids:
            if not wl.product_id:
                continue
            line_commands.append((0, 0, {
                'product_id': wl.product_id.id,
                'quantity': wl.quantity or 0.0,
                'unit_price': wl.unit_price or 0.0,
            }))
        if line_commands:
            report.write({'line_ids': line_commands})
        return {'type': 'ir.actions.act_window_close'}


class WizardAddEmployeeServiceLine(models.TransientModel):
    _name = "wizard.add.employee.service.line"
    _description = "Línea del wizard de servicios"
    _order = "sequence, id"

    wizard_id = fields.Many2one('wizard.add.employee.service', string="Wizard",
                                required=True, ondelete='cascade', default=lambda self: self._context.get('default_wizard_id'),)
    sequence = fields.Integer('Secuencia', default=10)  # <— nuevo para el “handle”
    product_id = fields.Many2one('product.product', string="Producto", required=True)
    quantity = fields.Float('Cantidad', default=1.0)
    unit_price = fields.Float('Precio Unitario')
    subtotal = fields.Float('Subtotal', compute='_compute_subtotal', store=False)

    @api.onchange('product_id')
    def _onchange_product_id_set_price(self):
        for rec in self:
            rec.unit_price = rec.product_id.list_price if rec.product_id else 0.0

    @api.onchange('quantity', 'unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = (rec.quantity or 0.0) * (rec.unit_price or 0.0)

    ''' def action_add_service(self):
        report = self.env['hr.employee.services.report']
        value = {
            'name': self.partner_id.name,
            'employee_id': self.employee_id,
        }
        report.create(value)
    '''