from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

load_dotenv()

#Configuración del modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def preprocess_text(text):
  """Limpia el texto eliminando espacios extras y limitando longitud"""
  text = text.strip()  # Limpiar espacios extras
  text = text[:500]  # Limitar longitud a 500 caracteres
  return text

# Convertir en runnable
preprocessor = RunnableLambda(preprocess_text)

def generate_summary(text):
  """Generar un resumen conciso del texto manteniendo el sentimiento original"""
  prompt = f"Resume en una sola oración: {text}"
  response = llm.invoke(prompt)
  return response.content

def analyze_sentiment(text):
  """Analiza el sentimiento y devuelve el resultado estructurado"""
  prompt = f"""Analiza el sentimiento del siguiente texto.
  Responde ÚNICAMENTE en formato JSON válido:
  {{"sentimiento": "positivo |negativo|neutro", "razon": "justificación breve"}}

  Texto: {text}"""

  response = llm.invoke(prompt)
  try:
    return json.loads(response.content)
  except json.JSONDecodeError:
    return {"sentimiento": "neutro", "razon": "Error en análisis"}
  
def merge_results(data):
  """Combina los resultados de ambas ramas en un formato unificado"""
  return {
    "resumen": data["resumen"],
    "sentimiento": data["sentimiento_data"]["sentimiento"],
    "razon": data["sentimiento_data"]["razon"],
  }

# Coordinar el análisis completo (resumen + sentimiento)
def process_one(t):
  resumen = generate_summary(t) # Llamada 1 al LLM
  sentimiento_data = analyze_sentiment(t) # Llamada 2 al LLM
  return merge_results({
    "resumen": resumen,
    "sentimiento_data": sentimiento_data
  })

process = RunnableLambda(process_one)

# Construir la cadena de llamadas
chain = preprocessor | process

# Prueba con diferentes textos
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]
 
for texto in textos_prueba:
    resultado = chain.invoke(texto)
    print(f"Texto: {texto}")
    print(f"Resultado: {resultado}")
    print("-" * 50)

