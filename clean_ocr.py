import openai
import os
from tqdm import tqdm

openai.api_key = "YOUR_API_KEY"

def get_subfolders(folder_path):
    subfolders = []
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            subfolders.append(subfolder_path)
    return subfolders

def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


folder_path = "./sample"
subfolders = get_subfolders(folder_path)
for subfolder in tqdm(subfolders):
    with open(f'{subfolder}/raw_transcription.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    

    # ここにプロンプト
    prompt = f"以下のバッククォーテーションで囲まれたOCRで書き起こした文書について，整形してください```{content}```"


    # GPT-4に入力
    response = get_completion(prompt)
    print(response)


    with open(f"{subfolder}/cleaned_transcription.txt", "w", encoding="utf-8") as file:
        file.write(response)