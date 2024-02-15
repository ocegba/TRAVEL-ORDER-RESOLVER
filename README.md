# TRAVEL ORDER RESOLVER

## Overview

This Python-based program is designed to process text and voice commands related to travel orders and generate appropriate itineraries based on customer expectations. The core functionality of this software involves discriminating between valid and non-valid orders, as well as identifying departure and destination details from the input text.

## Features

- **Text :** The program accepts text inputs, making it versatile and user-friendly. Users can submit trip orders via email, chat messages.

- **Named Entity Recognition (NER):** Utilizing advanced NER techniques, the program identifies and extracts relevant information such as departure locations and destinations from the provided input.

- **Validation Mechanism:** The software incorporates a robust validation mechanism to distinguish between valid and non-valid travel orders.

- **Itinerary Generation:** Once the relevant details are extracted and validated, the program generates one or more appropriate travel itineraries that align with the customer's expectations. These itineraries can include transportation modes, routes, and estimated travel times.

## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```

### Clone the Repository

To get started, clone this repository to your local machine using the following command:

```bash
git clone git@github.com:EpitechMscProPromo2024/T-AIA-901-MPL_7.git
```

```bash
cd T-AIA-901-MPL_7
python -m venv .venv
source .venv\Scripts\activate    # On Windows
```

```bash
source .venv/bin/activate # On macOS/Linux
pip install -r requirements.txt
```

## Usage

### Training or Using the Model

**1) From Scratch**

If you want to train the model from scratch:

1. You have to create a virtual environment and install `python -m spacy download fr_core_news_sm`.
2. Execute `python generate_data.py` to generate or download the required data files [here](https://drive.google.com/drive/folders/1CwlDv9-gv2yMrvKn3sGn3sgh0O70P5Th?usp=sharing).
3. Run `camembert_model.ipynb` to train the model.
4. After training, you can use the model in `main.py`.

**2) Using a Pretrained Model**

If you want to use a pretrained model:

1. You have to create a virtual environment and install `python -m spacy download fr_core_news_sm`.
2. Download the required data files [here](https://drive.google.com/drive/folders/1CwlDv9-gv2yMrvKn3sGn3sgh0O70P5Th?usp=sharing) and the pretrained model repository from [here](https://drive.google.com/drive/folders/1vWVqxsKW2YoniYJZUIgs8RuayMPTSKu8?usp=sharing).
3. Place the downloaded files in the appropriate directories (`datas/` and `models/`).
4. Run `main.py` to utilize the pretrained model for travel order resolution.

### Testing

To test the functionality of the program:

1. Ensure that the required dependencies are installed and the virtual environment is activated.
2. Modify or add some sentences in `sample_nlp_input.txt`.
3. Run `main.py`.
4. Review the generated travel itinerary or any validation messages.

## Project Architectures

    .
    ├── README.md
    ├── __pycache__
    ├── camembert_model.ipynb
    ├── datas
    │   ├── cache
    │   ├── csv
    │   │   ├── cities.csv
    │   │   ├── departments.csv
    │   │   └── regions.csv
    │   ├── dev_iob.csv
    │   ├── test_iob.csv
    │   └── train_iob.csv
    ├── generate_data.py
    ├── main.py
    ├── models
    │   └── trajet_v1
    │       ├── added_tokens.json
    │       ├── config.json
    │       ├── model.safetensors
    │       ├── sentencepiece.bpe.model
    │       ├── special_tokens_map.json
    │       ├── tokenizer.json
    │       ├── tokenizer_config.json
    │       └── training_args.bin
    ├── requirements.txt
    ├── results
    │   └── results.json
    ├── sample_nlp_input.txt
    ├── sample_nlp_output.txt
    ├── test-ner
    ├── tokenizer.py
    └── trajet_dataset.py
