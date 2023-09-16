<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: NER dataset annotated in a very standard way


You're provided with a corpus zip-file, coming from a Kaggle challenge. It is a NER dataset annotated in a very standard way, where each word is associated with its corresponding label.
The file ner_dataset.csv contains different sentences; each line corresponds to a token with its NER tag. Note that all elements of the sentence are preserved, including commas, periods, etc.
These are all very important for identifying entities (e.g., "I saw Mr. Poubelle yesterday": In this case, even without the capitalization of “Poubelle,”
you can guess that it refers to a named entity and not an everyday object). Start by applying a classical NER model like spaCy to get a first idea of the results.
Then, calculate some more advanced metrics


## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `preprocess` | Convert the corpus to spaCy's format |
| `train` | Train a spaCy pipeline using the specified corpus and config |
| `evaluate` | Evaluate on the test data and save the metrics |
| `package` | Package the trained model so it can be installed |
| `visualize` | Visualize the model's output interactively using Streamlit |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `preprocess` &rarr; `train` &rarr; `evaluate` &rarr; `package` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/ner_dataset.csv` | URL | ner_dataset.csv |
| `assets/ner.csv` | URL | ner.csv |
| `assets/bottins.csv` | URL | bottins.csv |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->