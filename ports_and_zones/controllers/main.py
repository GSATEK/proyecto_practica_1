from odoo import http
from odoo.http import request
import logging

logger = logging.getLogger(__name__)


class PropetiesController(http.Controller):
    @http.route("/", tupe="http", auth="public", website=True)
    def homePage(self, **kw):
        return request.render("ports_and_zones.homeTemplate")
    
    @http.route("/qr-scan", type="http", auth="public", website=True)
    def qrScan(self, **kw):
        return request.render("ports_and_zones.qrScanTemplate")
