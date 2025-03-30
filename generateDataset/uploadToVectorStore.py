from openai import OpenAI
import pymupdf4llm
import pathlib
import os


def uploadToVectorStore(input_path, client):
    vector_store_name = os.path.basename(input_path).split(".")[0]  # Extract name from file path
    vector_store = client.vector_stores.create(  # Create vector store
        name=vector_store_name,
    )


    response = client.vector_stores.files.upload_and_poll(  # Upload file
        vector_store_id=vector_store.id,
        file=open(input_path, "rb"),
    )

    return response, vector_store

if __name__ == "__main__":

    # Get OpenAI API key from file
    path = os.path.join("openai_key.txt")
    with open(path, "r") as file:
        key = file.read().replace('\n', '')

    # Initialize OpenAI client with the API key
    client = OpenAI(
    api_key=key
    )
    
    # Set the name of the PDF file and the output markdown file
    name = "testPdf"
    # input_file = os.path.join("data","reports", name + ".txt")  # Path to the PDF file
    parsed_file = os.path.join("data","texts", name + ".txt")  # Path to the output markdown file

    # Parse the PDF file and
    # md_text = pymupdf4llm.to_markdown(input_file)  # Convert PDF to markdown
    # pathlib.Path(output_file).write_bytes(md_text.encode())

    # Upload it to the vector store
    print(f"[*] Parsing {name}.txt to vector store...")
    response = uploadToVectorStore(parsed_file, client)
    if response.last_error:
        print("[x] Something went wrong: ", response.last_error)
    else:
        print("[+] PDF parsed and uploaded successfully")


