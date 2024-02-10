import logging
import os
import datasets
import spacy
import csv
from spacy.training.iob_utils import biluo_to_iob, doc_to_biluo_tags
from datasets import ClassLabel, DownloadConfig
import pandas as pd
from pandas import read_csv
import csv
from generate_data import DataGenerator

logger = datasets.logging.get_logger(__name__)

class IOBTRAJETConfig(datasets.BuilderConfig):
    """BuilderConfig for IOBTRAJET"""

    def __init__(self, **kwargs):
        """BuilderConfig for IOBTRAJET.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IOBTRAJETConfig, self).__init__(**kwargs)

class IOBTRAJET(datasets.GeneratorBasedBuilder):
    """IOBTRAJET dataset."""

    BUILDER_CONFIGS = [
        IOBTRAJETConfig(
            name="IOBTRAJET",
            version=datasets.Version("1.0.0"),
            description="IOBTRAJET dataset",
        ),
    ]

    def __init__(
        self,
        *args,
        cache_dir,
        csv_file_train="datas/train_iob.csv",
        csv_file_validation="datas/dev_iob.csv",
        csv_file_test="datas/test_iob.csv",
        ner_tags=("B-DEP", "I-DEP", "B-DEST", "I-DEST", "O"),
        **kwargs,
    ):
        self._csv_file_train = csv_file_train
        self._csv_file_validation = csv_file_validation
        self._csv_file_test = csv_file_test
        self._ner_tags = ner_tags
        super(IOBTRAJET, self).__init__(*args, cache_dir=cache_dir, **kwargs)

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens":  datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=sorted(list(self._ner_tags))
                        )
                    ),
                }
            ),
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # Specify the URLs from which to download the data and where to store them
        urls_to_download = {
            "train": self._csv_file_train,
            "validation": self._csv_file_validation,
            "test": self._csv_file_test,
        }

        # Download and extract the data if necessary
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        # Return the SplitGenerators
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"csv_file": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"csv_file": downloaded_files["validation"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"csv_file": downloaded_files["test"]},
            ),
        ]

    def _generate_examples(self, csv_file):
        logger.info("⏳ Generating examples from = %s", csv_file)

        df = pd.read_csv(csv_file, encoding="utf-8")

        guid = 0
        tokens = []
        ner_tags = []
        prev_prefix = "Sentence:1"

        for index, row in df.iterrows():
            if row["Sentence #"] == "Sentence #":
                continue

            prefix = row["Sentence #"]

            if prev_prefix != prefix:
                if tokens:
                    yield guid, {
                        "id" : str(guid),
                        "tokens": tokens,
                        "ner_tags": ner_tags,
                    }
                    guid += 1
                    tokens = []
                    ner_tags = []
                
                prev_prefix = prefix

            tokens.append(row["Word"])
            ner_tags.append(row["Tag"])

        if tokens:
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
            
class IOBTRAJETDataset(object):

    NAME = "IOBTRAJETDataset"

    def __init__(self):
        cache_dir = "datas/cache"
        os.makedirs(cache_dir, exist_ok=True)

        download_config = DownloadConfig(cache_dir=cache_dir)
        
        self._dataset = IOBTRAJET(cache_dir=cache_dir)

        self._dataset.download_and_prepare(download_config=download_config)

        self._dataset = self._dataset.as_dataset()

    @property
    def dataset(self):
        return self._dataset

    @property
    def labels(self) -> ClassLabel:
        return self._dataset["train"].features["ner_tags"].feature.names

    @property
    def id2label(self):
        return dict(list(enumerate(self.labels)))

    @property
    def label2id(self):
        return {v: k for k, v in self.id2label.items()}

    def train(self):
        return self._dataset["train"]

    def test(self):
        return self._dataset["test"]

    def validation(self):
        return self._dataset["validation"]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    DataGenerator()

    dataset = IOBTRAJETDataset().dataset

    print(dataset['train'])
    print(dataset['test'])
    print(dataset['validation'])

    print("List of tags: ", dataset['train'].features['ner_tags'].feature.names)

    print("First sample: ", dataset['train'][0])