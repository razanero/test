# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _
from account_invoice_fe import Documento, Item, SignOnLineCmd, Parameter
from suds.client import Client
from suds.transport.http import HttpAuthenticated

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
                    xml = self.build(invoiceEntity)
                    self.send(xml)

                child._write({'state': 'declarado'})

        return account_control_list

    @api.model
    def build(self, invoice_entity):

        p = SignOnLineCmd(declare_sunat="0", declare_direct_sunat="0", publish=1, output="PDF")

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

        documento.subTotal = invoice_entity.amount_untaxed
        documento.totalIgv = invoice_entity.amount_tax
        documento.totalDescuentos = 0
        documento.totalVenta = invoice_entity.amount_total
        documento.inHabilitado = 1

        documento.codigoLeyenda_1 = "101"
        documento.textoLeyenda_1 = "41545"

        secuencia=0
        totalValorVentaNetoOpGravadas=0
        totalValorVentaNetoOpNoGravada=0
        for line in invoice_entity.invoice_line_ids:
            secuencia=secuencia+1
            item1 = Item()
            item1.indicador = "D"
            item1.numeroOrdenItem = str(secuencia)
            item1.codigoProducto = line.product_id.default_code
            item1.descripcion = line.product_id.name
            item1.cantidad = line.quantity
            item1.unidadMedida = "UM"
            item1.importeUnitarioSinImpuesto = line.price_unit

            impuestoUnitario=0
            codigoImporteUnitarioConImpuesto="02"
            codigoRazonExoneracion="30"
            for impuesto in line.invoice_line_tax_ids:
                impuestoUnitario = impuestoUnitario+ line.price_unit*(impuesto.amount/100)
                codigoImporteUnitarioConImpuesto = "01"
                codigoRazonExoneracion = "10"
                totalValorVentaNetoOpGravadas=totalValorVentaNetoOpGravadas+line.price_subtotal*(impuesto.amount/100)

            if impuestoUnitario==0 :
                totalValorVentaNetoOpNoGravada=totalValorVentaNetoOpNoGravada+line.price_subtotal

            item1.importeUnitarioConImpuesto= line.price_unit+impuestoUnitario
            item1.codigoImporteUnitarioConImpuesto = codigoImporteUnitarioConImpuesto
            item1.importeTotalSinImpuesto = line.price_subtotal
            item1.importeDescuento = 0
            item1.importeCargo = 0
            item1.codigoRazonExoneracion = codigoRazonExoneracion
            item1.importeIgv = impuestoUnitario
            documento.items.append(item1)



        documento.totalValorVentaNetoOpGravadas = totalValorVentaNetoOpGravadas
        documento.totalValorVentaNetoOpNoGravada = totalValorVentaNetoOpNoGravada
        documento.totalValorVentaNetoOpExoneradas = 0

        p.documentos.append(documento)
        _logger.info('Ejecutando llamada  del id ' + p.render(fragment=True))

        return p.render(fragment=True)


    @api.model
    def send(self, xml):
        t = HttpAuthenticated(username='MAINSOLUTIONS', password='10455548816')
        client = Client(url='http://test3.alignetsac.com/sfewsperu/ws/invoker?wsdl', transport=t)
        response = client.service.invoke(xml)
        _logger.info('resultado ' + response)
        return self

