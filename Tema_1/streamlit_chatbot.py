from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Confguración de la página de la aplicación
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown('Este es un chabot de ejemplo construido con LangChain + Streamlit. ¡Escribe tu mensaje abajo para comenzar!')

# Sidebar para configurar el modelo y la temperatura
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    
    # Inicializar el modelo de lenguaje con la configuración seleccionada
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)

# Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
  st.session_state.mensajes = []

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatbotPro.
     
     Historial de la conversación:
     {historial}

     Responde de manera clara y concisa a la siguiente pregunta {mensaje}"""
)

# Crear cadena usando LCEL (Langchain Expresion Language)
cadena = prompt_template | chat_model

# Renderizar historial existente
for msg in st.session_state.mensajes:
  if isinstance(msg, SystemMessage):
    # No mostrar el mensaje por pantalla
    continue
  
  role = "assistant" if isinstance(msg, AIMessage) else "user"
  with st.chat_message(role):
    st.markdown(msg.content)

#Botón para iniciar una nueva conversaciónº
if st.button("🗑️ Nueva conversación"):
  st.session_state.mensajes = []
  st.rerun()

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje aquí: ")

if pregunta:
  # Mostrar y almacenar mensaje del usuario
  with st.chat_message("user"):
    st.markdown(pregunta)

  # Generar y mostrar respuesta del usuario
  try:
    with st.chat_message("assistant"):
      response_placeholder = st.empty()
      full_response = ""

      # streaming de la respuesta
      for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
        full_response += chunk.content
        response_placeholder.markdown(full_response + "▌")  # Agregar un cursor de carga

      response_placeholder.markdown(full_response)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    st.session_state.mensajes.append(AIMessage(content=full_response))

  except Exception as e:
    st.error(f"Error al generar respuesta: {str(e)}")
    st.info("Verifica que tu Api Key esté configurada correctamente y que el modelo seleccionado esté disponible.")