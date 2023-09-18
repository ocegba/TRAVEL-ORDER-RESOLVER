<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: e a bottins.csv dataset with annotated entries from 20th-century directories


The specificity of this dataset is that the annotation is directly done in the text. To test the NER,
you will need to start by splitting the annotation to have the original text on one side and the
annotated tokens on the other. This phase requires a bit more work than the previous one before
you can get the initial results.
Once the cleaning is done, try running spaCy as well as a NER model based on Transformers
(e.g., BERT), and evaluate the results.


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
| `assets/bottins.csv` | URL | bottins.csv |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->