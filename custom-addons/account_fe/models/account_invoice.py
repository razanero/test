# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()

        control = self.env['account.invoice.control']

        for invoice in self:
            _logger.info('Almacenando para declaracion a sunat ' + str(invoice.id))
            vals = {
                'invoice_id': invoice.id
            }
            control.create(vals)

        return res
