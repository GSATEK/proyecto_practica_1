from odoo import api, fields, models, _

class wizardAddService(models.TransientModel):
    _name = "wizard.add.service"
    _description = "Wizard para agregar servicios a un cliente"
    
    exemple_field = fields.Char(string="Campo de Ejemplo", help="Este es un campo de ejemplo para el wizard.")
    
    name_employee = fields.Many2one('hr.employee', string="Empleado", help="Seleccione el empleado asociado al servicio.")
    
    def action_add_service(self):
        # Lógica para agregar el servicio al cliente
        return True
    
    