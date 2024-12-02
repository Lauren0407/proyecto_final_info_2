# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
class BaseDatos:
    def __init__(self):
        self.__credenciales = {
            "paciente": {"Usuario": "paciente_user", "Contraseña": "abc123"},
            "medico": {"Usuario": "medico_user", "Contraseña": "def456"},
            "estudiante": {"Usuario": "estudiante_user", "Contraseña": "ghi789"}
        }

    def obtener_credenciales(self, cargo):
        return self.__credenciales.get(cargo, None)

    def validar_usuario(self, cargo, usu, contra):
        
        credenciales = self.__credenciales.get(cargo)
        if credenciales:
            return credenciales["Usuario"] == usu and credenciales["Contraseña"] == contra
        return False

class Medico:
    def __init__(self, nombre, especialidad):
        self.__nombre = nombre
        self.__especialidad = especialidad
        self.__pacientes = []
    def agregar_paciente(self, paciente):
        self.__pacientes.append({"nombre": paciente, "examenes": []})
        print(f"Paciente {paciente} agregado con éxito al médico {self.__nombre}.")
    def eliminar_paciente(self, paciente):
        for p in self.__pacientes:
            if p["nombre"] == paciente:
                self.__pacientes.remove(p)
                print(f"Paciente {paciente} eliminado con éxito.")
                return
        print(f"Paciente {paciente} no encontrado en la lista.")
    def agregar_examen(self, paciente, examen):
        for p in self.__pacientes:
            if p["nombre"] == paciente:
                p["examenes"].append(examen)
                print(f"Examen '{examen}' agregado para el paciente {paciente}.")
                return
        print(f"Paciente {paciente} no encontrado.")
    def ver_examenes(self, paciente):
        for p in self.pacientes:
            if p["nombre"] == paciente:
                return p["examenes"]
        print(f"Paciente {paciente} no encontrado.")
        return None
    def actualizar_examen(self, paciente, examen_actual, examen_nuevo):
        
        for p in self.pacientes:
            if p["nombre"] == paciente:
                if examen_actual in p["examenes"]:
                    p["examenes"].remove(examen_actual)
                    p["examenes"].append(examen_nuevo)
                    print(f"Examen '{examen_actual}' actualizado a '{examen_nuevo}' para el paciente {paciente}.")
                    return
                print(f"Examen '{examen_actual}' no encontrado para el paciente {paciente}.")
                return
        print(f"Paciente {paciente} no encontrado.")
    def listar_pacientes(self):
        return [p["nombre"] for p in self.__pacientes]
    def __str__(self):
        return f"Dr. {self.nombre} - Especialidad: {self.especialidad}"
    
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



        
    


    
        
        
        
          