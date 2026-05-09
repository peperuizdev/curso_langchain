from langchain_openai import ChatOpenAI
from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts
from dotenv import load_dotenv

load_dotenv()

def crear_evaluador_de_cv():
  """Crea un evaluador de CVs para analizar y evaluar candidatos de manera objetiva, profesional y constructiva."""
  modelo_base = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.2,
  )
  
  modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
  chat_prompt = crear_sistema_prompts()

  cadena_evaluación = chat_prompt | modelo_estructurado

  return cadena_evaluación

def evaluar_candidato(texto_cv: str, descripcion_puesto: str):
  """Evalua un candidato de manera objetiva, profesional y constructiva."""
  try:
    cadena_evaluación = crear_evaluador_de_cv()
    resultado = cadena_evaluación.invoke({
      "texto_cv": texto_cv,
      "descripcion_puesto": descripcion_puesto
    })

    return resultado
  except Exception as e:
    return AnalisisCV(
      nombre_candidato="Error al evaluar el CV",
      experiencia_años=0,
      habilidades_clave=["Error al evaluar el CV"],
      education="No se puede determinar",
      experiencia_relevante="No se puede determinar",
      fortalezas=["Requiere revisión manual del CV"],
      areas_mejora=["Verificar formato y legibilidad del CV"],
      porcentaje_ajuste=0,
    )
  


