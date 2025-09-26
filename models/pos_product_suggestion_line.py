# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosProductSuggestionLine(models.Model):
    _inherit = 'pos.product.suggestion.line'

    # اجعل الفاريانت غير إجباري (v16 كان يقبل القالب فقط)
    product_variant_id = fields.Many2one(
        'product.product',
        string='Suggested Variant',
        required=False,      # <= أهم تغيير
    )

    # alias متوافق مع بعض الواجهات القديمة
    product_suggestion_id = fields.Many2one(
        'product.template',
        string='Product Template (Suggestion)',
        related='product_tmpl_id',
        readonly=False,
    )

    # عندما يختار المستخدم القالب فقط، نكمل الفاريانت الافتراضي
    @api.onchange('product_tmpl_id', 'product_suggestion_id')
    def _onchange_template_set_variant(self):
        for line in self:
            # إبقاء alias و الحقل الأصلي متزامنين
            if line.product_suggestion_id and not line.product_tmpl_id:
                line.product_tmpl_id = line.product_suggestion_id
            # لو ما فيه فاريانت، عيّن الفاريانت الافتراضي للقالب
            if line.product_tmpl_id and not line.product_variant_id:
                line.product_variant_id = line.product_tmpl_id.product_variant_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # دعم الكتابة عبر alias القديم
            if vals.get('product_suggestion_id') and not vals.get('product_tmpl_id'):
                vals['product_tmpl_id'] = vals['product_suggestion_id']

            # لو أُرسل القالب فقط بدون فاريانت، عيّنه تلقائياً
            if not vals.get('product_variant_id') and vals.get('product_tmpl_id'):
                tmpl = self.env['product.template'].browse(vals['product_tmpl_id'])
                if tmpl:
                    vals['product_variant_id'] = tmpl.product_variant_id.id
        return super().create(vals_list)

    def write(self, vals):
        vals = dict(vals or {})
        # دعم الكتابة عبر alias
        if vals.get('product_suggestion_id') and not vals.get('product_tmpl_id'):
            vals['product_tmpl_id'] = vals['product_suggestion_id']

        # لو تم تغيير القالب ولم يُحدّد الفاريانت، عيّنه تلقائياً
        if vals.get('product_tmpl_id') and not vals.get('product_variant_id'):
            tmpl = self.env['product.template'].browse(vals['product_tmpl_id'])
            if tmpl:
                vals['product_variant_id'] = tmpl.product_variant_id.id
        return super().write(vals)

