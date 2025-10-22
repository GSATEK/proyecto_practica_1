Puertos de carga
=================

Módulo Odoo: Puertos de carga

Instalación rápida (Docker)
1. Asegúrate de que la carpeta `puertos_carga` esté dentro del volumen montado en el contenedor Odoo (p.ej. `/mnt/extra-addons-extra`).
2. Reinicia el contenedor y reconstruye: `docker-compose down; docker-compose up -d --build`.
3. En Odoo backend: activar modo desarrollador -> Apps -> Update Apps List -> buscar "Gestión de Puertos y Zonas de carga" -> Instalar.

Rutas web útiles
- /puertos/dashboard  (dashboard web con botones)
- /puertos/chart_data (JSON con datos para gráficos)
- /puertos/get_port/<qr> (JSON por QR)
- /puertos/update_from_qr (POST JSON para actualizar plaza desde QR)

Notas
- Requiere módulos: base, fleet, website
- Cron programado para generar un reporte diario (escribe en ir.logging por ahora)
