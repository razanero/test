# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, exceptions, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        invoices = super(SaleOrder, self).action_invoice_create()
        return [inv.id for inv in invoices.values()]
