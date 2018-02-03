# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _
from account_invoice_fe import Documento, Item, SignOnLineCmd, Parameter
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
        _logger.info('Ejecutando job')
        account_control_list = self.env['account.invoice.control'].search([('state', '=', 'pendiente')], order='id ASC')

        if account_control_list:
            for child in account_control_list:
                _logger.info('Ejecutando llamanda  del id ' + str(child.id))
                for invoiceEntity in self.env['account.invoice'].search([('id', '=', child.invoice_id)]):
                    self.build(invoiceEntity)

                child._write({'state': 'declarado'})

        return account_control_list

    @api.model
    def build(self, invoice_entity):

        p = SignOnLineCmd(declare_sunat="0", declare_direct_sunat="0", publish=0, output="PDF")

        emisor_partner = invoice_entity.company_id.partner_id
        p.parametros.append(Parameter(value=emisor_partner.vat, name="idEmisor"))
        p.parametros.append(Parameter(value=invoice_entity.journal_id.type_document, name="tipoDocumento"))

        documento = Documento()
        documento.tipoDocumentoEmisor = "6"
        documento.numeroDocumentoEmisor = emisor_partner.vat
        documento.razonSocialEmisor = emisor_partner.name
        documento.nombreComercialEmisor = emisor_partner.name
        documento.ubigeoEmisor = emisor_partner.zip
        documento.direccionEmisor = emisor_partner.street
        documento.urbanizacion = "-"
        documento.provinciaEmisor = "-"
        documento.departamentoEmisor = "-"
        documento.distritoEmisor = "-"
        documento.paisEmisor = emisor_partner.country_id.code
        documento.correoEmisor = emisor_partner.email

        adquiriente_partner = invoice_entity.commercial_partner_id
        documento.tipoDocumentoAdquiriente = "6"
        documento.numeroDocumentoAdquiriente = adquiriente_partner.vat
        documento.razonSocialAdquiriente = adquiriente_partner.name
        documento.correoAdquiriente = adquiriente_partner.email

        documento.tipoDocumento = invoice_entity.journal_id.type_document
        documento.serieNumero = invoice_entity.number
        documento.fechaEmision = invoice_entity.date_invoice
        documento.tipoMoneda = invoice_entity.currency_id.name
        documento.totalValorVentaNetoOpGravadas = 100
        documento.totalValorVentaNetoOpNoGravada = 200
        documento.totalValorVentaNetoOpExoneradas = 200
        documento.subTotal = 10
        documento.totalIgv = 18
        documento.totalDescuentos = 105
        documento.totalVenta = 100
        documento.inHabilitado = 1
        documento.codigoLeyenda_1 = "101"
        documento.textoLeyenda_1 = "41545"

        item1 = Item()
        item1.indicador = "D"
        item1.numeroOrdenItem = "1"
        item1.codigoProducto = "10"
        item1.descripcion = "100"
        item1.cantidad = 10
        item1.unidadMedida = "UM"
        item1.importeUnitarioSinImpuesto = 100
        item1.importeUnitarioConImpuesto = 100
        item1.codigoImporteUnitarioConImpuesto = "100"
        item1.importeTotalSinImpuesto = 100
        item1.importeDescuento = 100
        item1.importeCargo = 100
        item1.codigoRazonExoneracion = "10"
        item1.importeIgv = 100
        documento.items.append(item1)
        p.documentos.append(documento)
        _logger.info('Ejecutando llamanda  del id ' + p.render(fragment=True))

        return self
