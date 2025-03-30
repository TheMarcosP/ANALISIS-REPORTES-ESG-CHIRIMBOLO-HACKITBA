import json
import os
from uploadToVectorStore import uploadToVectorStore
from getClient import getClient


def getGuidelineFeedback(textPath, client, rootpath):


    #read prompt from file
    prompt_path = os.path.join(rootpath, "generateDataset", "prompts", "guideline.txt")
    with open(prompt_path, "r") as file:
        prompt = file.read().replace('\n', '')

    #read guideline from file
    guideline_path = os.path.join(rootpath, "data","guideline", "resumen_guia_divulgacion_asg.txt")
    with open(guideline_path, "r",  encoding="utf-8") as file:
        guideline = file.read().replace('\n', '')

    #read ESG report from file
    name = os.path.basename(textPath).split(".")[0]  # Extract name from file path
    report_path = os.path.join(rootpath, "data", "texts", name + ".txt")

    # Upload the ESG report to the vector store
    response, vector_store = uploadToVectorStore(report_path, client)
    if response.last_error:
        print("[x] Something went wrong: ", response.last_error)
    else:
        print("[+] ESG report uploaded successfully")

    print("[*] Generating feedback on guideline...")
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[{
            "role": "user", 
            "content": prompt + "\n" + guideline + "\n" 
        }],
        tools=[{
        "type": "file_search",
        "vector_store_ids": [f"{vector_store.id}"],
        }]
        
    )

    return response.output_text


if __name__ == "__main__":
    # Path to your PDF file
    name = "Pampa-2022-Reporte-Sustentabilidad"
    file_path = os.path.join("data", name + ".txt")  # Replace with your PDF file path

    # Get the summary of the txt file
    events = getGuidelineFeedback(file_path, getClient(os.path.join("openai_key.txt")))

    # Save the structured output to a file
    output_path = os.path.join("data", "feedbackGuideline", name + ".txt")
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=4)

    print(f"Structured output saved to {output_path}")