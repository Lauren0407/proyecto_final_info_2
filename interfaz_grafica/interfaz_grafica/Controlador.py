from modelo_proyecto import BaseDatos, Medico, Paciente, Estudiante, dicom
from vista1 import VentanaPrincipal, VentanaIngreso,VentanaMedico2, VentanaMedico,VentanaVerMed,VentanaVerPac, VentanaPaciente,VentanaEliminar,VentanaCargar,VentanaActualizar, VentanaEstudiante
import sys
from PyQt5.QtWidgets import QApplication

class Principal:
    def __init__(self):
        # Inicializa la aplicación PyQt
        self.__app = QApplication(sys.argv)
        
      
        # Instancias del modelo
        self.__Base = BaseDatos()
        self.__Med = Medico("Nombre", "Especialidad", self.__Base)
        self.__Pac = Paciente("")
        self.__Es = Estudiante()
        self.__Modelo = dicom(dicom_dir=r"C:\Users\PAULA GARCIA\Desktop\PROYECTO INFORMATICA II\dicom_dir")
        
        self.__VP = VentanaPrincipal()
        self.__VI = VentanaIngreso()
        self.__VM = VentanaMedico()
        self.__VPC= VentanaPaciente()
        self.__VE= VentanaEstudiante()
        self.__VMM= VentanaMedico2()
        self.__VC=VentanaCargar()
        self.__VEE=VentanaEliminar()
        self.__VA=VentanaActualizar()
        self.__VVP= VentanaVerPac()
        self.__VVM= VentanaVerMed()


       
        
        # Instancia del coordinador (controlador)
        self.__mi_controlador = Coordinador(
            self.__VP, self.__Base, self.__Med, self.__Pac, self.__Es, self.__Modelo, self.__VMM, self.__VVM
        )

          
        if self.__mi_controlador is None:
            print("Error: El controlador no está inicializado correctamente.")
        else:
        # Asignar el controlador a las vistas
    
            self.__VP.asignarCoordinador(self.__mi_controlador)
            self.__VI.asignarCoordinador(self.__mi_controlador)
            self.__VM.asignarCoordinador(self.__mi_controlador)
            self.__VPC.asignarCoordinador(self.__mi_controlador)
            self.__VE.asignarCoordinador(self.__mi_controlador)
            
            self.__VC.asignarCoordinador(self.__mi_controlador)
            self.__VEE.asignarCoordinador(self.__mi_controlador)
            self.__VA.asignarCoordinador(self.__mi_controlador)
            self.__VVP.asignarCoordinador(self.__mi_controlador)
            self.__VVM.asignarCoordinador(self.__mi_controlador)
            self.__VMM.asignarCoordinador(self.__mi_controlador)

            
    def main(self):
        # Mostrar la ventana principal y ejecutar la aplicación
        self.__VP.show()
        sys.exit(self.__app.exec_())
        

class Coordinador:
    def __init__(self, vista1, base_datos, Medico, Paciente, Estudiante, dicom, VentanaMedico2,VentanaVerMed):
        print("Controlador inicializado con:", vista1, base_datos, Medico, Paciente, Estudiante, dicom, VentanaMedico2)
        self.__mi_vista = vista1
        self.__mi_base_datos = base_datos
        self.__mi_medico = Medico
        self.__mi_paciente = Paciente
        self.__mi_estudiante = Estudiante
        self.__modelo_dicom = dicom
        self.__VentanaMedico2= VentanaMedico2
        self.__VentanaVer= VentanaVerMed

    def RecibirInfoUsuario(self, cargo, usu, contra):
        # Verificamos credenciales
        if self.__mi_base_datos.validar_usuario(usu, contra, cargo):
            return "Usuario autenticado exitosamente."
        else:
            return "Usuario o contraseña incorrectos."
    

    def AgregarExamen(self, cedula, ruta):
        if self.__mi_medico is None:
            return "Error: El médico no ha sido inicializado."
        self.__mi_medico.agregar_examen(cedula, ruta)
        return f"Examen del paciente identificado con {cedula} agregado correctamente."
 
    def VerExamen(self, cedula):
        if self.__mi_medico is None:
            return "Error: El médico no ha sido inicializado."
    
        # Recuperar exámenes de memoria
        examenes = self.__mi_medico.ver_examenes(cedula)
        if examenes:
            resultado = "Exámenes del paciente:\n"
            for ruta in examenes:
                resultado += f"Ruta: {ruta}\n"
            return resultado, examenes
        else:
            return "No se encontraron exámenes para esta cédula.", None


     
    def formatear_metadatos(self, metadatos):
        # Aquí formateas los metadatos para mostrar en la ventana emergente
        resultado = f"Nombre del paciente: {metadatos['patient_name']}\n"
        resultado += f"Modalidad: {metadatos['modality']}\n"
        resultado += f"Fecha del estudio: {metadatos['study_date']}\n"
        resultado += f"Tamaño de imagen: {metadatos['image_size']}\n"
        resultado += f"Espaciado entre píxeles: {metadatos['pixel_spacing']}\n"
        resultado += f"Ubicación de la rebanada: {metadatos['slice_location']}\n"
        return resultado
        
        
    def ActualizarExamen(self,ced,ruta,ruta_new):
        self.__mi_medico.actualizar_examen(ced,ruta,ruta_new)
        return f"Examen del paciente identificado con {ced} actualizado correctamente"
        
    def VerEspecialidades(self):
        especialidades = self.__mi_estudiante.ver_especialidades()
        return f"Especialidades disponibles: {', '.join(especialidades)}"
 
    def GuardarInfoMedico(self, nombre, especialidad):
        self.__mi_medico = Medico(nombre, especialidad, self.__mi_base_datos)
        return f"Médico {nombre} agregado con especialidad {especialidad}."


    
    def RecibirVer(self, cedula):
        return self.VerExamen(cedula)

class DICOMController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_and_display_metadata(self):
        """Carga y muestra los metadatos de los archivos DICOM."""
        num_files, dicom_files = self.model.load_dicom_files()
        self.view.show_message(f"Archivos encontrados: {num_files} archivos DICOM.")
        if num_files > 0:
            # Tomar el primer archivo como ejemplo
            example_file = dicom_files[0]
            metadata = self.model.get_dicom_metadata(example_file)
            self.view.show_metadata(metadata)
            self.view.display_image(metadata["pixel_array"])


if __name__ == "__main__":
    principal = Principal()
    principal.main()