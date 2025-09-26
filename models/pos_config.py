# your_module/models/pos_config.py
from odoo import fields, models, api

class PosConfig(models.Model):
    _inherit = 'pos.config'
    sh_enable_multi_barcode = fields.Boolean(string="Enable Multi Barcode")

    # ---- Retail core (أمثلة شائعة من v16) ----
    enable_product_suggestion = fields.Boolean(string='Enable Product Suggestion')
    enable_refund = fields.Boolean(string='Enable Refund Helper')
    enable_info = fields.Boolean(string='Enable Info Helper')
    enable_note = fields.Boolean(string='Enable Note on Order Lines')
    enable_change_uom = fields.Boolean(string='Enable Change UoM on POS')
    enable_quick_order = fields.Boolean(string='Enable Quick Order Buttons')
    enable_show_order = fields.Boolean(string='Show Order on Screen')
    enable_auto_pro_uom = fields.Boolean(string='Auto Product UoM')
    enable_variant_popup = fields.Boolean(string='Variant Popup')

    enable_product_bundle = fields.Boolean(string='Enable Product Bundle')

    sh_enable_auto_lock = fields.Boolean(string='Enable POS Auto Lock')
    sh_lock_timer = fields.Integer(string='Auto Lock Timer (sec)', default=60)

    sh_pos_bag_charges = fields.Boolean(string='Enable Bag Charges')
    sh_carry_bag_category = fields.Many2one('product.category', string='Carry Bag Category')

    enable_pos_item_counter = fields.Boolean(string='Enable Total Item Counter')
    enable_pos_qty_counter = fields.Boolean(string='Enable Total Qty Counter')
    enable_pos_item_report = fields.Boolean(string='Enable Quick Item Report')
    enable_pos_qty_report = fields.Boolean(string='Enable Quick Qty Report')

    sh_enable_default_customer = fields.Boolean(string='Enable Default Customer')
    sh_default_customer_id = fields.Many2one('res.partner', string='Default Customer')

    sh_enable_default_invoice = fields.Boolean(string='Enable Default Invoice')

    sh_enable_multi_barcode = fields.Boolean(string='Enable Multi Barcode')

    enable_weight = fields.Boolean(string='Enable Product Weight')
    enable_volume = fields.Boolean(string='Enable Product Volume')
    product_weight_receipt = fields.Boolean(string='Print Weight on Receipt')
    product_volume_receipt = fields.Boolean(string='Print Volume on Receipt')

    sh_apply_custom_discount = fields.Boolean(string='Enable Custom Discount')
    sh_apply_both_discount = fields.Boolean(string='Allow Both Discounts')
    sh_discount_code = fields.Char(string='Discount Code')

    sh_remove_all_item = fields.Boolean(string='Enable Remove All Items')
    sh_remove_single_item = fields.Boolean(string='Enable Remove Single Item')

    # ---- حقلان توافقيان (من رسالتك) ----
    payment_method_id = fields.Many2one(
        'pos.payment.method',
        string='Default Payment Method',
        help='Compatibility field for legacy views; mirrors a POS payment method.',
    )

    sh_payment_shortcut_screen_type = fields.Selection(
        selection=[('payment_screen', 'Payment Screen'), ('pos_screen', 'POS Screen')],
        string='Payment Shortcut Screen',
        default='payment_screen',
        help='Compatibility field expected by legacy POS views.',
    )

    @api.onchange('payment_method_id')
    def _onchange_payment_method_id(self):
        """إذا اختيرت طريقة دفع افتراضية، تأكد أنها ضمن payment_method_ids."""
        for rec in self:
            if rec.payment_method_id:
                # field payment_method_ids يأتي من Odoo core (M2M على pos.config)
                ids = set(rec.payment_method_ids.ids)
                ids.add(rec.payment_method_id.id)
                rec.payment_method_ids = [(6, 0, list(ids))]




    # Added from Odoo 16 for Retail Configuration
    pos_cancel_delivery = fields.Boolean(string="Cancel Delivery Order")
    pos_cancel_invoice = fields.Boolean(string="Cancel Invoice")
    pos_operation_type = fields.Selection([('cancel_draft', 'Cancel and Reset to Draft'), ('cancel_delete', 'Cancel and Delete'), ('cancel_credit_note', 'Cancel with Credit Note')], string='Operation Type', default='cancel_draft')
    pos_display_uom_in_receipt = fields.Boolean(string="Display UoM in Receipt")
    pos_enable_create_pos_product = fields.Boolean(string="Enable Create Product from POS")
    pos_enable_history_on_client_detail = fields.Boolean(string="Enable History on Client Detail")
    pos_enable_order_note = fields.Boolean(string="Enable Order Note")
    pos_enable_orderline_note = fields.Boolean(string="Enable Orderline Note")
    pos_display_order_note_payment = fields.Boolean(string="Display Order Note on Payment Screen")
    pos_display_order_note_receipt = fields.Boolean(string="Display Order Note in Receipt")
    pos_display_orderline_note_receipt = fields.Boolean(string="Display Orderline Note in Receipt")
    pos_hide_extra_note_checkbox = fields.Boolean(string="Hide Extra Note Checkbox")
    pos_enable_price_to_display = fields.Boolean(string="Enable Price to Display")
    pos_select_uom_type = fields.Selection([('primary', 'Primary'), ('secondary', 'Secondary')], string='Select UoM Type', default='primary')
    pos_enable_product_suggestion = fields.Boolean(string="Enable Product Suggestion")
    pos_enable_volume = fields.Boolean(string="Enable Volume")
    pos_enable_weight = fields.Boolean(string="Enable Weight")
    pos_product_volume_receipt = fields.Boolean(string="Product Volume in Receipt")
    pos_product_weight_receipt = fields.Boolean(string="Product Weight in Receipt")
    pos_enable_whatsapp = fields.Boolean(string="Enable WhatsApp Integration")
    pos_receipt_logo = fields.Binary(string="Receipt Logo")
    pos_round_product_id = fields.Many2one('product.product', string="Rounding Product")
    pos_rounding_type = fields.Selection([('fifty', 'Fifty'), ('ten', 'Ten')], string='Rounding Type', default='fifty')
    pos_select_order_state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string='Select Order State', default='draft')
    pos_select_purchase_state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string='Select Purchase State', default='draft')
    pos_sh_allow_global_discount = fields.Boolean(string="Allow Global Discount")
    pos_sh_allow_order_line_discount = fields.Boolean(string="Allow Order Line Discount")
    pos_sh_carry_bag_category = fields.Many2one('product.category', string="Carry Bag Category")
    pos_sh_close_popup_after_single_selection = fields.Boolean(string="Close Popup After Single Selection")
    pos_sh_customer_discount = fields.Char(string="Default POS Discount")
    pos_sh_customer_order_history = fields.Boolean(string="Customer Order History")
    pos_sh_day_wise_option = fields.Selection([('today', 'Today'), ('yesterday', 'Yesterday'), ('all', 'All')], string='Day Wise Option', default='today')
    pos_sh_default_customer_id = fields.Many2one('res.partner', string="Default Customer")
    pos_sh_dispaly_purchase_btn = fields.Boolean(string="Display Purchase Button")
    pos_sh_display_by = fields.Selection([('available_qty', 'Available Qty'), ('forecasted_qty', 'Forecasted Qty')], string='Display By', default='available_qty')
    pos_sh_display_date = fields.Boolean(string="Display Date in Receipt")
    pos_sh_display_name = fields.Boolean(string="Display Name in Receipt")
    pos_sh_display_sale_btn = fields.Boolean(string="Display Sale Button")
    pos_sh_display_signature = fields.Boolean(string="Display Signature in Receipt")
    pos_sh_display_signature_detail = fields.Boolean(string="Display Signature Detail in Receipt")
    pos_sh_display_stock = fields.Boolean(string="Display Stock")
    pos_sh_enable_auto_lock = fields.Boolean(string="Enable Auto Lock")
    pos_sh_enable_cash_in_out_statement = fields.Boolean(string="Enable Cash In/Out Statement")
    pos_sh_enable_customer_discount = fields.Boolean(string="Enable Customer Discount")
    pos_sh_enable_date = fields.Boolean(string="Allow Date with Signature")
    pos_sh_enable_default_customer = fields.Boolean(string="Enable Default Customer")
    pos_sh_enable_default_invoice = fields.Boolean(string="Enable Default Invoice")
    pos_sh_enable_internal_ref = fields.Boolean(string="Display Internal Reference")
    pos_sh_enable_multi_barcode = fields.Boolean(string="Enable Multi Barcode")
    pos_sh_enable_name = fields.Boolean(string="Allow Name with Signature")
    pos_sh_enable_order_list = fields.Boolean(string="Enable Order List")
    pos_sh_enable_order_reprint = fields.Boolean(string="Enable Order Reprint")
    pos_sh_enable_order_signature = fields.Boolean(string="Allow Signature")
    pos_sh_enable_own_customer = fields.Boolean(string="Enable Own Customer")
    pos_sh_enable_own_product = fields.Boolean(string="Enable Own Product")
    pos_sh_enable_payment = fields.Boolean(string="Enable Payment")
    pos_sh_enable_prduct_code = fields.Boolean(string="Enable Product Code")
    pos_sh_enable_product_code_in_cart = fields.Boolean(string="Enable Product Code in Cart")
    pos_sh_enable_product_code_in_receipt = fields.Boolean(string="Enable Product Code in Receipt")
    pos_sh_enable_product_template = fields.Boolean(string="Enable Product Template")

