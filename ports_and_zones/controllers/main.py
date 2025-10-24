from odoo import http
from odoo.http import request
import logging

logger = logging.getLogger(__name__)


class PropetiesController(http.Controller):
    @http.route("/", type="http", auth="public", website=True)
    def homePage(self, **kw):
        return request.render("ports_and_zones.homeTemplate")

    @http.route("/qr-scan", type="http", auth="user", website=True)
    def qrScan(self, **kw):
        return request.render("ports_and_zones.qrScanTemplate")

    @http.route(
        "/qr-scan-data",
        auth="user",
        methods=["POST"],
        csrf=False,
        type="json",
        cors="*",
    )
    def submitQrScan(self, **kw):
        data = request.get_json_data()
        user = request.env.user
        port_id_qr = data.get("port_id")
        vehicle_id_qr = data.get("vehicle_id")
        user_action = data.get("user_action")

        logger.info(
            f"Usuario: {user.id} | Puerto QR: {port_id_qr} | Vehículo QR: {vehicle_id_qr}"
        )

        Port = request.env["fleet.ports"]
        Vehicle = request.env["fleet.vehicle"]

        port_record = Port.sudo().search([("port_id", "=", port_id_qr)], limit=1)

        if not port_record:
            return {
                "success": False,
                "message": f"Error: Puerto con ID '{port_id_qr}' no encontrado.",
            }

        vehicle_record = Vehicle.sudo().search([("id", "=", vehicle_id_qr)], limit=1)

        if not vehicle_record:
            return {
                "success": False,
                "message": f"Error: Vehículo con ID '{vehicle_id_qr}' (Matrícula) no encontrado.",
            }

        try:
            port_record.sudo().write(
                {
                    "vehicle_id": (vehicle_record.id, False)[user_action == "entrar"],
                    "port_status": "libre" if user_action == "salir" else "ocupado",
                }
            )

            return {
                "success": True,
                "message": f"Puerto {port_id_qr} asignado al vehículo {vehicle_id_qr}.",
            }

        except Exception as e:
            logger.error(f"Error al asignar puerto/vehículo: {e}")
            return {
                "success": False,
                "message": f"Error interno al actualizar registros: {e}",
            }
