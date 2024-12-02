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

class VentanaPrincipal(QDialog):
    def __init__(self, ppal=None):      
        super(VentanaPrincipal, self).__init__()
        loadUi('Interfaz grafica.ui', self)
        self.setup()

    def setup(self):
        self.boton_ingresar.clicked.connect(self.abrir_ventana_ingreso)
        self.boton_registro.clicked.connect(self.abrir_ventana_registro)

    def asignarCoordinador(self, coordinador):
        self.__mi_controlador = coordinador

    def abrir_ventana_ingreso(self):
        ventana_ingreso = VentanaIngreso(self)
        ventana_ingreso.asignarCoordinador(self.__mi_controlador)  # Pasar controlador
        self.hide()
        ventana_ingreso.show()

    def abrir_ventana_registro(self):
        ventana_agregar = VentanaRegistro(self)
        ventana_agregar.asignarCoordinador(self.__mi_controlador)  # Pasar controlador
        self.hide()
        ventana_agregar.show()

    def recibir_ingreso(self,u,co,cg):
        resultado=self.__mi_controlador.RecibirInfoUsuario(u,co,cg)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
    def recibir_registro(self, c, n, cg):
        resultado = self.__mi_controlador.Agregarusuario(c, n, cg)
        return resultado  # Devuelve solo el mensaje para ser mostrado por guardarInfo


    def recibir_paciente(self,exm):
        resultado=self.__mi_controlador.VerExamen(exm)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
    def recibir_medico(self,n,esp):
        resultado=self.__mi_controlador.GuardarInfoMedico(n,esp)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
    def recibir_verpaci(self,ced):
        resultado=self.__mi_controlador.RecibirVer(ced)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
        
        
class VentanaIngreso(QDialog):
    def __init__(self, ppal=None):
        super(VentanaIngreso, self).__init__(ppal)
        loadUi('ventana_ingreso.ui', self)
        self.setup()
        self.__mi_ventana_padre = ppal
        


    def setup(self):
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)

    def asignarCoordinador(self, coordinador):
        self.__mi_controlador = coordinador

    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()

    def opcion_aceptar(self):
        contra = self.ced_ing.text()
        usuario = self.usu_ing.text()
        cargo = self.boton_cargo.currentText()
        resultado = self.__mi_controlador.RecibirInfoUsuario(cargo, usuario, contra)

        if "autenticado" in resultado:
            if cargo == "Paciente":
                ventana = VentanaPaciente(self.__mi_ventana_padre)  
            elif cargo == "Medico":
                ventana = VentanaMedico(self)
            elif cargo == "Estudiante":
                ventana = VentanaEstudiante(self)

            ventana.asignarCoordinador(self.__mi_controlador)
            ventana.show()
            self.hide()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText(resultado)
            msg.setWindowTitle("Resultado de la operación")
            msg.exec_()

        
class VentanaRegistro(QDialog):
    def __init__(self, ppal=None):
        super(VentanaRegistro, self).__init__(ppal)
        loadUi('ventana_registro.ui', self)
        self.setup()
        self.__mi_ventana_padre = ppal
    def asignarCoordinador(self, coordinador):
        self.coordinador = coordinador

    def setup(self):
        soloEntero = QIntValidator()
        self.ced_reg.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)

    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()

    def guardarInfo(self):
        cedula = self.ced_reg.text()
        nombre = self.nom_reg.text()
        cargo = self.bot_cargo.currentText()

        # Llama a la función del controlador para registrar al usuario
        mensaje = self.__mi_ventana_padre.recibir_registro(cedula, nombre, cargo)

        # Muestra el mensaje con el resultado
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(mensaje)
        msg.setWindowTitle("Resultado de la operación")
        msg.exec_()  # Usa exec_() para bloquear hasta que el usuario cierre el mensaje

        # Vuelve a la ventana principal
        self.__mi_ventana_padre.show()
        self.hide()

class VentanaMedico(QDialog):
    def __init__(self, ppal=None):
        super(VentanaMedico, self).__init__(ppal)
        loadUi('medico.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def asignarCoordinador(self, coordinador):
        self.coordinador = coordinador
    def setup(self):
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        nombre=self.nom_meding.text()
        especialidad=self.espe_ing.text()
        self.__mi_ventana_padre.recibir_medico(nombre,especialidad)
        ventana= VentanaMedico2(self)
        ventana.show()
        self.hide();
        print('Final guardar info')

class VentanaPaciente(QDialog):
    def __init__(self, ppal=None):
        super(VentanaPaciente, self).__init__(ppal)
        loadUi('paciente.ui', self)
        self.setup()
        self.__mi_ventana_padre = ppal
        
    def asignarCoordinador(self, coordinador):
        self.coordinador = coordinador
    
    def setup(self):
        self.ver_examen.clicked.connect(self.abrir_ver)  # Asocia el clic al método abrir_ver
        self.cancelar.clicked.connect(self.opcion_cancelar)

    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()

    def abrir_ver(self):
        cedula = self.ver_examen.text()  
        self.__mi_ventana_padre.recibir_verpaci(cedula)
        
        ventana_ver = VentanaVerPac(self)
        ventana_ver.show()
        self.hide()
        

class VentanaEstudiante(QDialog):
    def __init__(self, ppal=None):
        super(VentanaEstudiante, self).__init__(ppal)
        loadUi('estudiante.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def asignarCoordinador(self, coordinador):
        self.coordinador = coordinador
    def setup(self):
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        especialidad=self.espe_ing.currentText()
        
        if especialidad == "Cardiología":
            ventana = VentanaCardiologia(self)
        elif especialidad == "Neurología":
            ventana = VentanaNeurologia(self)
        elif especialidad == "Gastroenterología":
            ventana = VentanaGastro(self)
        elif especialidad == "Patología":
            ventana = VentanaPatologia(self)
        elif especialidad == "Ortopedia":
            ventana = VentanaOrtopedia(self)
    
        ventana.show()
        self.hide()

        
class VentanaMedico2(QDialog):
    def __init__(self, ppal=None):
        super(VentanaMedico2, self).__init__(ppal)
        loadUi('vent_medico.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
        self.cargar.clicked.connect(self.abrir_ventana_cargar)
        self.eliminar.clicked.connect(self.abrir_ventana_eliminar)
        self.actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.ver.clicked.connect(self.abrir_ventana_ver)
        self.cancelar.clicked.connect(self.opcion_cancelar)
        
    def abrir_ventana_ver(self):
        ventana= VentanaVerMed(self)
        self.hide()
        ventana.show()
    def abrir_ventana_cargar(self):
        ventana= VentanaCargar(self)
        self.hide()
        ventana.show()
    def abrir_ventana_actualizar(self):
        ventana= VentanaActualizar(self)
        self.hide()
        ventana.show()
    def abrir_ventana_eliminar(self):
        ventana= VentanaEliminar(self)
        self.hide()
        ventana.show()
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
        
      
class VentanaVerPac(QDialog):
    def __init__(self, ppal=None):
        super(VentanaVerPac, self).__init__(ppal)
        loadUi('paci_ver.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.ced_ing_2.text()
        self.__mi_ventana_padre.recibir_verpaci(ced)
        
        #ventana= VentanaMedico2(self)
        #ventana.show()
        self.hide();
        print('Final guardar info')
        
class VentanaCardiologia(QDialog):
    def __init__(self, ppal=None):
        super(VentanaCardiologia, self).__init__(ppal)
        loadUi('cardiologia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
            
        # Aquí puedes conectar los botones o realizar otras configuraciones
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        # Aquí puedes poner lo que debe suceder cuando el usuario haga clic en Aceptar
        print('Opción Aceptar seleccionada en la Ventana de Cardiología')
        
class VentanaNeurologia(QDialog):
    def __init__(self, ppal=None):
        super(VentanaNeurologia, self).__init__(ppal)
        loadUi('neurologia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
            
        # Aquí puedes conectar los botones o realizar otras configuraciones
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        # Aquí puedes poner lo que debe suceder cuando el usuario haga clic en Aceptar
        print('Opción Aceptar seleccionada en la Ventana de Neurología')

class VentanaGastro(QDialog):
    def __init__(self, ppal=None):
        super(VentanaGastro, self).__init__(ppal)
        loadUi('gastro.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
            
        # Aquí puedes conectar los botones o realizar otras configuraciones
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        # Aquí puedes poner lo que debe suceder cuando el usuario haga clic en Aceptar
        print('Opción Aceptar seleccionada en la Ventana de Gastro')
        
class VentanaPatologia(QDialog):
    def __init__(self, ppal=None):
        super(VentanaPatologia, self).__init__(ppal)
        loadUi('patologia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
            
        # Aquí puedes conectar los botones o realizar otras configuraciones
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        # Aquí puedes poner lo que debe suceder cuando el usuario haga clic en Aceptar
        print('Opción Aceptar seleccionada en la Ventana de Patología')
        
class VentanaOrtopedia(QDialog):
    def __init__(self, ppal=None):
        super(VentanaOrtopedia, self).__init__(ppal)
        loadUi('ortopedia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
            
        # Aquí puedes conectar los botones o realizar otras configuraciones
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        # Aquí puedes poner lo que debe suceder cuando el usuario haga clic en Aceptar
        print('Opción Aceptar seleccionada en la Ventana de Patología')
        
class VentanaVerMed(QDialog):
    def __init__(self, ppal=None):
        super(VentanaVerMed, self).__init__(ppal)
        loadUi('vent_med_ver.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.ced_ing.text()
        self.__mi_ventana_padre.recibir_verpaci(ced)
        
        #ventana= VentanaMedico2(self)
        #ventana.show()
        self.hide();
        print('Final guardar info')
        
class VentanaCargar(QDialog):
    def __init__(self, ppal=None):
        super(VentanaCargar, self).__init__(ppal)
        loadUi('vent_cargar.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
class VentanaActualizar(QDialog):
     def __init__(self, ppal=None):
         super(VentanaActualizar, self).__init__(ppal)
         loadUi('vent_actualizar.ui', self)
         self.setup()
         self.__mi_ventana_padre=ppal
class VentanaEliminar(QDialog):
      def __init__(self, ppal=None):
          super(VentanaEliminar, self).__init__(ppal)
          loadUi('ven_eliminar.ui', self)
          self.setup()
          self.__mi_ventana_padre=ppal
          
   

        
        

   
        
