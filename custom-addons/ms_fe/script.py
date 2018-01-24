# This program prints Hello, world!
import logging
import sys
sys.path.append('/home/odoo/.local/lib/python3.5/site-packages')

import dexml

_logger = logging.getLogger(__name__)

from suds.client import Client
logging.getLogger('suds.client').setLevel(logging.DEBUG)


from dexml import fields
class Person(dexml.Model):
    name = fields.String()
    age = fields.Integer(tagname='age')


p = Person.parse("<Person name='Foo McBar'><age>42</age></Person>")

p = Person(name="Handsome B. Wonderful",age=36)
# print p.render()

from suds.client import Client

from suds.transport.http import HttpAuthenticated
t = HttpAuthenticated(username='MAINSOLUTIONS', password='10455548816')
client = Client(url='http://test3.alignetsac.com/sfewsperu/ws/invoker?wsdl',transport=t)


response = client.service.invoke("""<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
    <SignOnLineCmd declare-sunat='0' declare-direct-sunat='0' publish='1' output='PDF'>
    <parametros/>
    <parameter value='10455548816' name='idEmisor'/>
    <parameter value='01' name='tipoDocumento'/>
    <documento>
        <tipoDocumentoEmisor>6</tipoDocumentoEmisor>
        <numeroDocumentoEmisor>10455548816</numeroDocumentoEmisor>
        <razonSocialEmisor>BIZLINKS SAC</razonSocialEmisor>
        <nombreComercialEmisor>BIZLINKS</nombreComercialEmisor>
        <tipoDocumento>01</tipoDocumento>
        <serieNumero>FBIZ-00000006</serieNumero>
        <fechaEmision>2018-01-07</fechaEmision>
        <ubigeoEmisor>150122</ubigeoEmisor>
        <direccionEmisor>AV. CASIMIRO ULLOA NRO. 333</direccionEmisor>
        <urbanizacion>SAN ANTONIO</urbanizacion>
        <provinciaEmisor>LIMA</provinciaEmisor>
        <departamentoEmisor>LIMA</departamentoEmisor>
        <distritoEmisor>MIRAFLORES</distritoEmisor>
        <paisEmisor>PE</paisEmisor>
        <correoEmisor>-</correoEmisor>
        <tipoDocumentoAdquiriente>6</tipoDocumentoAdquiriente>
        <numeroDocumentoAdquiriente>20100018625</numeroDocumentoAdquiriente>
        <razonSocialAdquiriente>MEDIFARMA S.A.</razonSocialAdquiriente>
        <correoAdquiriente>-</correoAdquiriente>
        <tipoMoneda>PEN</tipoMoneda>
        <totalValorVentaNetoOpGravadas>78055.79</totalValorVentaNetoOpGravadas>
        <totalValorVentaNetoOpNoGravada>0.00</totalValorVentaNetoOpNoGravada>
        <totalValorVentaNetoOpExoneradas>0.00</totalValorVentaNetoOpExoneradas>
        <subTotal>0.00</subTotal>
        <totalIgv>14050.03</totalIgv>
        <totalDescuentos>0.00</totalDescuentos>
        <totalVenta>92105.82</totalVenta>
        <inHabilitado>1</inHabilitado>
        <codigoLeyenda_1>1000</codigoLeyenda_1>
        <textoLeyenda_1>NOVENTA Y DOS MIL CIENTO CINCO SOLES CON OCHENTA Y DOS CENTIMOS</textoLeyenda_1>
        <item>
            <indicador>D</indicador>
            <numeroOrdenItem>1</numeroOrdenItem>
            <codigoProducto>3742107600</codigoProducto>
            <descripcion>RODAJE DE BOLAS</descripcion>
            <cantidad>10.00</cantidad>
            <unidadMedida>NIU</unidadMedida>
            <importeUnitarioSinImpuesto>7803.30</importeUnitarioSinImpuesto>
            <importeUnitarioConImpuesto>9207.89</importeUnitarioConImpuesto>
            <codigoImporteUnitarioConImpuesto>01</codigoImporteUnitarioConImpuesto>
            <importeTotalSinImpuesto>78033.00</importeTotalSinImpuesto>
            <importeDescuento>0.00</importeDescuento>
            <importeCargo>0.00</importeCargo>
            <codigoRazonExoneracion>10</codigoRazonExoneracion>
            <importeIgv>14045.93</importeIgv>
        </item>
    </documento>
</SignOnLineCmd>""")
print (response)