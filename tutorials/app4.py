from langchain_google_genai import ChatGoogleGenerativeAI


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    vertexai=True,                  # <--- Force Vertex AI backend
    project="gd-gcp-gridu-genai",  # <--- Your GCP Project ID
)

result = llm.invoke("Explain dark matter in simple terms.")
print(result.content)
result = llm.invoke("Explain dark matter in simple terms.")
print(result.content)