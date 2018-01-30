# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, exceptions, fields, models, _


class SaleAdvancePaymentInvFe(models.TransientModel):
    _name = "sale.advance.payment.inv.fe"
    _inherit = 'sale.advance.payment.inv'

    type_document = fields.Selection([
        ('01', 'Factura'),
        ('03', 'Boleta')], readonly=True, index=True, change_default=True, default=01, track_visibility='always')
