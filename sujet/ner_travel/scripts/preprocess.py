import typer
import srsly
from pathlib import Path
from spacy.util import get_words_and_spaces
from spacy.tokens import Doc, DocBin
import spacy
from pandas import read_csv
import random
from spacy.training import docs_to_json, offsets_to_biluo_tags, biluo_tags_to_spans

def main(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_path: Path = typer.Argument(..., dir_okay=False),
):
    nlp  = spacy.blank("fr")
    doc_bin = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])

    data = read_csv(input_path, encoding = "ISO-8859-1", usecols=['TEXT','DEPART','START_DEPART','END_DEPART','DEP','DESTINATION','START_DEST','END_DEST','DEST'])

    formatted_data = []

    for index, row in data.iterrows():
        text = row["TEXT"]
        dep_start = int(row["START_DEPART"])
        dep_end = int(row["END_DEPART"])
        dest_start = int(row["START_DEST"])
        dest_end = int(row["END_DEST"])

        entities = []

        # Check if entities conflict before adding them
        if (dep_start, dep_end, "DEP") != (dest_start, dest_end, "DEST"):
            entities.append((dep_start, dep_end, "DEP"))
            entities.append((dest_start, dest_end, "DEST"))

        formatted_item = (text, {"entities": entities})
        formatted_data.append(formatted_item)

    for text, annotations in formatted_data:
        doc = nlp.make_doc(text)
        tags = offsets_to_biluo_tags(doc, annotations['entities'])
        entities = biluo_tags_to_spans(doc, tags)
        doc.ents = entities
        doc_bin.add(doc)

    doc_bin.to_disk(output_path)

if __name__ == "__main__":
    typer.run(main)