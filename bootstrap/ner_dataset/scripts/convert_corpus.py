from pathlib import Path
import typer
from spacy.tokens import DocBin
import spacy
from pandas import read_csv
import pandas as pd
import random
from spacy.training import docs_to_json, offsets_to_biluo_tags, biluo_tags_to_spans
from spacy.training import Example
from spacy.scorer import Scorer

ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "corpus"

def read_csv_final(path: Path):
    return read_csv(path, encoding="ISO-8859-1", usecols=['Sentence #', 'Word', 'POS', 'Tag'])

def create_spacy_data(words):
    spacy_data = []

    for i, row in words.iterrows():
        tokens = row["Word"]
        tags = row["Tag"]
        sentence = row["Sentence"]

        entities = []
        start_pos = 0

        for i in range(len(tags)):
            if tags[i] != 'O':
                end_pos = start_pos + len(str(tokens[i]))
                entities.append((start_pos, end_pos, tags[i]))
                start_pos = end_pos + 1
            else:
                start_pos += len(str(tokens[i]))

        data_tuple = (sentence, {"entities": entities})
        spacy_data.append(data_tuple)

    return spacy_data

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
        tags = offsets_to_biluo_tags(doc, annotations['entities'])
        entities = biluo_tags_to_spans(doc, tags)
        doc.ents = entities
        doc_bin.add(doc)

def save_doc_bin(doc_bin, output_path):
    doc_bin.to_disk(output_path)

def main(assets_dir: Path=ASSETS_DIR, corpus_dir: Path=CORPUS_DIR, lang: str="en"):
    nlp = spacy.blank(lang)

    data = read_csv_final(assets_dir / "ner_dataset.csv")
    words = pd.DataFrame(data.groupby('Sentence #')['Word'].apply(list))
    tags = data.groupby('Sentence #')['Tag'].apply(list)
    words['Tag'] = tags
    words['Sentence'] = words['Word'].apply(lambda x: " ".join(map(str, x)))

    spacy_data = create_spacy_data(words)
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
