from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_sh_pos_z_report = fields.Boolean(
        string="POS Z Report",
        implied_group='sh_pos_all_in_one_retail.group_sh_pos_z_report',   # ← صحيح
    )
