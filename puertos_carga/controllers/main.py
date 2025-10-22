from odoo import http
from odoo.http import request

class PuertosController(http.Controller):

    @http.route('/puertos/dashboard', type='http', auth='user', website=True)
    def dashboard(self, **kw):
        ports = request.env['fleet.port'].search([])
        return request.render('puertos_carga.dashboard_template', {'ports': ports})

    @http.route('/puertos/get_port/<string:qr>', type='json', auth='user')
    def get_port(self, qr):
        port = request.env['fleet.port'].search([('qr_code', '=', qr)], limit=1)
        if not port:
            return {'error': 'No encontrada'}
        return {
            'id': port.id,
            'name': port.name,
            'is_occupied': port.is_occupied,
            'vehicle': {
                'id': port.current_vehicle_id.id if port.current_vehicle_id else False,
                'name': port.current_vehicle_id.name if port.current_vehicle_id else False,
                'license_plate': port.current_vehicle_id.license_plate if port.current_vehicle_id else False,
            }
        }

    @http.route('/puertos/update_from_qr', type='json', auth='user', methods=['POST'])
    def update_from_qr(self, **post):
        qr = post.get('qr')
        vehicle = post.get('vehicle')
        port = request.env['fleet.port'].sudo().update_from_qr(qr, vehicle)
        return {'result': True, 'port_id': port.id}

    @http.route('/puertos/get_port_by_id', type='json', auth='user', methods=['POST'])
    def get_port_by_id(self, **post):
        pid = post.get('id')
        port = request.env['fleet.port'].browse(int(pid)) if pid else None
        if not port or not port.exists():
            return {'error': 'No encontrada'}
        return {
            'id': port.id,
            'name': port.name,
            'is_occupied': port.is_occupied,
            'vehicle': {
                'id': port.current_vehicle_id.id if port.current_vehicle_id else False,
                'name': port.current_vehicle_id.name if port.current_vehicle_id else False,
                'license_plate': port.current_vehicle_id.license_plate if port.current_vehicle_id else False,
            }
        }

    @http.route('/puertos/chart_data', type='json', auth='user')
    def chart_data(self, **post):
        # preparar datos: conteo de ocupaciones por plaza hoy y actividad por hora
        from datetime import datetime, timedelta
        today = datetime.now()
        from_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        to_date = today

        logs = request.env['fleet.port.log'].search([('timestamp', '>=', from_date), ('timestamp', '<=', to_date)])
        stats = {}
        hours = {h: 0 for h in range(24)}
        for l in logs:
            pid = l.port_id.name or ('#%s' % l.port_id.id)
            stats.setdefault(pid, 0)
            if l.is_occupied:
                stats[pid] += 1
            if l.timestamp:
                try:
                    hr = int(str(l.timestamp)[11:13])
                    hours[hr] = hours.get(hr, 0) + 1
                except Exception:
                    pass

        port_labels = list(stats.keys())
        port_values = [stats[k] for k in port_labels]
        hour_labels = [str(h) for h in range(24)]
        hour_values = [hours[h] for h in range(24)]
        return {'port_labels': port_labels, 'port_values': port_values, 'hour_labels': hour_labels, 'hour_values': hour_values}
