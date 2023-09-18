from pathlib import Path
import typer
from spacy.tokens import DocBin
import spacy
from pandas import read_csv
import random
from spacy.training.example import Example  # Ajout de "example"
from spacy.training.iob_utils import offsets_to_biluo_tags, biluo_tags_to_spans  # Modification de l'import
from spacy.scorer import Scorer
import csv
import re

ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "corpus"

def csv_to_txt(path: Path):  # Changement de la fonction pour correspondre à son nom
    with open(path, 'r', newline='', encoding='Latin1') as csv_file:
        csv_reader = csv.reader(csv_file)
    
        with open('bottins.txt', 'w', encoding='Latin1', errors='replace') as txt_file:
            for row in csv_reader:
                ligne = ','.join(row)
                txt_file.write(ligne + '\n')

def create_spacy_data():
    with open('bottins.txt', 'r', encoding='Latin1') as file:
        text = file.read()
    pattern = r'<PER>(.*?)<\/PER>, <ACT>(.*?)<\/ACT>, <LOC>(.*?)<\/LOC>, <CARDINAL>(\d+)<\/CARDINAL>'
    matches = re.findall(pattern, text)
    data = []
    for match in matches:
        ent = (f"{match[0]} {match[1]} {match[2]}",
            {"entities": [
                (0, len(match[0]), "PER"),
                (len(match[0])+1, len(match[0])+len(match[1])+1, "ACT"),
                (len(match[0])+len(match[1])+2, len(match[0])+len(match[1])+len(match[2])+2, "LOC")
            ]})
        data.append(ent)  # Déplacement de l'indentation pour inclure cette ligne dans la boucle

    return data

def split_data(spacy_data):
    random.shuffle(spacy_data)
    morceaux = len(spacy_data) // 10

    train_docs = spacy_data[:(morceaux * 6)]
    dev_docs = spacy_data[(morceaux * 6):(morceaux * 6) + (morceaux * 2)]
    test_docs = spacy_data[(morceaux * 6) + (morceaux * 2):]

    return train_docs, dev_docs, test_docs

def convert_to_doc_bin(nlp, docs, doc_bin):
    for text, annotations in docs:
        doc = nlp.make_doc(text)
        tags = offsets_to_biluo_tags(doc, annotations['entities'])  # This line seems to be causing the issue
        entities = biluo_tags_to_spans(doc, tags)
        doc.ents = entities
        doc_bin.add(doc)

def save_doc_bin(doc_bin, output_path):
    doc_bin.to_disk(output_path)

def main(assets_dir: Path=ASSETS_DIR, corpus_dir: Path=CORPUS_DIR, lang: str="fr"):
    nlp = spacy.blank(lang)

    csv_to_txt(assets_dir / "bottins.csv")  # Appel à la fonction corrigée
    spacy_data = create_spacy_data()
    train_docs, dev_docs, test_docs = split_data(spacy_data)

    train_doc_bin = DocBin()
    dev_doc_bin = DocBin()
    test_doc_bin = DocBin()

    convert_to_doc_bin(nlp, train_docs, train_doc_bin)
    convert_to_doc_bin(nlp, dev_docs, dev_doc_bin)
    convert_to_doc_bin(nlp, test_docs, test_doc_bin)

    save_doc_bin(train_doc_bin, f"./{corpus_dir}/train.spacy")
    save_doc_bin(dev_doc_bin, f"./{corpus_dir}/dev.spacy")
    save_doc_bin(test_doc_bin, f"./{corpus_dir}/test.spacy")

if __name__ == "__main__":
    typer.run(main)
