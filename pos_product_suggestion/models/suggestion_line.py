# -*- coding: utf-8 -*-
from odoo import models, fields

class PosProductSuggestionLine(models.Model):
    _name = 'pos.product.suggestion.line'
    _description = 'POS Product Suggestion Line'
    _order = 'id desc'

    product_tmpl_id = fields.Many2one(
        'product.template', required=True, ondelete='cascade', index=True
    )
    product_variant_id = fields.Many2one(
        'product.product', string='Suggested Variant',
        required=True, domain="[('product_tmpl_id','=',product_tmpl_id)]"
    )
    note = fields.Char()
    active = fields.Boolean(default=True)

