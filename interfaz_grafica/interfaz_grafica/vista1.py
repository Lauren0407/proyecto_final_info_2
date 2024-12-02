# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:46:16 2024

@author: corde
"""
import sys 
from PyQt5.QtWidgets import QApplication,QMainWindow, QDialog, QMessageBox, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox 
from PyQt5.QtGui import QIntValidator

#PRUEBA
#holaaa
#hola por 2

class VentanaPrincipal(QDialog):
    def __init__(self, ppal=None): #lazamiento de la ventana
        super(VentanaPrincipal,self).__init__();
        loadUi('Interfaz grafica.ui',self);
        self.setup();
        
    def setup(self):
        self.boton_ingresar.clicked.connect(self.abrir_ventana_ingreso)
        self.boton_registro.clicked.connect(self.abrir_ventana_registro)
        
    def asignarCoordinador(self,coordinador):
        self.__mi_controlador=coordinador
        
    def abrir_ventana_ingreso(self):
        ventana_ingreso= VentanaIngreso(self)
        self.hide()
        ventana_ingreso.show()
    def abrir_ventana_registro(self):
        ventana_agregar= VentanaRegistro(self)
        self.hide()
        ventana_agregar.show()
    def recibir_ingreso(self,u,co,cg):
        resultado=self.__mi_controlador.RecibirInfoUsuario(u,co,cg)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
    def recibir_registro(self,c,n,cg):
        resultado=self.__mi_controlador.Agregarusuario(c,n,cg)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
        
        
class VentanaIngreso(QDialog):
    def __init__(self, ppal=None): #lazamiento de la ventana
        super(VentanaIngreso,self).__init__(ppal)
        loadUi('ventana_ingreso.ui',self)
        self.setup()
        self.__mi_ventana_padre=ppal
        
    def setup(self):
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)

    def opcion_cancelar(self):
        self.__mi_ventana_padre.show() 
        self.hide()
    
    def opcion_aceptar(self):
        contra= self.ced_ing.text()
        usuario=self.usu_ing.text()
        cargo = self.boton_cargo.currentText()  
        self.__mi_ventana_padre.recibir_ingreso(usuario,contra,cargo)
        
        if cargo == "paciente":
            ventana = VentanaPaciente(self)
        elif cargo == "medico":
            ventana = VentanaMedico(self)
        elif cargo == "estudiante":
            ventana = VentanaEstudiante(self)
    
        ventana.show()
        self.hide()
        
class VentanaRegistro(QDialog):
    def __init__(self, ppal=None):
        super(VentanaRegistro, self).__init__(ppal)
        loadUi('ventana_registro.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
        soloEntero = QIntValidator()
        self.ced_reg.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
#        
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        cedula= self.ced_reg.text()
        nombre=self.nom_reg.text()
        cargo= self.bot_cargo.currentText()
        self.__mi_ventana_padre.recibir_registro(cedula,nombre,cargo)        
        self.__mi_ventana_padre.show()
        self.hide();
        print('Final guardar info')
        
class VentanaPaciente(QDialog):
    def __init__(self, ppal=None):
        super(VentanaPaciente, self).__init__(ppal)
        loadUi('paciente.ui', self)

class VentanaMedico(QDialog):
    def __init__(self, ppal=None):
        super(VentanaMedico, self).__init__(ppal)
        loadUi('medico.ui', self)

class VentanaEstudiante(QDialog):
    def __init__(self, ppal=None):
        super(VentanaEstudiante, self).__init__(ppal)
        loadUi('estudiante.ui', self)

   
        
