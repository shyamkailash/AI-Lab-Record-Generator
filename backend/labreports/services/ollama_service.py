import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"


def generate_lab_record(
    experiment_name,
    subject,
    language="",
    output_text="",
    code_text=""
):
    prompt = f"""
You are a college lab record generator.

Generate the lab record using EXACTLY this format:

Aim:
Write one clear aim for the experiment.

Procedure:
Write 4 to 6 simple numbered steps.

Program or Theory:
If code is given, write the exact code.
If code is not given, write short theory.

Output:
Write only the given output text.

Result:
Write one simple result sentence.

Input Details:
Experiment Name: {experiment_name}
Subject: {subject}
Programming Language: {language}
OCR Output Text: {output_text}
Code: {code_text}

Strict Rules:
Do not use markdown.
Do not use ###.
Do not use **.
Do not use ``` code blocks.
Do not add extra headings.
Do not explain the rules.
Start directly with Aim:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    data = response.json()
    return data.get("response", "").strip()
