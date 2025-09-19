{
    'name': 'SPA',
    'version': '1.0.0',
    'description': """
        Módulo para la gestión de servicios de un SPA en ODOO.
    """,
    'depends': ['base','product', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'wizards/wizard_add_service.xml',
        'reports/report_services.xml',
    ],
    "images": ["static/description/icon.png"]
}
