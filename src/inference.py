from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
from utils import config


tokenizer = AutoTokenizer.from_pretrained(config['INFERENCE_MODEL'])
model = AutoModelForTokenClassification.from_pretrained(config['INFERENCE_MODEL'])
pipe = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_entities(text):
    return pipe(text)