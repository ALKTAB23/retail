from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    unit = fields.Many2one(
        'uom.uom',
        related='uom_id',
        string='Unit',
        readonly=True,
        store=False,
        help='Compatibility alias for uom_id.'
    )

    price = fields.Float(
        string='Price',
        related='product_tmpl_id.list_price',
        readonly=False,
        store=False,
        help='Compatibility alias for template list_price.'
    )

    available_item = fields.Boolean(
        string='Available Item',
        related='product_tmpl_id.available_in_pos',
        readonly=False,
        store=False,
        help='Compatibility alias for template available_in_pos.'
    )

    negative_qty_price = fields.Boolean(
        string='Negative Quantity Price',
        default=False,
        help='Compatibility field kept for legacy views.'
    )
