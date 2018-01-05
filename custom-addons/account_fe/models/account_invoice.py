# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):

        res = super(AccountInvoice, self).action_invoice_open()
        _logger.info('Tax Base Amount not computable probably due to a change in an underlying tax (%s).')

        return res




