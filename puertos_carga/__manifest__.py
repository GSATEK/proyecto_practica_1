{
    "name": "Gestión de Puertos y Zonas de carga",
    "version": "1.0.0",
    "summary": "Módulo para la gestión de puertos y zonas de carga",
    "description": "-.-",
    "author": "Jhonny",
    "website": "https://github.com/vandalieu06",
    "depends": ["base", "fleet", "web", "website"],
    "data": [
        "security/ir.model.access.csv",
        "views/dashboard_views.xml",
        "views/dashboard_templates.xml",
        "views/chart_templates.xml",
        "data/cron_jobs.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "puertos_carga/static/src/js/form_qr.js"
        ],
        "web.assets_qweb": [
            "puertos_carga/static/src/xml/templates.xml"
        ]
    }
}
