from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.  \nNombre del usuario: {nombre}\nAsistente: ",
)

chain = LLMChain(llm=chat, prompt=plantilla)

resultado = chain.run(nombre="Pepe")
print(resultado)


