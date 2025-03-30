import os
import sys
import json
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), "generateDataset"))  # Add the generateDataset directory to the path
from generateDataset.textract import extractTextFromPdf
from generateDataset.summary import getSummary
from generateDataset.guidelines import getGuidelineFeedback
from generateDataset.conclusions import getConclusion
def processNewReport(pdf_file_path, rootpath):
    """
    Process a new ESG report PDF file by extracting text and generating a summary.

    Args:
        pdf_file_path (str): The local file path of the PDF to be processed.
        rootpath (str): The root path of the project.

    Returns:
        str: The extracted text from the PDF.
    """

    data = dict()
    name = os.path.basename(pdf_file_path).split(".")[0]  # Extract name from file path

    outputFile = os.path.join(rootpath, "data", "texts")
    if not os.path.exists(outputFile):
        text = extractTextFromPdf(pdf_file_path)
        with open(os.path.join(outputFile, name + ".txt"), "w", encoding="utf-8") as file:
            file.write(text)


    outputFile = os.path.join(rootpath, "data", "summaries", name + ".json")
    if not os.path.exists(outputFile):
        summary = getSummary(pdf_file_path, rootpath)
        with open(outputFile, "w", encoding="utf-8") as file:
            file.write(summary)
    else:
        with open(outputFile, "r", encoding="utf-8") as file:
            summary = file.read().replace('\n', '')            
    data["SUMMARY"] = summary

        
    outputFile = os.path.join(rootpath,"data","scores", "ESGScores.json")
    with open(outputFile, "r",  encoding="utf-8") as file:
        scores = file.read().replace('\n', '')
    data["SCORES"] = json.loads(scores)[name]
    
    lawScores = pd.read_csv(os.path.join(rootpath,"data", "scores", "lawScores", name + "_cos_score.csv"))
    data["LAWSCORES"] = lawScores.to_dict(orient="records")


    outputFile = os.path.join(rootpath, "data", "feedbackGuideline", name + ".txt")
    if not os.path.exists(outputFile):
        feedback = getGuidelineFeedback(pdf_file_path, rootpath)
        with open(outputFile, "w", encoding="utf-8") as file:
            file.write(feedback)
    else:
        with open(outputFile, "r", encoding="utf-8") as file:
            feedback = file.read().replace('\n', '')
    data["FEEDBACK"] = feedback

    outputFile = os.path.join(rootpath, "data", "conclusions", name + ".txt")
    if not os.path.exists(outputFile):
        conclusion = getConclusion(pdf_file_path, rootpath)
        with open(outputFile, "w", encoding="utf-8") as file:
            file.write(conclusion)
    else:
        with open(outputFile, "r", encoding="utf-8") as file:
            conclusion = file.read().replace('\n', '')
    data["CONCLUSION"] = conclusion

    return data     

if __name__ == "__main__":
    # Path to your PDF file
    name = "Pampa-2022-Reporte-Sustentabilidad"
    file_path = os.path.join("data", name + ".pdf")  # Replace with your PDF file path

    # Process the PDF file
    processNewReport(file_path, "")  # Pass the root path if needed