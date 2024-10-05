
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain_google_vertexai import VertexAI



model = VertexAI(model_name="gemini-pro")

memory = ConversationBufferMemory()


chain = ConversationChain(llm=model, memory = memory)

txt = input()
while txt != 'exit':
    print(chain(txt)['response'])
    txt = input()