# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, exceptions, fields, models, _
import logging
import sys

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.journal'

    type_document = fields.Selection([
        ('01', 'Factura'),
        ('03', 'Boleta'),
        ('07', 'Nota Crédito'),
    ], string='Tipo de Comprobante', default='01')

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()

        control = self.env['account.invoice.control']

        for invoice in self:
            _logger.info('Almacenando para declaracion a sunat ' + str(invoice.id) + " version " + sys.version)
            vals = {
                'invoice_id': invoice.id,
                'state': 'pendiente'
            }
            control.create(vals)

        return res

