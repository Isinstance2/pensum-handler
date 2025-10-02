import ollama
import json
from data.init_db import PensumLoaderFactory
from scripts.utils.configuration import load_env
from scripts.utils.configuration import get_actual_file_to_load
import sys
import logging
from sklearn.linear_model import LinearRegression


log = logging.getLogger()
log.setLevel(logging.INFO)

file_handler = logging.FileHandler("llama_model.log", mode='a')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
log.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.__stdout__)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
log.addHandler(console_handler)



class AiCompanion():
    def __init__(self, selected_file):
        try: 
        
            self.selected_file = selected_file
            self.env_path = "/home/os/projects/uni/config/.env"
            self.data_folder = load_env(self.env_path, "DATA_FOLDER")
            self.file_to_load = get_actual_file_to_load(self.selected_file, self.data_folder )
            self.loader = PensumLoaderFactory().get_loader('unicaribe', self.file_to_load)
            self.df = self.loader.df
            self.summary = self.loader.completed_summary()



            self.system_prompt = """
                Eres un analista de datos educativo profesional. 
                Tu trabajo consiste en analizar el desempeño académico de estudiantes universitarios con base en datos tabulares. 
                Escribe tus respuestas en un lenguaje formal, conciso y profesional. 
                Evita saludos, introducciones o preguntas finales.
                """

            self.llama_context = {
                'summary_data' : {

                't_sub' : f"{self.summary['total']} materias",
                'c_sub' : f"{self.summary['completed']} materias completadas",
                'm_sub' : f"{self.summary['missing']} materias pendientes",
                'avg' : f" Avg : {self.df['nota'].mean():.2f}",
                
                },

                'student_data' : {

                'data_columns' : self.df.columns.tolist(),
                'asignatura' : self.df['asignatura'].tolist(),
                'clave_asignatura' : self.df['clave'].tolist(),
                'creditos' : self.df['credito'].tolist(),
                'pre_requisitos' : self.df['pre_req'].tolist(),
                'mes_cursado' : self.df['mes_cursado'].tolist(),
                'calificaciones' : self.df['nota'].tolist(),


                }
            }

            self.user_prompt = f"""
                Este conjunto de datos contiene el historial académico de un estudiante universitario. 
                las calificaciones nan(vacias) , pueden ser ignorados. Son nulos. No digas absolutamente nada acerca de las calificaciones nulas, ignoralas completamente.
                Las materias que son pendientes , ignorlas, no la menciones para absolutamente nada. 
                Debe realizar un análisis profesional, en lenguaje formal que sea de ayuda para el estudiante. segun los datos recibidos.
                LAS MATERIAS PENDIENTES PUEDEN SER IGNARADAS TODO DATO VACIO PUEDE SER IGNORADOS SOLO CONCENTRATE CON LAS QUE NO ESTAN VACIAS. 
                NO ME HABLES DE NADA DE LAS MATERIAS PENDIENTE EN TU ANALISIS. 

                LAS CALIFICACIONES DE 90 PARA ARRIBA SON EXCELENTE DE 80 - 90 BUENAS Y DE 80 PARA ABAJO = QUE TIENE QUE MEJORAR. 
                recuerda... Si una calificacion es por ejemplo 90, entonces es excelente

                Ejemplo del output:

                Análisis del desempeño académico del estudiante:

                La media de calificaciones del estudiante es de x, lo que indica un rendimiento excelente. De las x materias completadas, hay varias que tienen calificaciones superiores a los x, lo que sugiere una capacidad destacada para aprender y dominar los conceptos.

                Entre las materias con calificaciones superiores a los 90, se encuentran "MÉTODO DEL TRABAJO ACADÉMICO" (97.0), "METODOLOGÍA DE LA INVESTIGACIÓN" (98.0) y "ADMINISTRACION I" (94.0). Estas materias pueden ser importantes para el estudiante en términos de desarrollo académico y profesional.

                Es importante destacar que no hay calificaciones nulas ni pendientes en las materias completadas, lo que sugiere un buen compromiso y gestión del tiempo por parte del estudiante.


                Aquí están los datos del estudiante:

                {json.dumps(self.llama_context, ensure_ascii=False, indent=2)}
                """

        except Exception as e:
            logging.error(f"Error initiating assistant {e}")

    def call_assistant(self):
        try:
            logging.debug("Initializing . . .")
            self.response = ollama.chat(
                model="llama3",
                messages=[
                {"role": "system", "content": self.system_prompt.strip()},
                {"role": "user", "content": self.user_prompt.strip()}
                ]
                )
            logging.info("Agent has been initiated.")
            return str(self.response['message']['content'])
        except Exception as e:
            logging.error(f"Couldn't initialize AI agent : {e}")


    








