# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, exceptions, fields, models, _
import logging
import sys

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    type_document = fields.Selection([
        ('01', 'Factura'),
        ('03', 'Boleta'),
        ('07', 'Nota Crédito'),
    ], string='Tipo de Comprobante Asociado', default='01', required='True')



