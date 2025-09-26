# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def _auto_validate_pos_session(self):
        """
        Cron entry point.
        يغلق/يعتمد تلقائياً الجلسات في الحالات 'opened' أو 'closing_control'.
        لا يوقف الخدمة عند وجود خطأ؛ يسجل الخطأ في log.track ويكمل.
        """
        # قلل الحمل لو عندك عدد كبير من الجلسات
        LIMIT = 100

        domain = [('state', 'in', ('opened', 'closing_control'))]
        sessions = self.sudo().search(domain, limit=LIMIT)

        if not sessions:
            _logger.debug("Auto POS validate: no sessions to process.")
            return True

        processed = failed = 0
        for rec in sessions:
            try:
                # تسلسل الإغلاق القياسي في v17/18
                rec.sudo().action_pos_session_closing_control()
                # بعض التركيبات قد تعتمد مباشرة بعد الإغلاق
                if hasattr(rec, "action_pos_session_validate"):
                    rec.sudo().action_pos_session_validate()
                processed += 1
                _logger.info("Auto-validated POS session %s (id=%s)", rec.name, rec.id)
            except UserError as e:
                failed += 1
                msg = (e.name or getattr(e, "value", None) or str(e)).strip()
                _logger.warning("Auto-validate failed for session %s: %s", rec.id, msg)
                self.env["log.track"].sudo().create({
                    "date": fields.Date.context_today(self),
                    "session_id": rec.id,
                    "error": msg,
                })
            except Exception as e:
                failed += 1
                _logger.exception("Unexpected error while auto-validating session %s", rec.id)
                self.env["log.track"].sudo().create({
                    "date": fields.Date.context_today(self),
                    "session_id": rec.id,
                    "error": str(e),
                })

        _logger.info("Auto POS validate finished: processed=%s failed=%s", processed, failed)
        return True


class LogTrack(models.Model):
    _name = "log.track"
    _description = "Log Track for POS Auto-Validation"
    _rec_name = "session_id"

    date = fields.Date("Date", default=lambda self: fields.Date.context_today(self))
    session_id = fields.Many2one("pos.session", string="Session", ondelete="set null")
    error = fields.Char("Error")

