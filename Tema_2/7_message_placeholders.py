from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
  ("system", "Eres un asistente útil que mantiene el contexto de la conversación."),
  MessagesPlaceholder(variable_name="historial"),
  ("human", "Usuario: {pregunta_actual}")
])

# Simulamos un historial de conversación
historial_conversacion = [
  HumanMessage(content="Usuario:¿Cuál es la capital de Francia?"),
  AIMessage(content="IA: La capital de Francia es Paris."),
  HumanMessage(content="Usuario: ¿Y cuantos habitantes tiene?"),
  AIMessage(content="IA: Paris tiene aproximadamente 2,2 millones de habitantes."),
]

mensajes = chat_prompt.format_messages(
  historial = historial_conversacion,
  pregunta_actual = "¿Puedes decirme algo interesante de su arquitectura?"
)

for m in mensajes:
  print(m.content)
