# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # تختار أي نقطة بيع تريد تعديل إعداداتها
    pos_config_id = fields.Many2one('pos.config', string='Point of Sale', required=True)

    # Shortcuts & Payments
    payment_method_id = fields.Many2one('pos.payment.method', related='pos_config_id.payment_method_id', readonly=False)
    sh_payment_shortcut_screen_type = fields.Selection(related='pos_config_id.sh_payment_shortcut_screen_type', readonly=False)

    # Defaults
    sh_enable_default_customer = fields.Boolean(related='pos_config_id.sh_enable_default_customer', readonly=False)
    sh_default_customer_id = fields.Many2one('res.partner', related='pos_config_id.sh_default_customer_id', readonly=False)
    sh_enable_default_invoice = fields.Boolean(related='pos_config_id.sh_enable_default_invoice', readonly=False)

    # Auto Lock
    sh_enable_auto_lock = fields.Boolean(related='pos_config_id.sh_enable_auto_lock', readonly=False)
    sh_lock_timer = fields.Integer(related='pos_config_id.sh_lock_timer', readonly=False)

    # Bag Charges
    sh_pos_bag_charges = fields.Boolean(related='pos_config_id.sh_pos_bag_charges', readonly=False)
    sh_carry_bag_category = fields.Many2one('pos.category', related='pos_config_id.sh_carry_bag_category', readonly=False)

    # Barcode / Weight / Volume
    sh_enable_multi_barcode = fields.Boolean(related='pos_config_id.sh_enable_multi_barcode', readonly=False)
    enable_weight = fields.Boolean(related='pos_config_id.enable_weight', readonly=False)
    product_weight_receipt = fields.Boolean(related='pos_config_id.product_weight_receipt', readonly=False)
    enable_volume = fields.Boolean(related='pos_config_id.enable_volume', readonly=False)
    product_volume_receipt = fields.Boolean(related='pos_config_id.product_volume_receipt', readonly=False)

    # Counters & Quick Reports
    enable_pos_item_counter = fields.Boolean(related='pos_config_id.enable_pos_item_counter', readonly=False)
    enable_pos_item_report = fields.Boolean(related='pos_config_id.enable_pos_item_report', readonly=False)
    enable_pos_qty_counter = fields.Boolean(related='pos_config_id.enable_pos_qty_counter', readonly=False)
    enable_pos_qty_report = fields.Boolean(related='pos_config_id.enable_pos_qty_report', readonly=False)

    # Discounts
    sh_apply_custom_discount = fields.Boolean(related='pos_config_id.sh_apply_custom_discount', readonly=False)
    sh_apply_both_discount = fields.Boolean(related='pos_config_id.sh_apply_both_discount', readonly=False)
    sh_discount_code = fields.Char(related='pos_config_id.sh_discount_code', readonly=False)

    # Cart helpers
    sh_remove_all_item = fields.Boolean(related='pos_config_id.sh_remove_all_item', readonly=False)
    sh_remove_single_item = fields.Boolean(related='pos_config_id.sh_remove_single_item', readonly=False)

    # Product helpers & Bundle
    enable_product_suggestion = fields.Boolean(related='pos_config_id.enable_product_suggestion', readonly=False)
    enable_refund = fields.Boolean(related='pos_config_id.enable_refund', readonly=False)
    enable_info = fields.Boolean(related='pos_config_id.enable_info', readonly=False)
    enable_note = fields.Boolean(related='pos_config_id.enable_note', readonly=False)
    enable_change_uom = fields.Boolean(related='pos_config_id.enable_change_uom', readonly=False)
    enable_quick_order = fields.Boolean(related='pos_config_id.enable_quick_order', readonly=False)
    enable_show_order = fields.Boolean(related='pos_config_id.enable_show_order', readonly=False)
    enable_auto_pro_uom = fields.Boolean(related='pos_config_id.enable_auto_pro_uom', readonly=False)
    enable_variant_popup = fields.Boolean(related='pos_config_id.enable_variant_popup', readonly=False)
    enable_product_bundle = fields.Boolean(related='pos_config_id.enable_product_bundle', readonly=False)

