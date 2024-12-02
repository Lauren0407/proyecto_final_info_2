# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
class BaseDatos:
    def __init__(self):
        self.__credenciales = {
            "Paciente": {"Usuario": "paciente_user", "Contraseña": "abc123"},
            "Medico": {"Usuario": "medico_user", "Contraseña": "def456"},
            "Estudiante": {"Usuario": "estudiante_user", "Contraseña": "ghi789"}
        }
        self.__cedulas = set()
        self.__usuarios = {
                "Paciente": [],
                "Medico": [],
                "Estudiante": []
            }

    def obtener_credenciales(self, cargo):
        return self.__credenciales.get(cargo, None)

    def validar_usuario(self, usu, contra,cargo):
        credenciales = self.__credenciales.get(cargo)
        if credenciales:
            return credenciales["Usuario"] == usu and credenciales["Contraseña"] == contra
        return False
    def validar_cedula(self, cedula):
        if cedula in self.__cedulas:
            return False  
        else:
            self.__cedulas.add(cedula)  
            return True
    def agregar_usuario(self,cedula,nombre, cargo):
        if self.validar_cedula(cedula):
            credenciales = self.__credenciales.get(cargo)
            usuario = {
                "Nombre": nombre,
                "Cedula": cedula,
                "Usuario": credenciales["Usuario"],
                "Contraseña": credenciales["Contraseña"]
            }
            self.__usuarios[cargo].append(usuario)
            print("Usuario agregado exitosamente.")
            return usuario 
        else:
            print("La cédula ya existe.")
            return None
class Medico:
    def __init__(self, nombre, especialidad):
        self.__nombre = nombre
        self.__especialidad = especialidad
        self.__pacientes = []
    def agregar_paciente(self, cedula, nombre):
        for p in self.__pacientes:
            if p["cedula"] == cedula:
                print(f"El paciente con cédula {cedula} ya está registrado.")
                return
            self.__pacientes.append({"cedula": cedula, "nombre": nombre, "examenes": []})
            print(f"Paciente {nombre} (Cédula: {cedula}) agregado con éxito al médico {self.__nombre}.")

    def eliminar_paciente(self, cedula):
        for p in self.__pacientes:
            if p["cedula"] == cedula:
                self.__pacientes.remove(p)
                print(f"Paciente con cédula {cedula} eliminado con éxito.")
                return
        print(f"Paciente con cédula {cedula} no encontrado en la lista.")

    def agregar_examen(self, cedula, examen):
        for p in self.__pacientes:
            if p["cedula"] == cedula:
                p["examenes"].append(examen)
                print(f"Examen '{examen}' agregado para el paciente con cédula {cedula}.")
                return
        print(f"Paciente con cédula {cedula} no encontrado.")

    def ver_examenes(self, cedula):
        for p in self.__pacientes:
            if p["cedula"] == cedula:
                return p["examenes"]
        print(f"Paciente con cédula {cedula} no encontrado.")
        return None

    def actualizar_examen(self, cedula, examen_actual, examen_nuevo):
        for p in self.__pacientes:
            if p["cedula"] == cedula:
                if examen_actual in p["examenes"]:
                    p["examenes"].remove(examen_actual)
                    p["examenes"].append(examen_nuevo)
                    print(f"Examen '{examen_actual}' actualizado a '{examen_nuevo}' para el paciente con cédula {cedula}.")
                    return
                print(f"Examen '{examen_actual}' no encontrado para el paciente con cédula {cedula}.")
                return
        print(f"Paciente con cédula {cedula} no encontrado.")

class Paciente:
    def __init__(self, examen):
        self.__examen_paciente = examen

    def ver_examen(self):
        return self.__examen_paciente
    
class Estudiante: 
    def __init__(self):
        self.__especialidades = {
            "Cardiología": {
                "examenes": ["Electrocardiograma", "Tomografía cardiaca", "Resonancia magnética cardiaca"],
                "imagenes": ["ecg_cardio.jpg", "tomografia_cardio.jpg", "resonancia_cardio.jpg"]
            },
            "Neurología": {
                "examenes": ["Electroencefalograma", "Sonografía", "Tomografía cerebral"],
                "imagenes": ["electroencefalograma.jpg", "sonografia_neuro.jpg", "tomografia_cerebral.jpg"]
            },
            "Gastroenterología": {
                "examenes": ["Endoscopia digestiva alta", "Ecoendoscopia", "Colonoscopía"],
                "imagenes": ["endoscopia_gastro.jpg", "ecoendoscopia.jpg", "colonoscopia.jpg"]
            },
            "Patología": {
                "examenes": ["Estudio histopatológico", "Estudios Inmunohistoquímicos", "Biopsias"],
                "imagenes": ["histologia_patologia.jpg", "inmunohistoquimica.jpg", "biopsia_patologia.jpg"]
            },
            "Ortopedia": {
                "examenes": ["Artrografía", "Ecografía Doppler", "Rayos X"],
                "imagenes": ["artrografia_ortopedia.jpg", "ecografia_doppler.jpg", "rayos_x.jpg"]
            }
        }

    def ver_especialidades(self):
        return list(self.__especialidades.keys())

    def documentos(self, especialidad):
        if especialidad in self.__especialidades:
            return {
                "examenes": self.__especialidades[especialidad]["examenes"],
                "imagenes": self.__especialidades[especialidad]["imagenes"]
            }
        else:
            return f"La especialidad '{especialidad}' no está disponible."

    def imagenes(self, especialidad):
        if especialidad in self.__especialidades:
            return self.__especialidades[especialidad]["imagenes"]
        else:
            return f"La especialidad '{especialidad}' no está disponible."
