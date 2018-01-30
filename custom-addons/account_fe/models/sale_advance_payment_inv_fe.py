# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _

class SaleAdvancePaymentInv(models.TransientModel):
    _name = "sale.advance.payment.inv.fe"
    _inherit = 'sale.advance.payment.inv'

    type_document = fields.Selection([
        ('01', 'Factura'),
        ('03', 'Boleta')], readonly=True, index=True, change_default=True, default=01, track_visibility='always')
