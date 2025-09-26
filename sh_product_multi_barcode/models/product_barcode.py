# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# ------------------------------------------------------------
# TEMPLATE: expose barcode lines of the main variant on template form
# ------------------------------------------------------------
class ShProductTemplate(models.Model):
    _inherit = 'product.template'

    # ملاحظة هامة:
    # related عبر product_variant_ids (one2many) غير موثوق.
    # في 18 نربطه بـ product_variant_id (الڤاريانت الأساسي) ليكون قابلًا للتحرير وآمن.
    barcode_line_ids = fields.One2many(
        related='product_variant_id.barcode_line_ids',
        string='Barcode Lines (Main Variant)',
        readonly=False,
        help="Edit barcode lines of the main variant directly from the template."
    )

    # UoM category (قراءة فقط من uom_id)
    uom_category_id = fields.Many2one(
        "uom.category",
        string="UOM Category",
        related="uom_id.category_id",
        readonly=True
    )

    @api.constrains('barcode', 'barcode_line_ids')
    def check_uniqe_name(self):
        """شفرة التأكد من فريدة الباركود على مستوى الشركة (عند تفعيل الإعداد)."""
        for rec in self:
            if self.env.company and self.env.company.sh_multi_barcode_unique:
                if rec.barcode:
                    multi_barcode_id = self.env['product.template.barcode'].search(
                        [('name', '=', rec.barcode)], limit=1
                    )
                    if multi_barcode_id:
                        raise ValidationError(_('Barcode must be unique!'))

    @api.model_create_multi
    def create(self, vals_list):
        """بعد إنشاء الـ template، مرر قيم barcode_line_ids إلى الڤاريانت الأساسي لو كانت قادمة مع الإنشاء."""
        templates = super().create(vals_list)
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if vals.get('barcode_line_ids'):
                related_vals['barcode_line_ids'] = vals['barcode_line_ids']
            if related_vals:
                # يطبّق على الڤاريانت الأساسي عبر الـ related أعلاه
                template.write(related_vals)
        return templates


# ------------------------------------------------------------
# PRODUCT (variant): actual storage of barcode lines
# ------------------------------------------------------------
class ShProduct(models.Model):
    _inherit = 'product.product'

    barcode_line_ids = fields.One2many(
        'product.template.barcode',
        'product_id',
        string='Barcode Lines',
        ondelete="cascade"
    )

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """اجعل البحث باسم المنتج يشمل باركود السطور الثانوية أيضاً."""
        args = args or []
        res = super()._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

        # ابحث بسجلات الباركود الثانوية (خطوط) بالاسم مباشرة
        extra_ids = list(self._search(
            [('barcode_line_ids.name', '=', name)] + args,
            limit=limit,
            access_rights_uid=name_get_uid
        ))
        if extra_ids:
            # res هو list[(id, name)] بينما _search يعيد ids
            # نحافظ على ترتيب/قيود limit بتجميع النتائج
            return res + extra_ids
        return res

    @api.constrains('barcode', 'barcode_line_ids')
    def check_uniqe_name(self):
        """تأكّد أن الباركود فريد على مستوى product + خطوطه."""
        for rec in self:
            if self.env.company and self.env.company.sh_multi_barcode_unique and rec.barcode:
                multi_barcode_id = self.env['product.template.barcode'].search(
                    [('name', '=', rec.barcode)], limit=1
                )
                if multi_barcode_id:
                    raise ValidationError(_('Barcode must be unique!'))


# ------------------------------------------------------------
# BARCODE LINE model (secondary barcodes, pricing tie-in with pricelists)
# ------------------------------------------------------------
class ShProductBarcode(models.Model):
    _name = 'product.template.barcode'
    _description = "Product Barcode"
    _order = 'id desc'

    product_id = fields.Many2one('product.product', 'Product', required=True, ondelete="cascade")
    product_type = fields.Selection(related='product_id.type', store=True, readonly=True)
    product_active = fields.Boolean('Active', store=True, related="product_id.active")
    name = fields.Char("Barcode", required=True)
    price = fields.Float("Price")
    available_item = fields.Boolean('Valuable Sale & POS', store=True)
    unit = fields.Many2one('uom.uom', 'Secondary UOM', required=True)
    price_lst = fields.Many2one('product.pricelist', string='Pricelist', required=True)
    negative_qty_price = fields.Boolean('Allow Negative Quantity & Price', store=True)
    item_pricelist_id = fields.Many2one('product.pricelist.item', string='Linked Pricelist Item')

    def create_update_price_item(self, item_pricelist_id=False, context=None):
        """أنشئ/حدّث سطر قائمة الأسعار الموافق لهذا الباركود."""
        context = dict(self.env.context or (context or {}))
        if context.get('updating_price', False):
            return True

        # ملاحظة: 'applied_on' و 'compute_price' و 'fixed_price' ما زالت مدعومة في 18
        # عند أي تغيير مستقبلي سنحوّلها للحقول البديلة، لكن الآن تُستخدم كما هي.
        item_vals = {
            'product_id': self.product_id.id,
            'uom_id': self.unit.id,
            'multi_barcode': self.name,        # حقل مخصص لديك على pricelist.item
            'pricelist_id': self.price_lst.id,
            'fixed_price': self.price,
            'applied_on': '0_product_variant',
            'compute_price': 'fixed',
        }
        # لو كان موجودًا نعدّله، وإلا ننشئه
        existing_item = item_pricelist_id or self.env['product.pricelist.item'].sudo().search(
            [('multi_barcode', '=', self.name), ('pricelist_id', '=', self.price_lst.id)],
            limit=1
        )
        if existing_item:
            existing_item.with_context(updating_price=True).write(item_vals)
            if not item_pricelist_id:
                self.item_pricelist_id = existing_item.id
        else:
            new_item = self.env['product.pricelist.item'].with_context(updating_price=True).create(item_vals)
            self.item_pricelist_id = new_item.id
        return True

    @api.model
    def create(self, vals):
        recs = super().create(vals)
        context = dict(self.env.context or {})
        for rec in recs:
            if rec.price_lst and not context.get('updating_price', False):
                rec.create_update_price_item()
        return recs

    def write(self, vals):
        res = super().write(vals)
        context = dict(self.env.context or {})
        # لا تحدّث من حلقة pricelist.item نفسها لتجنّب الدورة
        if self._context.get('params') and self._context['params'].get('model') == 'product.pricelist.item':
            return res
        if not context.get('updating_price', False):
            for rec in self:
                if rec.price_lst:
                    rec.create_update_price_item(rec.item_pricelist_id, context=self._context)
        return res

    def unlink(self):
        for rec in self:
            if rec.item_pricelist_id and not rec.env.context.get('force_delete', False):
                rec.item_pricelist_id.with_context(force_delete=True).unlink()
        return super().unlink()

    @api.constrains('name')
    def check_uniqe_name(self):
        """فحص فريدة الباركود على مستوى المنتجات وخطوط الباركود."""
        for rec in self:
            # تكرار على product.product (الباركود الرئيسي أو في خطوط أخرى)
            prod = self.env['product.product'].sudo().search(
                ['|', ('barcode', '=', rec.name), ('barcode_line_ids.name', '=', rec.name),
                 ('id', '!=', rec.product_id.id)], limit=1)
            if prod:
                raise ValidationError(_('Barcode must be unique!'))

            # تكرار ضمن نفس الجدول
            barcode_line = self.env['product.template.barcode'].search(
                [('name', '=', rec.name), ('id', '!=', rec.id)], limit=1)
            if barcode_line:
                raise ValidationError(_('Barcode must be unique!'))

    @api.model
    def sh_create_from_pos(self, vals):
        rec = self.create(vals)
        return rec.read()


# ------------------------------------------------------------
# PRICELIST item back-link update (keep 2-way sync)
# ------------------------------------------------------------
class ShProductPriceListItem(models.Model):
    _inherit = 'product.pricelist.item'

    dynamic_price_ids = fields.One2many(
        "product.template.barcode", "item_pricelist_id", string='Dynamic Products Barcode'
    )

    def create_update_price_item(self, item_pricelist_id=False):
        """عند تعديل سطر pricelist، عكس السعر والوحدة إلى سجلات الباركود المرتبطة."""
        context = dict(self.env.context or {})
        for rec in self:
            vals = {
                'price': rec.fixed_price,
                'unit': rec.uom_id.id,
                'product_id': rec.product_id.id,
            }
            linked_barcodes = rec.env['product.template.barcode'].sudo().search(
                [('name', '=', rec.multi_barcode), ('price_lst', '=', rec.pricelist_id.id)]
            )
            if linked_barcodes:
                linked_barcodes.with_context(updating_price=True).write(vals)
        return True

    def write(self, vals):
        res = super().write(vals)
        # إذا لم تكن الكتابة آتية من product.product (لتجنّب دورات)
        if not (self._context.get('params') and self._context['params'].get('model') == 'product.product'):
            for rec in self:
                rec.create_update_price_item()
        return res

    def unlink(self):
        for rec in self:
            if rec.dynamic_price_ids and not rec.env.context.get('force_delete', False):
                rec.dynamic_price_ids.with_context(force_delete=True).unlink()
        return super().unlink()

