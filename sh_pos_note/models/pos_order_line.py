from odoo import fields, models

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    note = fields.Text(string="Note")

