# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # سويتش تفعيل الميزة (اختياري؛ علّق السطر لو لا تريد جروب)
    group_sh_product_tags = fields.Boolean(
        string="Product Tags",
        implied_group="sh_pos_all_in_one_retail.group_sh_product_tags",
    )

    # وسوم افتراضية مرتبطة بالشركة
    product_tags_id = fields.Many2many(
        'sh.product.tag',
        string="Default Product Tags",
        related='company_id.product_tags_id',
        readonly=False
    )

