# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sh_product_id = fields.Many2one(
        'product.product', string='SH Variant (Helper)',
        compute='_compute_sh_product_id', store=True, readonly=True,
        help='Helper field for old views; equals product_variant_id.'
    )

    sh_qty = fields.Float(
        string='Quantity (All Variants)',
        compute='_compute_sh_qty', store=False, readonly=True,
        help='Sum of qty_available of all variants.'
    )

    sh_uom = fields.Many2one(
        'uom.uom', string='UoM (Helper)',
        related='uom_id', store=True, readonly=True,
        help='Mirror of uom_id for backward compatible views.'
    )

    sh_cost_price = fields.Float(
        string='Cost (Helper)',
        related='standard_price', store=True, readonly=True,
        help='Mirror of standard_price for backward compatible views.'
    )

    sh_price_unit = fields.Float(
        string='Sale Price (Helper)',
        related='list_price', store=True, readonly=True,
        help='Mirror of list_price for backward compatible views.'
    )

    # ✅ الجديد: Subtotal (Helper) كمرآة مؤقتة لسعر البيع
    sh_price_subtotal = fields.Float(
        string='Subtotal (Helper)',
        related='list_price', store=True, readonly=True,
        help='Mirror of list_price for old views; adjust later if subtotal logic is needed.'
    )

    def _compute_sh_product_id(self):
        for rec in self:
            rec.sh_product_id = rec.product_variant_id

    @api.depends('product_variant_ids', 'product_variant_ids.qty_available')
    def _compute_sh_qty(self):
        for rec in self:
            rec.sh_qty = sum(rec.product_variant_ids.mapped('qty_available'))

