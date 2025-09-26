# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    secondary_unit_id = fields.Many2one(
        'uom.uom',
        string='Secondary UoM',
        help='Optional secondary unit used to display/print line quantity.'
    )

    secondary_qty = fields.Float(
        string='Secondary Qty',
        compute='_compute_secondary_qty',
        digits='Product Unit of Measure',
        help='Quantity expressed in the secondary unit if available and compatible.'
    )

    @api.depends('qty', 'product_id', 'secondary_unit_id')
    def _compute_secondary_qty(self):
        for line in self:
            sec_uom = line.secondary_unit_id
            if not sec_uom and line.product_id:
                tmpl = line.product_id.product_tmpl_id
                # أسماء شائعة للوحدة الثانوية في إضافات أخرى
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
            base_uom = line.product_id.uom_id if line.product_id else False
            if base_uom and sec_uom and base_uom.category_id == sec_uom.category_id:
                try:
                    line.secondary_qty = base_uom._compute_quantity(
                        line.qty, sec_uom, rounding_method='HALF-UP'
                    )
                except Exception:
                    line.secondary_qty = 0.0
            else:
                line.secondary_qty = 0.0
