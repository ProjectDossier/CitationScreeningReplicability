"""This module prepares SWIFT systematic review data.
https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-016-0263-z
"""
import argparse

import pandas as pd
from Bio import Entrez, Medline

# change to your email address
Entrez.email = "Your.Name@example.org"


def get_from_pubmed(df)-> pd.DataFrame:
    """
    :param df: input dataframe containing (PubMedId, Label) dataset.
    """
    labels_column: str = "Label"
    pubmed_id_column: str = 'PMID'

    df[labels_column] = 1
    df.loc[df["Status"] == "Excluded", labels_column] = 0

    data_size = len(df)
    docs = []
    for x in range(0, data_size, 5000):
        pubmed_id_list = df[pubmed_id_column].tolist()[x:x+5000]
        handle = Entrez.efetch(db="pubmed", id=pubmed_id_list, rettype="medline", retmode="text")

        articles = Medline.parse(handle)
        for article in articles:
            docs.append(article)

    output_df = pd.DataFrame(docs)
    output_df = output_df.rename(
        columns={'TI': 'Title', 'AB': 'Abstract'})

    output_df[labels_column] = df[labels_column].tolist()

    return output_df


def prepare_fluoride_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    :param df: input dataframe containing Fluoride dataset
    """
    labels_column: str = "Label"
    df['Title'] = df['Title'].fillna("")
    df['Abstract'] = df['Abstract'].fillna("")

    df[labels_column] = 1
    df.loc[df['Included'] == 'EXCLUDED', labels_column] = 0

    return df


def prepare_neuropathic_pain_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    :param df: input dataframe containing NeuropathicPain dataset
    """
    labels_column: str = "Label"
    df['Title'] = df['Title'].fillna("")
    df['Abstract'] = df['Abstract'].fillna("")

    df['tmp_label'] = df['Label']
    df[labels_column] = 1
    df.loc[df['tmp_label'] == 'Excluded', labels_column] = 0

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_folder",
        default="../../data/external/SWIFT/",
        type=str,
    )
    parser.add_argument(
        "--output_folder",
        default="../../data/processed/",
        type=str,
    )

    args = parser.parse_args()

    datasets = {
        "NeuropathicPain.tsv": prepare_neuropathic_pain_dataset,
        "Fluoride.tsv": prepare_fluoride_dataset,
        "BPA.tsv": get_from_pubmed,
        "Transgenerational.tsv": get_from_pubmed,
        "PFOS-PFOA.tsv": get_from_pubmed,
    }

    for filename, parsing_function in datasets.items():
        input_data = f"{args.input_folder}/{filename}"
        output_data = f"{args.output_folder}/{filename}"

        df = pd.read_csv(input_data, sep='\t')
        print(f"{filename=}, {len(df)=}")

        df = parsing_function(df)
        df.to_csv(output_data, sep='\t', index=False)
