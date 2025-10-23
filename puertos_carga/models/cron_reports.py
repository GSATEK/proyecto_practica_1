from odoo import models, api, fields


class FleetPortCron(models.Model):
    _name = "fleet.port.cron"
    _description = "Operaciones programadas"

    @api.model
    def _cron_generate_daily_report(self):
        """Generar estadisticas simples: plazas mas ocupadas y menos ocupadas en el día"""
        now = fields.Datetime.now()
        from_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        to_date = now
        logs = self.env["fleet.port.log"].search(
            [("timestamp", ">=", from_date), ("timestamp", "<=", to_date)]
        )
        stats = {}
        for log in logs:
            pid = log.port_id.id
            stats.setdefault(pid, 0)
            if log.is_occupied:
                stats[pid] += 1
        # ordenar
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        # escribir log con el resultado
        self.env["ir.logging"].create(
            {
                "name": "report_port",
                "type": "server",
                "level": "info",
                "message": "Daily report: %s" % (sorted_stats,),
            }
        )
