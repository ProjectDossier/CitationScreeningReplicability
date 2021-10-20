"""This module prepares Clinical systematic review data.
Inout data comes from the repository: https://github.com/bwallace/citation-screening/
"""
import os
import argparse

import pandas as pd


def prepare_clinical_dataset(
    dataset_name: str,
    labels_filename: str,
    repository_path: str,
    output_folder: str,
) -> None:
    """
    github.com/bwallace/citation-screening/tree/master/modeling/curious_snake/data

    :param dataset_name: name of the dataset
    :param labels_filename: filename that contains labels for that dataset
    :param repository_path: path to the root of bwallace/citation-screening/ repository
    :param output_folder:
    :return:
    """
    labels_column: str = "Label"

    in_path = (
        f"{repository_path}/modeling/curious_snake/data/{dataset_dict['dataset_name']}"
    )
    labels_file = f"{in_path}/{labels_filename}"

    abstract_dir = f"{in_path}/Abstracts/"
    title_dir = f"{in_path}/Titles/"
    output_file = f"{output_folder}/{dataset_name}.tsv"

    dataset = {}
    with open(labels_file) as fp:
        for content in fp.readlines():
            paper = {}
            doc_id, label = content.split(" ")[:2]
            if label == "-1":
                paper[labels_column] = 0
            else:
                paper[labels_column] = label

            dataset[doc_id] = paper

    for abstract_file in os.listdir(abstract_dir):
        if (
            not os.path.isdir(f"{abstract_dir}/{abstract_file}")
            and abstract_file in dataset
        ):
            doc_id = abstract_file.split("/")[-1]
            with open(f"{abstract_dir}/{abstract_file}") as fp:
                abstract = fp.readline()

            with open(f"{title_dir}/{abstract_file}") as fp:
                title = fp.readline()

            dataset[doc_id]["Title"] = f"{title.lower()}. {abstract.lower()}"
            dataset[doc_id]["Abstract"] = f"{title.lower()}. {abstract.lower()}"

    df = pd.DataFrame.from_dict(dataset).transpose()

    df.to_csv(output_file, sep="\t", index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repository_path",
        default="../../../citation-screening/",
        type=str,
        help="Path to the https://github.com/bwallace/citation-screening/ repository",
    )
    parser.add_argument(
        "--output_folder",
        default="../../data/processed/",
        type=str,
    )

    args = parser.parse_args()

    datasets = [
        {"dataset_name": "proton_beam", "labels_filename": "proton_labeled_features"},
        {
            "dataset_name": "micro_nutrients",
            "labels_filename": "micro_labeled_features_only",
        },
        {"dataset_name": "copd", "labels_filename": "copd_labeled_terms_only"},
    ]

    for dataset_dict in datasets:
        print(f"{dataset_dict['dataset_name']=}")

        prepare_clinical_dataset(
            dataset_name=dataset_dict["dataset_name"],
            labels_filename=dataset_dict["labels_filename"],
            repository_path=args.repository_path,
            output_folder=args.output_folder,
        )
