# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, exceptions, fields, models, _


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    _columns = {
        'type_document' : fields.Selection([
        ('01', 'Factura'),
        ('03', 'Boleta')], default=01, required=True)
    }
