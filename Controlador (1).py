from modelo_proyecto import BaseDatos, Medico, Paciente, Estudiante
from vista1 import VentanaPrincipal, VentanaIngreso, VentanaRegistro, VentanaMedico, VentanaPaciente, VentanaEstudiante
import sys
from PyQt5.QtWidgets import QApplication


class Principal:
    def __init__(self):
        # Inicializa la aplicación PyQt
        self.__app = QApplication(sys.argv)

        # Instancias del modelo
        self.__Base = BaseDatos()
        self.__Med = None  # No inicializamos el médico de inmediato
        self.__Pac = None
        self.__Es = None

        self.__VP = VentanaPrincipal()
        self.__VI = VentanaIngreso()
        self.__VR = VentanaRegistro()
        self.__VM = VentanaMedico()
        self.__VPC= VentanaPaciente()
        self.__VE= VentanaEstudiante()

        # Instancia del coordinador (controlador)
        self.__mi_controlador = Coordinador(
           self.__VP, self.__Base, self.__Pac, self.__Med, self.__Es
        )
        # Asignar el controlador a la vista principal
        self.__VP.asignarCoordinador(self.__mi_controlador)

    def main(self):
        # Mostrar la ventana principal y ejecutar la aplicación
        self.__VP.show()
        sys.exit(self.__app.exec_())


class Coordinador:
    def __init__(self, vista1, base_datos, medico, paciente, estudiante):
        self.__mi_vista = vista1
        self.__mi_base_datos = base_datos
        self.__mi_medico = medico
        self.__mi_paciente = paciente
        self.__mi_estudiante = estudiante

    def RecibirInfoUsuario(self, cargo, usu, contra):
        # Verificamos credenciales
        if self.__mi_base_datos.validar_usuario(usu, contra, cargo):
            return "Usuario autenticado exitosamente."
        else:
            return "Usuario o contraseña incorrectos."
    
    def Agregarusuario(self, cedula, nombre, cargo):
        usuario = self.__mi_base_datos.agregar_usuario(cedula, nombre, cargo)
        if usuario:
            return (
                f"Usuario agregado correctamente.\n"
                f"Credenciales:\nUsuario: {usuario['Usuario']}\nContraseña: {usuario['Contraseña']}"
            )
        else:
            return f"El usuario con cédula {cedula} ya existe."

    def AgregarPaciente(self, cedula, nombre):
        self.__mi_medico.agregar_paciente(cedula, nombre)
        return f"Paciente {nombre} agregado correctamente."
 
    def VerExamen(self, cedula):
        if not self.__mi_base_datos.validar_cedula(cedula):
            examenes = self.__mi_base_datos.obtener_examenes(cedula)
            if examenes:
                return f"Exámenes del paciente con cédula {cedula}: {', '.join(examenes)}"
            return f"No se encontraron exámenes para el paciente con cédula {cedula}."
        
    def VerEspecialidades(self):
        especialidades = self.__mi_estudiante.ver_especialidades()
        return f"Especialidades disponibles: {', '.join(especialidades)}"
 
    def GuardarInfoMedico(self, nombre, especialidad):
        self.__mi_medico = Medico(nombre, especialidad, self.__mi_base_datos)  # Pasar la base de datos
        return f"Médico {nombre} agregado con especialidad {especialidad}."

    
    def RecibirVer(self, cedula):
        return self.VerExamen(cedula)



if __name__ == "__main__":
    principal = Principal()
    principal.main()
