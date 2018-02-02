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
                for invoiceEntity in self.env['account.invoice'].search([('id', '=', child.id)]):
                    self.build(invoiceEntity)

                child._write({'state': 'declarado'})

        return account_control_list

    @api.model
    def build(self, invoiceEntity):
        p = SignOnLineCmd(declare_sunat="0", declare_direct_sunat="0", publish=0, output="PDF")
        p.parametros.append(Parameter(value="10455548816", name="idEmisor"))
        p.parametros.append(Parameter(value="01", name="tipoDocumento"))
        documento = Documento(totalDescuentos=float(4.52))
        documento.tipoDocumentoEmisor = "01"
        documento.numeroDocumentoEmisor = "10413168533"
        documento.razonSocialEmisor = "test"
        documento.nombreComercialEmisor = "dsds"
        documento.tipoDocumento = "01"
        documento.serieNumero = invoiceEntity.number
        documento.fechaEmision = invoiceEntity.date_invoice.strftime("%Y-%m-%d")
        documento.ubigeoEmisor = ""
        documento.direccionEmisor = "2544"
        documento.urbanizacion = "5454"
        documento.provinciaEmisor = "54"
        documento.departamentoEmisor = "5454"
        documento.distritoEmisor = "545"
        documento.paisEmisor = "PE"
        documento.correoEmisor = "DSDSD@DSDS.COM"
        documento.tipoDocumentoAdquiriente = "01"
        documento.numeroDocumentoAdquiriente = "104125444"
        documento.razonSocialAdquiriente = "DSDSD"
        documento.correoAdquiriente = "DSDS@SDSD.CIN"
        documento.tipoMoneda = "PEN"
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
