# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class AccountControl(models.Model):
    _name = "account.invoice.control"
    _description = "Invoice Control"

    invoice_id = fields.Integer(help="invoice id.")
    state = fields.Char(string='Estado del envio',
                        help="lista de estados")

    @api.model
    def create(self, vals):
        control = super(AccountControl, self).create(vals)
        return control

    @api.model
    def _declare_sunat(self, frequency='minutes'):
        _logger.info('Ejecutando llamanda  ')
        account_control_list = self.env['account.invoice']
        return account_control_list