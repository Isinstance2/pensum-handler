import ollama
from data.init_db import PensumLoaderFactory
from scripts.utils.configuration import get_actual_file_to_load
import json

file_name = "PENSUM-Ingenieria-de-Datos-e-Inteligencia-Organizacional_updated.csv"
data_folder = "/home/oa/projects/uni/data"

File_to_load = get_actual_file_to_load(file_name, data_folder )
loader = PensumLoaderFactory().get_loader('unicaribe', File_to_load)
df = loader.df
summary = loader.completed_summary()





llama_context = {
    'summary_data' : {

    't_sub' : f"{summary['total']} materias",
    'c_sub' : f"{summary['completed']} materias completadas",
    'm_sub' : f"{summary['missing']} materias pendientes",
    'avg' : f" Avg : {df['nota'].mean()}",
    
    },

    'student_data' : {

    'data_columns' : df.columns.tolist(),
    'asignatura' : df['asignatura'].tolist(),
    'clave_asignatura' : df['clave'].tolist(),
    'creditos' : df['credito'].tolist(),
    'pre_requisitos' : df['pre_req'].tolist(),
    'mes_cursado' : df['mes_cursado'].tolist(),
    'calificaciones' : df['nota'].tolist(),


    }
}




df = loader.df

# Convertir a JSON
json_data = df.to_dict(orient='records')

# --- Separar system y user ---
system_prompt = """
Eres un analista de datos educativo profesional. 
Tu trabajo consiste en analizar el desempeño académico de estudiantes universitarios con base en datos tabulares. 
Escribe tus respuestas en un lenguaje formal, conciso y profesional. 
Evita saludos, introducciones o preguntas finales.
"""

user_prompt = f"""
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

{json.dumps(llama_context, ensure_ascii=False, indent=2)} """

response = ollama.chat(
model="llama3",
messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": user_prompt}
]
)

print(response['message']['content'])