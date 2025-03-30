import json
from openai import OpenAI # pip install openai
import os
from uploadToVectorStore import uploadToVectorStore
from getClient import getClient


def getSummary(textPath, client, rootpath):

    #read prompt from file
    prompt_path = os.path.join(rootpath,"generateDataset", "prompts", "summary.txt")
    with open(prompt_path, "r") as file:
        prompt = file.read().replace('\n', '')

    #read ESG report from file
    name = os.path.basename(textPath).split(".")[0]  # Extract name from file path
    report_path = os.path.join(rootpath,"data", "texts", name + ".txt")

    # Upload the ESG report to the vector store
    response, vector_store = uploadToVectorStore(report_path, client)
    if response.last_error:
        print("[x] Something went wrong: ", response.last_error)
    else:
        print("[+] ESG report uploaded successfully")

    print("[*] Generating summary...")
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[{
            "role": "system", 
            "content": "Extract the key metrics and estimators from the ESG report in the specified format."
        }],
        tools=[{
        "type": "file_search",
        "vector_store_ids": [f"{vector_store.id}"],
        }],
        text={
            "format": {
                "type": "json_schema",
                "name": "resultado",
                "schema": {
                    "type": "object",
                    "properties": {
                        "resultados": {
                            "type": "array",
                            "description": "Lista de objetos con valores específicos.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "valor": {
                                        "type": "string",
                                        "description": "Un elemento central que puede ser una medida numérica o información descriptiva."
                                    },
                                    "categoria": {
                                        "type": "string",
                                        "description": "La categoría a la que pertenece el valor.",
                                        "enum": [
                                            "Medioambiente",
                                            "Social",
                                            "Gobernanza"
                                        ]
                                    },
                                    "descripcion": {
                                        "type": "string",
                                        "description": "Una nota explicativa que cite el texto de referencia."
                                    },
                                    "keywords": {
                                        "type": "array",
                                        "description": "Lista de palabras clave relevantes para la funcionalidad de búsqueda.",
                                        "items": {
                                            "type": "string"
                                        }
                                    }
                                },
                                "required": [
                                    "valor",
                                    "categoria",
                                    "descripcion",
                                    "keywords"
                                ],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": [
                        "resultados"
                    ],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    # Parse the structured response and save it to a JSON file
    events = json.loads(response.output_text)


    return events



if __name__ == "__main__":
    # Path to your PDF file
    name = "Pampa-2022-Reporte-Sustentabilidad"
    file_path = os.path.join("data", name + ".txt")  # Replace with your PDF file path

    # Get the summary of the txt file
    events = getSummary(file_path,  getClient(os.path.join("openai_key.txt")))

    # Save the structured output to a file
    output_path = os.path.join("data", "summaries", name + ".json")
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=4)

    print(f"Structured output saved to {output_path}")

