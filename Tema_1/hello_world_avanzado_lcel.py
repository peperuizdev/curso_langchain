from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Language Expresion Language (LCEL)

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.  \nNombre del usuario: {nombre}\nAsistente: ",
)

chain = plantilla | chat

resultado = chain.invoke({"nombre": "Pepe"})
print(resultado.content)


