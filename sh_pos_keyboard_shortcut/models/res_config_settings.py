# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
    جسر عرض/تعديل إعدادات اختصارات الـ POS من شاشة إعدادات النظام.
    جميع الحقول هنا related إلى pos_config_id لضمان حفظها على الـ pos.config.
    """
    _inherit = 'res.config.settings'

    pos_sh_enable_shortcut = fields.Boolean(
        string="Enable POS Shortcut Key",
        related='pos_config_id.sh_enable_shortcut',
        readonly=False,
    )

    pos_sh_shortcut_screen = fields.Selection(
        related='pos_config_id.sh_shortcut_screen',
        readonly=False,
    )

    pos_sh_shortcut_screen_type = fields.Selection(
        related='pos_config_id.sh_shortcut_screen_type',
        readonly=False,
    )

    pos_sh_shortcut_keys_screen = fields.One2many(
        'sh.pos.keyboard.shortcut', 'config_id',
        string="POS Shortcut Keys",
        related='pos_config_id.sh_shortcut_keys_screen',
        readonly=False,
    )

    pos_sh_payment_shortcut_keys_screen = fields.One2many(
        'sh.pos.keyboard.shortcut', 'payment_config_id',
        string="POS Payment Method Shortcut Keys",
        related='pos_config_id.sh_payment_shortcut_keys_screen',
        readonly=False,
    )

