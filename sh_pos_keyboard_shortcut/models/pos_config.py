# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    """
    امتداد لإعدادات نقطة البيع لإضافة مفاتيح الاختصار + نطاق تطبيقها.
    هذا الملف يحافظ على كل الميزات كما في الموديول الأصلي، ويضيف الحقول
    المطلوبة في Odoo 18 والتي تحتاجها الـ views (sh_shortcut_screen/sh_shortcut_screen_type).
    """
    _inherit = 'pos.config'

    # تشغيل/تعطيل ميزة اختصارات لوحة المفاتيح
    sh_enable_shortcut = fields.Boolean(string="Enable Shortcut Key")

    # نطاق شاشة الاختصارات (تستخدمها بعض الـ views مباشرة على pos.config)
    sh_shortcut_screen = fields.Selection([
        ('all', 'All Screens'),
        ('product_screen', 'Product Screen'),
        ('payment_screen', 'Payment Screen'),
        ('order_screen', 'Order Screen'),
        ('customer_screen', 'Customer Screen'),
        ('receipt_screen', 'Receipt Screen'),
    ], string="Shortcut Scope", default='product_screen')

    # نوع الشاشة (حقـل مورد في الـ views ابتداء من 17/18)
    sh_shortcut_screen_type = fields.Selection([
        ('all', 'All Screens'),
        ('product_screen', 'Product Screen'),
        ('payment_screen', 'Payment Screen'),
        ('order_screen', 'Order Screen'),
        ('customer_screen', 'Customer Screen'),
        ('receipt_screen', 'Receipt Screen'),
    ], string="Shortcut Screen Type", default='product_screen')

    # مفاتيح اختصار عامة مرتبطة بالكونفيج
    sh_shortcut_keys_screen = fields.One2many(
        'sh.pos.keyboard.shortcut', 'config_id', string="POS Shortcut Key"
    )
    # مفاتيح اختصار خاصة بطرق الدفع
    sh_payment_shortcut_keys_screen = fields.One2many(
        'sh.pos.keyboard.shortcut', 'payment_config_id', string="POS Payment Method Shortcut Key"
    )

    @api.model
    def default_get(self, fields_list):
        """
        يُنشئ قيَم افتراضية لمفاتيح الاختصارات عند إنشاء Config جديد.
        نحافظ على السلوك الأصلي، مع الحرص على استخدام xmlids الصحيحة من نفس الموديول.
        """
        res = super(PosConfig, self).default_get(fields_list)

        key_list = []
        vals = []

        # ====== Payment screen: Shift + P => go_payment_screen ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_shift', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_P', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'go_payment_screen',
                'sh_shortcut_screen_type': 'payment_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== All screens: Ctrl + C => go_customer_Screen ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_control', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_c', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'go_customer_Screen',
                'sh_shortcut_screen_type': 'all',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Product screen: Shift + G => go_order_Screen ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_shift', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_G', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'go_order_Screen',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Payment screen: v => validate_order ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_v', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'validate_order',
                'sh_shortcut_screen_type': 'payment_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Receipt screen: n => next_order ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_n', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'next_order',
                'sh_shortcut_screen_type': 'receipt_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== All screens: Esc => go_to_previous_screen ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_escape', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'go_to_previous_screen',
                'sh_shortcut_screen_type': 'all',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Product screen: q => select_quantity_mode ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_q', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'select_quantity_mode',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Product screen: d => select_discount_mode ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_d', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'select_discount_mode',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Product screen: p => select_price_mode ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_p', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'select_price_mode',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Product screen: f => search_product ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_f', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'search_product',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Order screen: f => search_order ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_f', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'search_order',
                'sh_shortcut_screen_type': 'order_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== All screens: Insert => add_new_order ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_Insert', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'add_new_order',
                'sh_shortcut_screen_type': 'all',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== All screens: Ctrl + Delete => destroy_current_order ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_control', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_delete', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'destroy_current_order',
                'sh_shortcut_screen_type': 'all',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Product screen: Delete => delete_orderline ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_delete', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            key_list.append(temp_key_id.id)
        if key_list:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'delete_orderline',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, key_list)]
            }))
        key_list = []

        # ====== Product screen: Arrow Up/Down => select_up/down_orderline ======
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_up', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            vals.append((0, 0, {
                'sh_shortcut_screen': 'select_up_orderline',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, [temp_key_id.id])]
            }))
        key_id = self.env.ref('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_down', raise_if_not_found=False)
        if key_id:
            temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
            vals.append((0, 0, {
                'sh_shortcut_screen': 'select_down_orderline',
                'sh_shortcut_screen_type': 'product_screen',
                'sh_key_ids': [(6, 0, [temp_key_id.id])]
            }))

        # ====== Customer screen: f / arrows / enter / e / s / + ======
        for xmlid, action in [
            ('sh_pos_all_in_one_retail.sh_keyboard_key_f', 'search_customer'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_up', 'select_up_customer'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_down', 'select_down_customer'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_Enter', 'set_customer'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_e', 'edit_customer'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_s', 'save_customer'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_+', 'create_customer'),
        ]:
            key_id = self.env.ref(xmlid, raise_if_not_found=False)
            if key_id:
                temp_key_id = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_id.id})
                vals.append((0, 0, {
                    'sh_shortcut_screen': action,
                    'sh_shortcut_screen_type': 'customer_screen',
                    'sh_key_ids': [(6, 0, [temp_key_id.id])]
                }))

        # ====== Payment screen: Delete / arrows / F10 / F2 / F5 ======
        # delete_payment_line (Shift + Delete)
        key_ids_combo = []
        for xmlid in [
            'sh_pos_all_in_one_retail.sh_keyboard_key_shift',
            'sh_pos_all_in_one_retail.sh_keyboard_key_delete'
        ]:
            kid = self.env.ref(xmlid, raise_if_not_found=False)
            if kid:
                tmp = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': kid.id})
                key_ids_combo.append(tmp.id)
        if key_ids_combo:
            vals.append((0, 0, {
                'sh_shortcut_screen': 'delete_payment_line',
                'sh_shortcut_screen_type': 'payment_screen',
                'sh_key_ids': [(6, 0, key_ids_combo)]
            }))

        # arrows up/down in payment
        for xmlid, action in [
            ('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_up', 'select_up_payment_line'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_down', 'select_down_payment_line'),
        ]:
            kid = self.env.ref(xmlid, raise_if_not_found=False)
            if kid:
                tmp = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': kid.id})
                vals.append((0, 0, {
                    'sh_shortcut_screen': action,
                    'sh_shortcut_screen_type': 'payment_screen',
                    'sh_key_ids': [(6, 0, [tmp.id])]
                }))

        # +10 / +20 / +50
        for xmlid, action in [
            ('sh_pos_all_in_one_retail.sh_keyboard_key_F10', '+10'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_F2', '+20'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_F5', '+50'),
        ]:
            kid = self.env.ref(xmlid, raise_if_not_found=False)
            if kid:
                tmp = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': kid.id})
                vals.append((0, 0, {
                    'sh_shortcut_screen': action,
                    'sh_shortcut_screen_type': 'payment_screen',
                    'sh_key_ids': [(6, 0, [tmp.id])]
                }))

        # ====== Order screen: arrows + enter ======
        for xmlid, action in [
            ('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_up', 'select_up_order'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_arrow_down', 'select_down_order'),
            ('sh_pos_all_in_one_retail.sh_keyboard_key_Enter', 'select_order'),
        ]:
            kid = self.env.ref(xmlid, raise_if_not_found=False)
            if kid:
                tmp = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': kid.id})
                vals.append((0, 0, {
                    'sh_shortcut_screen': action,
                    'sh_shortcut_screen_type': 'order_screen',
                    'sh_key_ids': [(6, 0, [tmp.id])]
                }))

        if vals:
            res.update({'sh_shortcut_keys_screen': vals})

        # إنشاء اختصارات تلقائية لطرق الدفع الموجودة
        payment_vals = []
        payment_methods = self.env['pos.payment.method'].search([])
        if payment_methods:
            for pm in payment_methods:
                if pm.name:
                    # نحاول إيجاد مفتاح بنفس الاسم
                    key_rec = self.env['sh.keyboard.key'].search([('name', '=', pm.name[0])], limit=1)
                    if key_rec:
                        tmp = self.env['sh.keyboard.key.temp'].sudo().create({'sh_key_ids': key_rec.id})
                        payment_vals.append((0, 0, {
                            'payment_method_id': pm.id,
                            'sh_payment_shortcut_screen_type': 'payment_screen',
                            'sh_key_ids': [(6, 0, [tmp.id])]
                        }))

        if payment_vals:
            res.update({'sh_payment_shortcut_keys_screen': payment_vals})

        return res

