import spacy
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import os
from tqdm import tqdm

# Cargar modelo de Spacy
nlp = spacy.load("es_dep_news_trf")

# Cargar modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Función para dividir texto en chunks
def split_text_into_chunks(text, chunk_size=3):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    chunks = [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]
    return chunks

# Directorio con los archivos .txt
input_dir = "data/texts"

# Cargar leyes desde CSV
laws_df = pd.read_csv("data/Argentina_laws.csv")

# Crear variable law_texts con Family Name sin duplicados
law_texts = laws_df["Family Name"].drop_duplicates().tolist()

# Asignar family_names para que coincidan con law_texts
family_names = law_texts

# Concatenar Family Name y Family Summary para obtener el texto completo
law_texts = (laws_df["Family Name"] + ". " + laws_df["Family Summary"]).drop_duplicates().tolist()

# Obtener embeddings de leyes
law_embeddings = model.encode(law_texts, convert_to_tensor=True)

# Procesar cada archivo .txt en el directorio
for filename in tqdm(os.listdir(input_dir), desc="Processing files"):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_dir, filename)
        
        # Leer texto desde el archivo .txt
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read().replace("\n", " ")
        
        # Obtener chunks del texto
        txt_chunks = split_text_into_chunks(text)
        
        # Inicializar el diccionario de similitudes
        max_similarities = {law: 0 for law in family_names}

        # Calcular similitudes para cada chunk y cada ley
        for chunk in tqdm(txt_chunks, desc=f"Processing chunks in {filename}"):
            chunk_embedding = model.encode(chunk, convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(chunk_embedding, law_embeddings)
            max_vals = similarities.max(dim=0).values.tolist()  # valores máximos
            
            # Actualiza el máximo por ley
            for i, law in enumerate(family_names):
                max_similarities[law] = max(max_similarities[law], max_vals[i])

        # Crear el DataFrame con las similitudes
        results_df = pd.DataFrame({"Law": family_names, "Score": list(max_similarities.values())})
        print(f"Results for {filename}:")
        print(results_df)
        
        # Guardar resultados en CSV
        output_csv = os.path.join("data/cos_simil", f"{os.path.splitext(filename)[0]}_cos_score.csv")
        results_df.to_csv(output_csv, index=False, encoding="utf-8-sig")