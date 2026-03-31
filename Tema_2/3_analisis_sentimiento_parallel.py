from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

load_dotenv()

#Configuración del modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Preprocesador: limpia espacios y limita a 500 caracteres
def preprocess_text(text):
  """Limpia el texto eliminando espacios extras y limitando longitud"""
  text = text.strip()  # Limpiar espacios extras
  text = text[:500]  # Limitar longitud a 500 caracteres
  return text

# Convertir en runnable
preprocessor = RunnableLambda(preprocess_text)

# Generación de resumen
def generate_summary(text):
  """Generar un resumen conciso del texto manteniendo el sentimiento original"""
  prompt = f"Resume en una sola oración: {text}"
  response = llm.invoke(prompt)
  return response.content

summary_branch = RunnableLambda(generate_summary)

# Análisis de sentimiento con formato JSON
def analyze_sentiment(text):
  """Analiza el sentimiento y devuelve el resultado estructurado"""
  prompt = f"""Analiza el sentimiento del siguiente texto.
  Responde ÚNICAMENTE en formato JSON válido:
  {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}

  Texto: {text}"""

  response = llm.invoke(prompt)
  try:
    return json.loads(response.content)
  except json.JSONDecodeError:
    return {"sentimiento": "neutro", "razon": "Error en análisis"}
  
sentiment_branch = RunnableLambda(analyze_sentiment)

# Combinación de resultados
def merge_results(data):
  """Combina los resultados de ambas ramas en un formato unificado"""
  return {
    "resumen": data["resumen"],
    "sentimiento": data["sentimiento_data"]["sentimiento"],
    "razon": data["sentimiento_data"]["razon"],
  }

merger = RunnableLambda(merge_results)

parallel_analysis = RunnableParallel({
  "resumen": summary_branch,
  "sentimiento_data": sentiment_branch,
})

# Construir la cadena de llamadas
chain = preprocessor | parallel_analysis | merger

review_batch = [
  "Excelente producto, muy satisfecho con la compra.",
  "Terrible calidad, no lo recomiendo para nada.",
  "Esta bien, cumple su función básica pero nada especial."
  ]

# Ejecutar la cadena de llamadas en lote de manera simultánea. Si falla en alguno, el resto se ejecutará en paralelo. Más simple que llamarlo de manera secuencial. 
resultado_batch = chain.batch(review_batch)
print(resultado_batch)