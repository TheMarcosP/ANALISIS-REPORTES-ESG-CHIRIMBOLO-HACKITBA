from openai import OpenAI
import pymupdf4llm
import os

path = os.path.join("openai_key.txt")
with open(path, "r") as file:
    key = file.read().replace('\n', '')

client = OpenAI(
  api_key=key
)

vector_store = client.vector_stores.create(        # Create vector store
    name="datos",
)

text = pymupdf4llm.to_markdown("testPdf.pdf")  # Convert PDF to markdown

client.vector_stores.files.upload_and_poll(        # Upload file
    vector_store_id=vector_store.id,
    file=text,
    file_type="markdown",
)