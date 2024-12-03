# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pydicom
import mysql.connector

class BaseDatos:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="examenes_medicos_db"
        )
        mycursor = self.mydb.cursor()
        sql = "SELECT cargo, usuario, clave FROM usuarios"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        self.__credenciales = {}
        for row in result:
            cargo, usuario, clave = row
            self.__credenciales[cargo] = {"Usuario": usuario, "Contraseña": clave}
        self.__cedulas = set()
        self.__usuarios = {
                "Paciente": [],
                "Medico": [],
                "Estudiante": []
            }

        self.usuarios = {}  # Para guardar usuarios (médicos, pacientes, estudiantes)


    def obtener_examenes(self, cedula):
        """Obtiene los exámenes asociados a una cédula de paciente."""
        sql = "SELECT ruta, fecha FROM examenes WHERE cedula_paciente = %s"
        self.mycursor.execute(sql, (cedula,))
        result = self.mycursor.fetchall()
        
        if result:
            # Devuelve una lista de tuplas (ruta, fecha)
            return [{"ruta": examen[0], "fecha": examen[1]} for examen in result]
        else:
            return None
        
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
class dicom:
    def __init__(self, dicom_dir):
        self.dicom_dir = dicom_dir
        self.dicom_files = []

    def cargar_archivos(self):
        """Carga la lista de archivos DICOM en el directorio especificado."""
        self.dicom_files = [os.path.join(self.dicom_dir, f) for f in os.listdir(self.dicom_dir) if f.endswith('.dcm')]
        return len(self.dicom_files), self.dicom_files
    def obtener_dicom(self, file_path):
        try:
            dataset = pydicom.dcmread(file_path)
            metadata = {
                "patient_name": getattr(dataset.PatientName, 'family_name', 'Desconocido') + 
                            ", " + getattr(dataset.PatientName, 'given_name', 'Desconocido'),
            "modality": getattr(dataset, 'Modality', 'Desconocida'),
            "study_date": getattr(dataset, 'StudyDate', 'Desconocida'),
            "image_size": f"{getattr(dataset, 'Rows', '0')} x {getattr(dataset, 'Columns', '0')}",
            "pixel_spacing": getattr(dataset, 'PixelSpacing', 'N/A'),
            "slice_location": getattr(dataset, 'SliceLocation', '(missing)'),
            "pixel_array": getattr(dataset, 'pixel_array', None)
            }
            return metadata
    
        except Exception as e:
            print(f"Error al leer archivo DICOM {file_path}: {e}")
            return None
class Medico:
    def __init__(self, cedula, especialidad,base_datos):
        self.__cedula = cedula
        self.__especialidad = especialidad
        self.__pacientes = []
        self.__mi_base_datos = base_datos
        self.examenes = {}
        
    
         
    def asignarCoordinador(self, coordinador):
        
        self.__mi_controlador = coordinador
        
    def agregar_examen(self, cedula, examen):
        if cedula not in self.examenes:
            self.examenes[cedula] = []
        self.examenes[cedula].append(examen)

    def eliminar_examen(self, cedula, ruta):
        for p in self.__pacientes:
            if p["cedula"] == cedula:
                self.__pacientes.remove(p)
                print(f"Paciente con cédula {cedula} eliminado con éxito.")
                return
        print(f"Paciente con cédula {cedula} no encontrado en la lista.")


    def ver_examenes(self, cedula):
        examenes = self.__mi_base_datos.obtener_examenes(cedula)
        if examenes:
            return examenes
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
            "Nuemología": {
                "examenes": ["Espirometría", "Volúmenes pulmonares", "Test de metacolina"],
                "imagenes": ["espirometria.jpg", "vol_pulmonar.jpg", "metacolina.jpg"]
            },
            "Infectología": {
                "examenes": ["PCR", "Cultivo microbiologico", "Hemograma completo"],
                "imagenes": ["pcr.jpg", "cultivo.jpg", "hemograma.jpg"]
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
