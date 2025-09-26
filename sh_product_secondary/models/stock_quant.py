# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockQuant(models.Model):
    _inherit = "stock.quant"

    secondary_unit_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Secondary UoM",
        help="Optional secondary unit used to display/convert the On Hand quantity."
    )

    secondary_qty = fields.Float(
        string="Secondary Qty",
        compute="_compute_secondary_qty",
        digits="Product Unit of Measure",
        help="Quantity expressed in the secondary unit if available."
    )

    @api.depends('quantity', 'product_uom_id', 'secondary_unit_id')
    def _compute_secondary_qty(self):
        for quant in self:
            sec_uom = quant.secondary_unit_id
            if not sec_uom:
                tmpl = quant.product_id.product_tmpl_id
                # أسماء شائعة لحقل وحدة ثانوية في إضافات أخرى
                for fname in ('secondary_uom_id', 'secondary_unit_id', 'alt_uom_id', 'dual_uom_id'):
                    if hasattr(tmpl, fname):
                        candidate = getattr(tmpl, fname)
                        try:
                            candidate = candidate if candidate and candidate.id else False
                        except Exception:
                            candidate = False
                        if candidate:
                            sec_uom = candidate
                            break
            if quant.product_uom_id and sec_uom and quant.product_uom_id.category_id == sec_uom.category_id:
                try:
                    quant.secondary_qty = quant.product_uom_id._compute_quantity(
                        quant.quantity, sec_uom, rounding_method='HALF-UP'
                    )
                except Exception:
                    quant.secondary_qty = 0.0
            else:
                quant.secondary_qty = 0.0

