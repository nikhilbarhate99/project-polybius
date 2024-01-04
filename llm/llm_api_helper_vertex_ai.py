#!/bin/python3

from global_variables import *
import vertexai
from vertexai.language_models import TextGenerationModel


GCP_LOCATION = "us-central1"
GCP_PROJECT_NAME = "dcsc-lab2-398417"
GCP_TEXT_GEN_MODEL_NAME = "text-bison"
GCP_TEXT_GEN_MODEL_TEMP = 0.5
GCP_TEXT_GEN_MODEL_MAX_OUTPUT_TOKENS = 512


vertexai.init(project=GCP_PROJECT_NAME, location=GCP_LOCATION)
parameters = {
    "candidate_count": 1,
    "max_output_tokens": GCP_TEXT_GEN_MODEL_MAX_OUTPUT_TOKENS,
    "temperature": GCP_TEXT_GEN_MODEL_TEMP,
    "top_p": 0.8,
    "top_k": 40
}

text_gen_model = TextGenerationModel.from_pretrained(GCP_TEXT_GEN_MODEL_NAME)

def generate_text(prompt):
    
    response = text_gen_model.predict(
        prompt,
        **parameters
    )
    
    print(f"Response from Model: ", response.text)
    # print("num tokens in input prompt:", text_gen_model.countMessageTokens(prompt))

    return response.text

