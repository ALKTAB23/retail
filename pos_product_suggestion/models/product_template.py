# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_suggestion_id = fields.Many2one(
        'product.product', string='POS Suggestion',
        help='Suggested product variant to show in POS.'
    )

    suggestion_line = fields.One2many(
        'pos.product.suggestion.line', 'product_tmpl_id',
        string='POS Suggestions'
    )

