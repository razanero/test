# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _
import logging


_logger = logging.getLogger(__name__)

class AccountControl(models.Model):
    _name = "account.invoice.control"
    _description = "Invoice Control"

    sequence = fields.Integer(help="invoice id.")
    state = fields.Char(string='Estado del envio',
        help="lista de estados")




