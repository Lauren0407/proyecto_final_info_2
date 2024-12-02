from modelo_proyecto import BaseDatos,Medicos,Paciente,Estudiante
from vista1 import VentanaPrincipal,VentanaIngreso,VentanaRegistro,VentanaPaciente,VentanaMedico,VentanaEstudiante
import sys
from PyQt5.Qwidgets import QApplication

#RecibirInfoUsuario(usuario, contraseña,cargo)  imprime si el usuario es válido o no -Agregarusuario(cédula, nombre, cargo)
#agrega la cédula y el nombre, dependiendo el cargo imprime el usuario y contraseña necesarios para ingresar.

class Principal(object):
    def __init__(self):
        self.__app=QApplication()
        self.__Base=BaseDatos()
        self.__Med= Medicos()
        self.__Pac= Paciente()
        self.__Es= Estudiante()
        self.__VP= VentanaPrincipal()
        self.__VI= VentanaIngreso()
        self.__VR= VentanaRegistro()
        self.__VPC= VentanaPaciente()
        self.__VM= VentanaMedico()
        self.__VE= VentanaEstudiante()
        
        # El controlador conecta el modelo y la vista
        self.__mi_controlador = Coordinador(self.__VP, self.__Base, self.__Med, self.__Pac, self.__Es)
        self.__VP.asignarCoordinador(self.__mi_controlador)

    def main(self):
        self.__VP.show()
        sys.exit(self.__app.exec_())


class Coordinador:
   
   def __init__(self, vista1, modelo_proyecto, base_datos, medico, estudiante, paciente):
    # Aquí se asignan las instancias de las clases correspondientes
    self.__mi_vista = vista1
    self.__mi_modelo = modelo_proyecto
    self.__mi_base_datos = base_datos  # Instancia de BaseDatos
    self.__mi_medico = medico  # Instancia de Medico
    self.__mi_estudiante = estudiante  # Instancia de Estudiante
    self.__mi_paciente = paciente  # Instancia de Paciente


   def RecibirInfoUsuario(self,cargo,usu,contra,cedula,nombre):
        #verificamos que el paciente no exista 
        if self.__mi_base_datos.validar_usuario(cargo,usu,contra)==True:
            return "ya el usuario existe"
        else:
            return "Usuario incorrecto"
    
    def AgregarUsuario(self, cedula, nombre, cargo):
        if self.__mi_base_datos.validar_usuario(cargo,nombre):
            return f"El usuario con cédula {cedula} ya existe."
        else:
            self.__mi_base_datos.agregar_usuario(cedula, nombre, cargo)
            return "Agregado correctamente"
        
    def AgregarPaciente(self, cedula, nombre):
        self.__mi_medico.agregar_paciente(cedula, nombre)
        return "Agregado correctamente"

    def VerExamen(self, cedula):
        exámenes = self.__mi_medico.ver_examenes(cedula)
        if exámenes:
            return f"Exámenes del paciente con cédula {cedula}: {', '.join(exámenes)}"
        return f"No se encontraron exámenes para el paciente con cédula {cedula}."

    def VerEspecialidades(self):
        especialidades = self.__mi_estudiante.ver_especialidades()
        return f"Especialidades disponibles: {', '.join(especialidades)}"

    def GuardarInfoMedico(self, nombre, especialidad):
        self.__mi_medico.agregar_medico(nombre, especialidad)
        return f"Médico {nombre} agregado con especialidad {especialidad}."


if __name__ == "__main__":
    principal = Principal()
    principal.main()

