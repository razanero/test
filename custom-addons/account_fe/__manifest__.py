# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Invoice FE',
    'version': '1.0',
    'website': 'http://main-solutions.com',
    'author': 'Main Solutions S.A.C.',
    'category': 'Accounting',
    'sequence': 15,
    'summary': 'Facturación Electronica',
    'description': '',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'data/account_invoice_control_cron.xml',
        'views/sale_make_invoice_advance_views_fe.xml',
    ],
    'application': False,
    "installable": True
}
