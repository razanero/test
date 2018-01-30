# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    type_document = fields.Selection([
            ('01','Factura'),
            ('03','Boleta')
        ], readonly=True, index=True, change_default=True,
        default=01,
        track_visibility='always')