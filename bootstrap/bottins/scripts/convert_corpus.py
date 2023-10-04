from pathlib import Path
import typer
from spacy.tokens import DocBin
import spacy
from pandas import read_csv
import random
from spacy.training import offsets_to_biluo_tags, biluo_tags_to_spans
import csv
import re

ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "corpus"

def csv_to_txt(path: Path):  # Changement de la fonction pour correspondre à son nom
    with open(path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
    
        with open('bottins.txt', 'w', encoding='utf-8', errors='replace') as txt_file:
            for row in csv_reader:
                ligne = ','.join(row)
                txt_file.write(ligne + '\n')

def create_spacy_data():
    with open('bottins.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []

    for sentence in lines:
        mots = sentence.split(",")  # Sépare la ligne en mots
        per = None
        loc = None
        cardinal = None
        act = None
        titre = None

        for mot in mots:
            if "<PER>" in mot:
                per = mot
            elif "<LOC>" in mot:
                loc = mot
            elif "<CARDINAL>" in mot:
                cardinal = mot
            elif "<ACT>" in mot:
                act = mot
            elif "<TITRE>" in mot:
                titre = mot

        random_elements_line = ""
        elements = [per, act, loc, cardinal, titre]
        random.shuffle(elements)

        for i in range(0, 5):
            random_elements_line += f"{elements[i].strip()} " if elements[i] is not None else ""

        matches = re.findall(
            r"<PER>(.*?)<\/PER>|<ACT>(.*?)<\/ACT>|<LOC>(.*?)<\/LOC>|<CARDINAL>(\d+)<\/CARDINAL>|<TITRE>(.*?)<\/TITRE>",
            random_elements_line)


        entities = []
        start_pos = 0

        random_sentences = ""

        for match in matches:
            for i, m in enumerate(match):
                if m:
                    tag = ["PER", "ACT", "LOC", "CARDINAL", "TITRE"][i]
                    end_pos = start_pos + len(str(m))
                    entities.append((start_pos, end_pos, tag))
                    start_pos = end_pos + 1
                    
                    random_sentences += f'{m}'

        data_tuple = (random_sentences, entities)
        data.append(data_tuple)

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
        print("=================================================================================")
        print(text, annotations)
        tags = offsets_to_biluo_tags(doc, annotations)
        entities = biluo_tags_to_spans(doc, tags)
        doc.ents = entities
        doc_bin.add(doc)

def save_doc_bin(doc_bin, output_path):
    doc_bin.to_disk(output_path)

def main(assets_dir: Path=ASSETS_DIR, corpus_dir: Path=CORPUS_DIR, lang: str="fr"):
    nlp = spacy.blank(lang)

    csv_to_txt(assets_dir / "bottins.csv")  # Appel à la fonction corrigée
    spacy_data = create_spacy_data()
    # train_docs, dev_docs, test_docs = split_data(spacy_data)

    # train_doc_bin = DocBin()
    # dev_doc_bin = DocBin()
    # test_doc_bin = DocBin()

    # convert_to_doc_bin(nlp, train_docs, train_doc_bin)
    # convert_to_doc_bin(nlp, dev_docs, dev_doc_bin)
    # convert_to_doc_bin(nlp, test_docs, test_doc_bin)

    # save_doc_bin(train_doc_bin, f"./{corpus_dir}/train.spacy")
    # save_doc_bin(dev_doc_bin, f"./{corpus_dir}/dev.spacy")
    # save_doc_bin(test_doc_bin, f"./{corpus_dir}/test.spacy")

if __name__ == "__main__":
    typer.run(main)