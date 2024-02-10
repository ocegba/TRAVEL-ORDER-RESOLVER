import logging
from datasets import load_metric
from transformers import CamembertTokenizerFast

from trajet_dataset import IOBTRAJETDataset

metric = load_metric("seqeval", trust_remote_code=True)

class Tokenizer(object):
    NAME = "Tokenizer"

    def __init__(self, pretrained_tokenizer_checkpoint):
        self._tokenizer = CamembertTokenizerFast.from_pretrained(pretrained_tokenizer_checkpoint)

    @property
    def tokenizer(self):
        return self._tokenizer

    @staticmethod
    def init_vf(pretrained_tokenizer_checkpoint):
        return Tokenizer(pretrained_tokenizer_checkpoint=pretrained_tokenizer_checkpoint)

    def tokenize_and_align_labels(self, examples):
        logging.info("Tokenize and align labels...")

        tokenized_inputs = self._tokenizer(
            examples["tokens"],
            truncation=True,
            is_split_into_words=True,
            padding="max_length",  # Use padding directly in the __call__ method.
            return_tensors="pt",  # Return PyTorch tensors directly.
        )

        labels = []
        for i, label in enumerate(examples[f"ner_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:  # Set the special tokens to -100.
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(-100)
                previous_word_idx = word_idx
            labels.append(label_ids)

        tokenized_inputs["labels"] = labels
        return tokenized_inputs

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    pretrained_tokenizer_checkpoint = "camembert-base"
    dataset = IOBTRAJETDataset().dataset

    preprocessor = Tokenizer.init_vf(pretrained_tokenizer_checkpoint=pretrained_tokenizer_checkpoint)

    tokenized_datasets = dataset.map(preprocessor.tokenize_and_align_labels, batched=True)

    print(dataset)
    print("*" * 100)
    print(tokenized_datasets)
    print("First sample: ", dataset["train"][0])
    print("*" * 100)
    print("First tokenized sample: ", tokenized_datasets["train"][0])
