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


# Report

## Problem Statement
How to design and train a robust AI model capable of accurately detecting the departure and arrival cities in sentences or texts, considering potential challenges such as case variability, compound city names, and other linguistic variations? 

Additionally, the goal is to optimize the F1 score as the primary metric for evaluating the model's performance.

Our project was inspired by the token classification task outlined in the [Hugging Face Token Classification documentation](https://huggingface.co/docs/transformers/tasks/token_classification).

## Datas
Our dataset was generated using various patterns, each representing a distinct scenario of travel or exploration. The sentences cover diverse situations, incorporating elements like city names, travel experiences, and cultural exploration. These patterns were used to create datasets for training, testing, and evaluation through our generate_data.py code.

Here is an example of some patterns used:

    "After exploring the bustling streets of {}, I headed to {} for some tranquility."
    "From {} to {}, Nana traced the footsteps of history and local culture."
    "I roamed the green trails of {} before ending up in {} for an urban immersion."

Additionally, the dataset includes labeled information for each word in the sentences, specifying parts of speech (POS) and tags. For example:

    Sentence #,Word,POS,Tag,sentence
    Sentence:1,J',PRON,O,J'ai choisi de passer par Wassigny avant d'explorer Surtauville et d'y découvrir une scène artistique bouillonnante.
    Sentence:1,ai,AUX,O,J'ai choisi de passer par Wassigny avant d'explorer Surtauville et d'y découvrir une scène artistique bouillonnante.
    [...]

This labeled data is crucial for training and evaluating our AI model's performance accurately. The patterns and associated information in our dataset serve as the foundation for developing a robust model capable of precisely identifying departure and arrival cities in diverse linguistic contexts.

## Method
We initially chose Spacy for Named Entity Recognition (NER), but upon reflection, we decided to switch to Camembert.

Our decision is grounded in several factors. Camembert, being a transformer-based natural language processing (NLP) model, has demonstrated impressive performance across various language processing tasks. Trained specifically on French data, it aligns well with our linguistic context, potentially enhancing NER accuracy.

Camembert's focus on the French language, coupled with strong community support and documentation, makes it a pragmatic choice. The model's pre-trained nature for French contributes to improved results compared to more generic models.

We referred to the process outlined in the [Hugging Face documentation](https://huggingface.co/docs/transformers/tasks/token_classification) to realize this project.

### Dataset
To create the dataset, we referred to the approach outlined in the [Hugging Face documentation](https://huggingface.co/docs/transformers/tasks/token_classification#load-wnut-17-dataset). Recognizing the importance of dataset diversity, we devised a method to ensure variability within the generated sentences.

**1) Creation**

**Data Retrieval**  
We obtained geographical data including regions, departments, cities, and villages of France and its overseas territories from the French government's official dataset.

**Sentence Pattern Generation**     
We created a set of sentence patterns with placeholders for city names and other linguistic elements.

**City Replacement**    
We replaced the placeholders in each sentence pattern with randomly selected city names from our dataset, ensuring a mix of uppercase and lowercase variations.

**Labeling**    
We labeled each sentence to indicate the start and end indices of the departure and arrival cities, assigning the labels "DEP" and "DEST" respectively.

**IOB Tagging**     
We applied the IOB (Inside, Outside, Beginning) tagging scheme to identify the position of each city name within the sentences, enabling precise token classification.

**Dataset Splitting**       
The generated dataset was divided into three parts: training, testing, and validation (dev) sets.

**2) Preprocess**

To preprocess the datas, we referred to the approach outlined in the [Hugging Face documentation](https://huggingface.co/docs/transformers/tasks/token_classification#preprocess). 

Thanks to `tokenizer.py`, we use  a CamembertTokenizerFast tokenizer to preprocess the tokens field. We'll need to set is_split_into_words=True to tokenize the words into subwords.

However, this adds some special tokens [CLS] and [SEP] and the subword tokenization creates a mismatch between the input and labels. A single word corresponding to a single label may now be split into two subwords. We need to realign the tokens and labels by:

- Mapping all tokens to their corresponding word with the word_ids method.
- Assigning the label -100 to the special tokens [CLS] and [SEP] so they’re ignored by the PyTorch loss function (see CrossEntropyLoss).
- Only labeling the first token of a given word. Assign -100 to other subtokens from the same word.

On utilise la méthode tokenize_and_align_labels et on l'ajuste.

### Processus

We use ``camembert_model.ipynb`` to create the model and ``main.py`` that takes an input sample_nlp_input.txt and applies the model and generated sample_nlp_output.txt

**Training, Testing, and Optimization Process**     
In this section, we describe the step-by-step process for training, testing, and optimizing the token classification model for detecting departure and arrival cities in sentences.

**Data and Dataset Generation**     
To create a diverse dataset for training, we retrieved geographical data, including regions, departments, cities, and villages of France and its overseas territories. We generated sentence patterns with placeholders for city names and replaced these placeholders with randomly selected city names, ensuring variability in case (uppercase and lowercase). The dataset was labeled to indicate the start and end indices of departure and arrival cities, labeled as "DEP" and "DEST."

**Tokenization and IOB Tagging**    
We utilized the Camembert tokenizer to tokenize the generated dataset. Additionally, we applied the IOB (Inside, Outside, Beginning) tagging scheme to identify the position of each city name within the sentences. This tagging scheme facilitates precise token classification during model training.

**Model Configuration**     
We used the CamembertForTokenClassification model from the Hugging Face Transformers library. The model was initialized with the Camembert base checkpoint, and its configuration was adjusted to match the number of labels in our dataset.

**Training Configuration**      
The training process involved defining hyperparameters, such as the learning rate, batch size, and maximum number of epochs. We employed the AdamW optimizer with weight decay, gradient accumulation steps, and gradient checkpointing for memory efficiency.

**Training and Evaluation**     
The model was trained using the defined hyperparameters and the tokenized training dataset. Evaluation was performed after each epoch on the validation dataset, and the training process was repeated for the specified number of epochs.

**Testing and Metrics**     
After training, the model was evaluated on a separate test dataset. Metrics such as precision, recall, F1 score, and accuracy were computed using the Seqeval library. The results provide insights into the model's performance in detecting departure and arrival cities.

**Results and Analysis**        
The final results, including metrics and any notable observations, were saved to a JSON file for further analysis. This file is stored in the "results" directory.

### Metrics
For evaluating the performance of your model, we've mentioned optimizing the F1 score as the primary metric. Additionally, we could consider including other metrics such as precision, recall, and accuracy. To do that, we referred to this [documentation](https://huggingface.co/docs/transformers/tasks/token_classification#evaluate) 

## Results
We obtain :

    {
    "DEP": {
        "precision": 0.7963299418604651,
        "recall": 0.8560546875,
        "f1": 0.825112951807229,
        "number": 15360
    },
    "DEST": {
        "precision": 0.8377068557919621,
        "recall": 0.9227864583333333,
        "f1": 0.8781908302354398,
        "number": 15360
    },
    "overall_precision": 0.8172708782005265,
    "overall_recall": 0.8894205729166667,
    "overall_f1": 0.85182067589475,
    "overall_accuracy": 0.9769229927925366
    }

## Conclusion