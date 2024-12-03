# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:46:16 2024

@author: corde
"""
import sys 
from PyQt5.QtWidgets import QApplication,QMainWindow, QDialog, QMessageBox, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox 
from PyQt5.QtGui import QIntValidator, QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit
import matplotlib.pyplot as plt
from modelo_proyecto import dicom
import numpy as np
import os


class VentanaPrincipal(QDialog):
    def __init__(self, ppal=None):      
        super(VentanaPrincipal, self).__init__()
        loadUi('Interfaz grafica.ui', self)
        self.setup()

    def setup(self):
        self.boton_ingresar.clicked.connect(self.abrir_ventana_ingreso)
        self.boton_cancelar.clicked.connect(self.opc_cancelar)
    def opc_cancelar(self):
        self.close()
    
    def asignarCoordinador(self, coordinador):
        self.__mi_controlador = coordinador

    def abrir_ventana_ingreso(self):
        ventana_ingreso = VentanaIngreso(self)
        ventana_ingreso.asignarCoordinador(self.__mi_controlador)
        self.hide()
        ventana_ingreso.show()

    def recibir_ingreso(self,u,co,cg):
        resultado=self.__mi_controlador.RecibirInfoUsuario(u,co,cg)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()

    def recibir_medico(self,n,esp):
        resultado=self.__mi_controlador.GuardarInfoMedico(n,esp)
        return resultado
        
        
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
                ventana = VentanaMedico(self.__mi_ventana_padre)
            elif cargo == "Estudiante":
                ventana = VentanaEstudiante(self.__mi_ventana_padre)

            ventana.asignarCoordinador(self.__mi_controlador)
            ventana.show()
            self.hide()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText(resultado)
            msg.setWindowTitle("Resultado de la operación")
            msg.exec_()
            
            self.ced_ing.clear()
            self.usu_ing.clear()
            self.show()

class VentanaMedico(QDialog):
    def __init__(self, ppal=None,controlador=None):
        super(VentanaMedico, self).__init__(ppal)
        loadUi('medico.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
        self.__mi_controlador=controlador
    
    def asignarCoordinador(self, coordinador):
         self.__mi_controlador = coordinador   
        
    def setup(self):
        soloEntero = QIntValidator()
        self.nom_meding.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.nom_meding.text()
        especialidad=self.espe_med.currentText()
        mensaje = self.__mi_ventana_padre.recibir_medico(ced,especialidad)
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(mensaje)
        msg.setWindowTitle("Resultado de la operación")
        msg.exec_()
        
        ventana = VentanaMedico2(self)
        ventana.asignarCoordinador(self.__mi_controlador)
        ventana.show()
        self.hide()
        print('Final guardar info')
    
class DICOMView:
    def show_message(self, message):
        """Muestra mensajes generales al usuario."""
        print(message)
    def show_metadata(self, metadata):
        """Muestra los metadatos del archivo DICOM."""
        print("\n--- Metadatos del Archivo DICOM ---")
        for key, value in metadata.items():
            if key != "pixel_array": 
                print(f"{key.replace('_', ' ').capitalize()}: {value}")

    def display_image(self, pixel_array):
        """Muestra la imagen del archivo DICOM."""
        plt.imshow(pixel_array, cmap=plt.cm.bone)
        plt.title("Imagen DICOM")
        plt.axis('off')
        plt.show()

class VentanaPaciente(QDialog):
    def __init__(self, ppal=None):
        super(VentanaPaciente, self).__init__(ppal)
        loadUi('paciente.ui', self)
        self.setup()
        self.__mi_ventana_padre = ppal
    def recibir_paciente(self,ced):
            if self.__mi_controlador is not None:
                print(f"Controlador activo en VentanaPaciente: {self.__mi_controlador}")
                resultado = self.__mi_controlador.VerExamen(ced)
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setInformativeText(resultado)
                msg.setWindowTitle("Resultado de la operación")
                msg.exec_()
            else:
                print("Error: El controlador no está inicializado en VentanaPaciente.")  
        
    def asignarCoordinador(self, coordinador):
        self.__mi_controlador = coordinador
    
    def setup(self):
        self.ver_examen.clicked.connect(self.abrir_ver)  
        self.cancelar.clicked.connect(self.opcion_cancelar)

    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()

    def abrir_ver(self): 
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
        self.__mi_coordinador = coordinador
    def setup(self):
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)

    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        especialidad=self.especialidad.currentText()
        
        if especialidad == "Cardiología":
            ventana = VentanaCardiologia(self)
        elif especialidad == "Neurología":
            ventana = VentanaNeurologia(self)
        elif especialidad == "Gastroenterología":
            ventana = VentanaGastro(self)
        elif especialidad == "Neumología":
            ventana = VentanaNeumo(self)
        elif especialidad == "Infectología":
            ventana = VentanaInfectologia(self)
    
        ventana.show()
        self.hide()
      
class VentanaMedico2(QDialog):
    
    def __init__(self, ppal=None,controlador=None):
        super(VentanaMedico2, self).__init__(ppal)
        loadUi('vent_medico.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
        self.__mi_controlador=controlador    
        self.datos_dicom = None
        self.datos_dicom = self.findChild(QTextEdit, "datos_dicom")
        

        
    def setup(self):
        self.cargar.clicked.connect(self.abrir_ventana_cargar)
        self.eliminar.clicked.connect(self.abrir_ventana_eliminar)
        self.actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.ver.clicked.connect(self.abrir_ventana_ver)
        self.cancelar.clicked.connect(self.opcion_cancelar)
        
    def asignarCoordinador(self, coordinador):
        
        self.__mi_controlador = coordinador
        self.__mi_controlador.VerExamen
     
    def abrir_ventana_ver(self):
        ventana = VentanaVerMed(self, controlador=self.__mi_controlador)
        if self.__mi_controlador is None:
            print("Error: El controlador no fue asignado.")
        self.hide()
        ventana.show()

    def abrir_ventana_cargar(self):
        ventana = VentanaCargar(self, controlador=self.__mi_controlador)
        self.hide()
        ventana.show()
    def abrir_ventana_actualizar(self):
        ventana = VentanaActualizar(self, controlador=self.__mi_controlador)
        self.hide()
        ventana.show()
    def abrir_ventana_eliminar(self):
        ventana = VentanaEliminar(self, controlador=self.__mi_controlador)
        self.hide()
        ventana.show()
    def recibir_Cargar(self, ced, ruta):
        try:
            resultado = self.__mi_controlador.AgregarExamen(ced, ruta)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText(resultado)
            msg.setWindowTitle("Resultado de la operación")
            msg.exec_()

            
            dicom_model = dicom(os.path.dirname(ruta))
            metadata = dicom_model.obtener_dicom(ruta)
            if metadata:
          
                if self.datos_dicom is not None:
                    self.datos_dicom.setText(self.formatear_metadatos(metadata))
                else:
                    print("Error: QLabel o QTextEdit para 'datos_dicom' no está inicializado.")
            else:
                print("Error al cargar los metadatos.")
        except Exception as e:
            print(f"Error al guardar información: {e}")

    def formatear_metadatos(self, metadatos):
    
        resultado = f"Nombre del paciente: {metadatos['patient_name']}\n"
        resultado += f"Modalidad: {metadatos['modality']}\n"
        resultado += f"Fecha del estudio: {metadatos['study_date']}\n"
        resultado += f"Tamaño de imagen: {metadatos['image_size']}\n"
        resultado += f"Espaciado entre píxeles: {metadatos['pixel_spacing']}\n"
        resultado += f"Ubicación de la rebanada: {metadatos['slice_location']}\n"
        return resultado
            
    def abrir_archivo_dicom(self, ruta):
        try:
            ruta = ruta.strip() 
            dicom_model = dicom(os.path.dirname(ruta))  
            _, archivos = dicom_model.cargar_archivos()  
            metadata = dicom_model.obtener_dicom(ruta)  
            
          
            self.metadata_dicom = metadata
            
        
            if self.datos_dicom is not None:
                self.datos_dicom.setText(str(metadata)) 
            else:
                print("Error: QLabel o QTextEdit no inicializado.")
        
            if metadata.get("pixel_array") is not None:
                self.mostrar_imagen(metadata["pixel_array"])
        except Exception as e:
            print(f"Error cargando archivo DICOM: {e}")


    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
        
    def mostrar_imagen(self, pixel_array):
        
        if pixel_array is None:
            print("No hay imagen para mostrar.")
            return

        normalized_array = (pixel_array / pixel_array.max() * 255).astype(np.uint8)
        height, width = normalized_array.shape
        image = QImage(normalized_array.data, width, height, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image)
        self.imagen_dicom.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    
    def recibir_Eliminar(self,ced,ruta):
        resultado=self.__mi_controlador.EliminarExamen(ced,ruta)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
    def recibir_Actualizar(self,ced,ruta,ruta_new):
        resultado=self.__mi_controlador.ActualizarExamen(ced, ruta, ruta_new)
        msg = QMessageBox(self) 
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(resultado)
        msg.setWindowTitle("Resultado de la operacion")
        msg.show()
    def recibir_paciente(self, cedula):
        resultado, examenes= self.__mi_controlador.VerExamen(cedula)
        try:
            if resultado:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Exámenes del paciente")
                msg.setInformativeText(resultado)
                msg.setWindowTitle("Resultado de la operación")
                msg.exec_()
    
                if examenes:
                    primera_ruta = examenes[0]
                    self.abrir_archivo_dicom(primera_ruta)
            else:
                QMessageBox.warning(self, "Sin resultados", "No se encontraron exámenes para esta cédula.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar exámenes: {e}")

class VentanaVerPac(QDialog):
    def __init__(self, ppal=None):
        super(VentanaVerPac, self).__init__(ppal)
        loadUi('paci_ver.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
        
    def asignarCoordinador(self, coordinador):
         self.__mi_controlador= coordinador
    def setup(self):
        soloEntero = QIntValidator()
        self.ced_ing_2.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.ced_ing_2.text()
        if hasattr(self.__mi_ventana_padre, "recibir_paciente"):
            print(f"Llamando a recibir_paciente con controlador: {self.__mi_ventana_padre.__mi_controlador}")
            self.__mi_ventana_padre.recibir_paciente(ced)
        else:
            print("Error: La ventana padre no tiene el método recibir_paciente.")
        self.hide()
        print('Final guardar info')
        
        
class VentanaCardiologia(QDialog):
    def __init__(self, ppal=None):
        super(VentanaCardiologia, self).__init__(ppal)
        loadUi('cardiologia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
      
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        print('Opción Aceptar seleccionada en la Ventana de Cardiología')
        self.__mi_ventana_padre.show()
        self.hide()
        
class VentanaNeurologia(QDialog):
    def __init__(self, ppal=None):
        super(VentanaNeurologia, self).__init__(ppal)
        loadUi('neurologia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
            
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        
    def opcion_aceptar(self):
        print('Opción Aceptar seleccionada en la Ventana de Neurología')
        self.__mi_ventana_padre.show()
        self.hide()
        

class VentanaGastro(QDialog):
    def __init__(self, ppal=None):
        super(VentanaGastro, self).__init__(ppal)
        loadUi('gastro.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        print('Opción Aceptar seleccionada en la Ventana de Gastro')
        self.__mi_ventana_padre.show()
        self.hide()
        
class VentanaNeumo(QDialog):
    def __init__(self, ppal=None):
        super(VentanaNeumo, self).__init__(ppal)
        loadUi('neumologia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        print('Opción Aceptar seleccionada en la Ventana de Patología')
        self.__mi_ventana_padre.show()
        self.hide()
        
class VentanaInfectologia(QDialog):
    def __init__(self, ppal=None):
        super(VentanaInfectologia, self).__init__(ppal)
        loadUi('infectologia.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
    def setup(self):
        
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
 
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
 
    def opcion_aceptar(self):
        print('Opción Aceptar seleccionada en la Ventana de Patología')
        self.__mi_ventana_padre.show()
        self.hide()
        
class VentanaVerMed(QDialog):
    def __init__(self, ppal=None,controlador=None):
        super(VentanaVerMed, self).__init__(ppal)
        loadUi('vent_med_ver.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
        self.__mi_controlador=controlador
        
    def asignarCoordinador(self, coordinador):
        self.__mi_controlador= coordinador
    def setup(self):
        soloEntero = QIntValidator()
        self.ced_ing.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.ced_ing.text()
        self.__mi_ventana_padre.recibir_paciente(ced)
        
        ventana= VentanaMedico2(self)
        ventana.show()
        self.hide();
        print('Final guardar info')
        
class VentanaCargar(QDialog):
    def __init__(self, ppal=None,controlador=None):
        super(VentanaCargar, self).__init__(ppal)
        loadUi('vent_cargar.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
        self.__mi_controlador=controlador
    def asignarCoordinador(self, coordinador):
        self.__mi_controlador= coordinador
    def setup(self):
        soloEntero = QIntValidator()
        self.ced_ing.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.ced_ing.text()
        ruta=self.rut_arch.text()
        try:
            self.__mi_ventana_padre.recibir_Cargar(ced, ruta)
            dicom_model = dicom(os.path.dirname(ruta))
            metadata = dicom_model.obtener_dicom(ruta)
            if metadata:
                print(f"Metadatos cargados: {metadata}")
            else:
                print("Error al cargar los metadatos.")
        except Exception as e:
            print(f"Error al guardar información: {e}")
        
        ventana= VentanaMedico2(self)
        ventana.show()
        self.hide();
        print('Final guardar info')
        
                     
class VentanaActualizar(QDialog):
    def __init__(self, ppal=None,controlador=None):
        super(VentanaActualizar, self).__init__(ppal)
        loadUi('vent_actualizar.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
        self.__mi_controlador=controlador
    def asignarCoordinador(self, coordinador):
        self.__mi_controlador= coordinador
    def setup(self):
        soloEntero = QIntValidator()
        self.ced_ing.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.ced_ing.text()
        ruta=self.rut_arc.text()
        ruta_new=self.rut_new.text()
        self.__mi_ventana_padre.recibir_Actualizar(ced,ruta,ruta_new)
        ventana= VentanaMedico2(self)
        ventana.show()
        self.hide();
        print('Final guardar info')
        
    
class VentanaEliminar(QDialog): 
    
    def __init__(self, ppal=None,controlador=None):
        super(VentanaEliminar, self).__init__(ppal)
        loadUi('ven_eliminar.ui', self)
        self.setup()
        self.__mi_ventana_padre=ppal
        self.__mi_controlador=controlador
    
    def asignarCoordinador(self, coordinador):
        self.__mi_controlador= coordinador
    
    def setup(self):
        soloEntero = QIntValidator()
        self.ced_ing.setValidator(soloEntero)
        self.buttonBox.accepted.connect(self.guardarInfo)
        self.buttonBox.rejected.connect(self.opcion_cancelar)
    def opcion_cancelar(self):
        self.__mi_ventana_padre.show()
        self.hide()
    def guardarInfo(self):
        ced=self.ced_ing.text()
        ruta=self.rut_elim.text()
        self.__mi_ventana_padre.recibir_Eliminar(ced,ruta)
        ventana= VentanaMedico2(self)
        ventana.show()
        self.hide();
        print('Final guardar info')
        