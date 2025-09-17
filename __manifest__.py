{
    'name': 'SPA',
    'description': """
    """,
    'depends': ['base','product','partner'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_pokemon.xml',
        'views/portal_templates.xml',
        'views/res_partner.xml',
        'views/view_website_header.xml',
        'views/res_pokedex.xml',
        'wizards/wizard_example.xml',
        'reports/report_pokemon.xml',
        'reports/move_tax_report.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'pokedex/static/src/css/pokemon_style.css',
        ],
    },
    "images": ["static/description/icon.png"], 
}
