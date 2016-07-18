# -*- coding: utf-8 -*-

from openerp import models, fields, api


class InvoiceCurrecyChangeWizard(models.TransientModel):
    _name = "invoice.currency.change.wizard"

    currency_id = fields.Many2one("res.currency")

    @api.multi
    def update_invoice_currency(self):
        active_id = self._context.get("active_id")
        model = self._context.get("active_model")
        inv = self.env[model].browse(active_id)

        if self.currency_id.id != inv.currency_id.id:
            if self.currency_id.id == self.env.user.company_id.currency_id.id:
                for line in inv.invoice_line_ids:
                    line.price_unit = line.price_unit*inv.rate
                inv.currency_id = self.currency_id.id
            else:
                inv.currency_id = self.currency_id.id
                for line in inv.invoice_line_ids:
                   line.price_unit = line.price_unit/inv.rate

        return True