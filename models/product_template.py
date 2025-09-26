# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ---------------- helpers ----------------
    @api.model
    def _suggestion_o2m_fields(self):
        """يرجع أسماء جميع حقول الـ One2many على المنتج التي تشير إلى pos.product.suggestion.line"""
        o2m_names = []
        for name, field in self.env['product.template']._fields.items():
            if isinstance(field, fields.One2many) and field.comodel_name == 'pos.product.suggestion.line':
                o2m_names.append(name)
        return o2m_names

    @api.model
    def _required_keys_for_o2m(self, o2m_name):
        """
        يحدد مفاتيح 'القيمة المطلوبة' لكل O2M اقتراح:
        - يأخذ الحقول M2O التي تشير إلى product.template أو product.product
        - يستثني حقل الربط الأب (inverse_name) حتى لا نعتبره هو المطلوب
        النتيجة: قائمة بأسماء الحقول التي تُمثل 'المنتج المقترَح' فعلاً.
        """
        line_model = self.env['pos.product.suggestion.line']
        line_fields = line_model._fields

        # inverse_name هو حقل الربط الأب (على سطر الاقتراح) المرتبط بالـ O2M على المنتج
        inverse_name = None
        prod_o2m = self.env['product.template']._fields.get(o2m_name)
        if isinstance(prod_o2m, fields.One2many):
            inverse_name = prod_o2m.inverse_name

        candidate_keys = []
        for fname, f in line_fields.items():
            # نأخذ الـ M2O التي تشير إلى منتج أو قالب منتج
            if isinstance(f, fields.Many2one) and f.comodel_name in ('product.template', 'product.product'):
                if fname != inverse_name:  # استثناء الحقل الأب
                    candidate_keys.append(fname)

        # احتياط إذا ما وجدنا شيء
        if not candidate_keys:
            for fallback in ('product_variant_id', 'product_tmpl_id', 'product_id'):
                if fallback in line_fields:
                    candidate_keys.append(fallback)

        return candidate_keys

    @api.model
    def _has_any_required_value(self, vals, keys):
        """True لو أحد الحقول المطلوبة له قيمة."""
        return any(vals.get(k) for k in keys)

    @api.model
    def _clears_required_value(self, vals, keys):
        """
        True لو القيم تُعدّل واحدًا أو أكثر من الحقول المطلوبة وتعيّنها لقيم falsy
        (يعني المستخدم مسح الاختيار).
        """
        touched = False
        for k in keys:
            if k in vals:
                touched = True
                if vals[k]:
                    return False
        return touched

    @api.model
    def _clean_pos_suggestion_commands(self, o2m_name, commands):
        """يحذف السطور الجديدة الفارغة ويحوّل تفريغ القيمة في سطر موجود إلى حذف."""
        if not commands:
            return commands

        required_keys = self._required_keys_for_o2m(o2m_name)
        cleaned = []

        for cmd in commands:
            if not isinstance(cmd, (list, tuple)) or not cmd:
                cleaned.append(cmd)
                continue

            op = cmd[0]

            if op == 0:  # (0, 0, vals)
                vals = (len(cmd) > 2 and cmd[2]) or {}
                if self._has_any_required_value(vals, required_keys):
                    cleaned.append(cmd)
                # غير هذا: سطر جديد بدون منتج مقترَح -> تجاهله
            elif op == 1:  # (1, id, vals)
                rec_id = cmd[1]
                vals = (len(cmd) > 2 and cmd[2]) or {}
                # إذا مسح المستخدم القيمة المطلوبة حوّلها إلى حذف
                if self._clears_required_value(vals, required_keys):
                    cleaned.append((2, rec_id))
                else:
                    cleaned.append(cmd)
            else:
                # باقي العمليات كما هي: (2 delete / 3 unlink / 4 link / 5 clear / 6 set)
                cleaned.append(cmd)

        return cleaned

    # ---------------- overrides ----------------
    @api.model_create_multi
    def create(self, vals_list):
        o2m_names = self._suggestion_o2m_fields()
        if o2m_names:
            for vals in vals_list:
                for o2m in o2m_names:
                    if o2m in vals and isinstance(vals[o2m], list):
                        vals[o2m] = self._clean_pos_suggestion_commands(o2m, vals[o2m])
        return super().create(vals_list)

    def write(self, vals):
        o2m_names = self._suggestion_o2m_fields()
        if o2m_names and isinstance(vals, dict):
            for o2m in o2m_names:
                if o2m in vals and isinstance(vals[o2m], list):
                    vals[o2m] = self._clean_pos_suggestion_commands(o2m, vals[o2m])
        return super().write(vals)

