import ollama
from data.init_db import PensumLoaderFactory
from scripts.utils.configuration import get_actual_file_to_load
import json

File_to_load = get_actual_file_to_load("PENSUM-Ingenieria-de-Datos-e-Inteligencia-Organizacional_updated.csv", "/home/oa/projects/uni/data")
loader = PensumLoaderFactory().get_loader('unicaribe', File_to_load)
df = loader.df
summary = loader.completed_summary()





llama_context = {
    'summary_data' : {

    't_sub' : f"{summary['total']} materias",
    'c_sub' : f"{summary['completed']} materias completadas",
    'm_sub' : f"{summary['missing']} materias pendientes",
    'avg' : df['nota'].mean(),
    
    },

    'subject_list' : {df['asignatura'].tolist()},

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
Cada fila representa una asignatura con su respectiva nota, crédito, y fecha de cursado. 
La columna 'completo' indica el estado de la materia:
- Si es 'Pendiente', el estudiante aún no ha cursado esa asignatura.
- Si es 'Completado', significa que ya ha sido aprobada y evaluada.

Debe realizar un análisis profesional, en lenguaje formal. El análisis debe identificar:

1. Estadísticas generales: promedio de nota, cantidad de asignaturas completadas y pendientes, total de créditos aprobados.
2. Riesgos académicos: notas menores a 80 se consideran de riesgo; entre 80 y 89 son rendimiento medio, y de 90 en adelante indican alto rendimiento.
3. Alertas: materias pendientes acumuladas, baja progresión o rendimiento deficiente en áreas específicas.
4. Recomendaciones: posibles rutas óptimas para cursar asignaturas restantes y priorización por riesgo o pre-requisitos.
5. Si es posible, identificar patrones o correlaciones entre fechas, tipos de materias y desempeño.
6. Incluir un reporte resumen y otro más detallado con asignaturas clave.

Aquí están los datos del estudiante:

{json.dumps(json_data, ensure_ascii=False, indent=2)} """

response = ollama.chat(
model="llama3",
messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": user_prompt}
]
)

print(response['message']['content'])