'''
Gestion facturacion
'''
from PyQt5 import QtSql,QtWidgets,QtCore

import conexion
import var
import window
class Facturas():
    def buscaCli(self):
        try:
            dni=var.ui.txtDNIFact.text().upper()
            var.ui.txtDNIFact.setText(dni)
            registro=conexion.Conexion.buscaCliFac(dni)
            nombre=registro[0]+", "+registro[1]
            var.ui.lblCliFac.setText(nombre)

        except Exception as error: print("Error buscar cliente en facturas",error)

    def Facturar(self):
        try:
            registro=[]
            dni=var.ui.txtDNIFact.text().upper()
            registro.append(str(dni))
            var.ui.txtDNIFact.setText(dni)
            fechafac=var.ui.txtFechaFac.text()
            registro.append(str(fechafac))
            conexion.Conexion.altaFact(registro)
        except Exception as error: print("Error al facturar",error)

    def CargaCli(self):

        try:
            fila = var.ui.tabClientes.selectedItems()

            if fila:
                row = [dato.text() for dato in fila]
                dni1 = row[0]
                query = QtSql.QSqlQuery()
                query.prepare(
                    'SELECT dni,apellidos,nombre FROM CLIENTES WHERE dni="' + dni1 + '"')
                if query.exec_():
                    while query.next():
                        dni = query.value(0)
                        apellidos = query.value(1)
                        nombre = query.value(2)

                var.ui.txtDNIFact.setText(dni)
                cliente = apellidos + ", " + nombre
                var.ui.lblCliFac.setText(cliente)


        except Exception as error:
            print("Error en modulo CargaCli", error)

    def cargaLineaVenta(self):
        try:
            index = 0
            var.cmbProducto = QtWidgets.QComboBox()
            var.cmbProducto.setFixedSize(180,25)
            conexion.Conexion.cargarCmbproducto()
            var.txtCantidad = QtWidgets.QLineEdit()
            var.txtCantidad.returnPressed.connect(Facturas.totalLineaVenta)
            var.txtCantidad.setFixedSize(70,25)
            var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabClientes.setRowCount(index+1)
            var.ui.tabClientes.setCellWidget(index, 1, var.cmbProducto)
            var.ui.tabClientes.setCellWidget(index,3,var.txtCantidad)


        except Exception as error:
            print("Error en cargar linea venta",error)

    def procesoVenta():
        try:
            row = var.ui.tabClientes.currentRow()
            articulo = var.cmbProducto.currentText()
            dato = conexion.Conexion.obtenerCodPrecio(articulo)
            var.ui.tabClientes.setItem(row,2, QtWidgets.QTableWidgetItem(str(dato[0])+ " €"))
            var.ui.tabClientes.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabClientes.setItem(row, 0, QtWidgets.QTableWidgetItem(str(dato[1])))
            var.ui.tabClientes.item(row, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            var.precio = dato[0].replace('€', '')
            var.precio = dato[0].replace(',', '.')
            var.codpro = dato[1]





        except Exception as error:
            print("Error en proceso venta", error)

    def totalLineaVenta(self = None):
        try:

            venta=[]
            var.precio=float(var.precio)
            row = var.ui.tabClientes.currentRow()
            cantidad1=var.txtCantidad.text()
            cantidad = round(float(cantidad1), 2)
            total_linea =round(var.precio*cantidad, 2)
            total_linea = str(total_linea)+ " €"
            var.ui.tabClientes.setItem(row, 4, QtWidgets.QTableWidgetItem(str(total_linea)))
            var.ui.tabClientes.item(row, 4).setTextAlignment(QtCore.Qt.AlignRight)
            codfac= var.ui.lblnumfac.text()
            venta.append(codfac)
            venta.append(int(var.codpro))
            venta.append(cantidad)
            venta.append(float(var.precio))
            conexion.Conexion.cargarVenta(venta)
            var.txtCantidad.clearFocus()



            # currency para convertir a moneda

        except Exception as error:
            print('Error en producto linea venta', error)