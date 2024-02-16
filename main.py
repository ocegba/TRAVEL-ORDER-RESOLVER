import spacy
import os
from transformers import CamembertForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification, CamembertTokenizerFast
import langid

nlp_fr = spacy.load('fr_core_news_sm')

# Specify the local path to your model
model_path = "./models/trajet_v2"

# Load the tokenizer and model from the local path
tokenizer = CamembertTokenizerFast.from_pretrained(model_path)
model = CamembertForTokenClassification.from_pretrained(model_path)

def process_sentence(sentence, tokenizer, model):
    # Tokenize the input sentence
    inputs = tokenizer(sentence, return_tensors="pt")

    # Forward pass through the model
    outputs = model(**inputs)
    logits = outputs.logits

    # Get the predicted labels for each token in the sequence
    predicted_label_ids = logits.argmax(dim=2)[0].tolist()
    
    # Convert label IDs to actual labels using the id2label mapping from the model's configuration
    predicted_labels = [model.config.id2label[label_id] for label_id in predicted_label_ids]

    dep_words = [word for word, label in zip(tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze().tolist()), predicted_labels) if label in ['B-DEP', 'I-DEP']]

    dest_words = [word for word, label in zip(tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze().tolist()), predicted_labels) if label in ['B-DEST', 'I-DEST']]
    # Join multi-token entities for departure
    dep_entities = join_multi_token_entities(dep_words)
    
    # Join multi-token entities for destination
    dest_entities = join_multi_token_entities(dest_words)

    return predicted_labels, dep_entities, dest_entities

def join_multi_token_entities(words):
    entities = []
    current_entity = ""
    for word in words:
        if word.startswith('▁'):  # Start of a new entity
            if current_entity:
                entities.append(current_entity)
            current_entity = word[1:]
        else:
            current_entity += word
    if current_entity:  # Add the last entity
        entities.append(current_entity)
    return entities

def detect_language(sentence):
    return langid.classify(sentence)

def main():
    input_file_path = os.path.abspath("sample_nlp_input.txt")
    output_file_path = os.path.abspath("sample_nlp_output.txt")

    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:

        for line in input_file:
            line = line.strip().split(',', 1)
            
            # Extract sentence_id and sentence from the line
            sentence_id, sentence = line[0], line[1]

            # Check if sentence_id is a number
            if not sentence_id.isdigit():
                output_file.write(f"0,NOT_TRIP\n")
                continue

            # Detect the language of the sentence
            lang, _ = detect_language(sentence)

            # Check if the detected language is French
            if lang == 'fr':
                predicted_labels, dep_words, dest_words = process_sentence(sentence, tokenizer, model)

                if all(label == 'O' for label in predicted_labels):
                    output_file.write(f"{sentence_id},NOT_TRIP\n")
                else:
                    output_file.write(f"{sentence_id },{', '.join(dep_words)}, {', '.join(dest_words)} ====> {dep_words} - {dest_words}\n")
            
            else:
                output_file.write(f"{sentence_id},NOT_FRENCH\n")

if __name__ == "__main__":
    main()
