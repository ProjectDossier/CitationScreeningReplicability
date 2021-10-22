"""Module calculates descriptive statistics of all review datasets in a .tsv format"""
import os
from typing import Dict

from tqdm import tqdm
import pandas as pd


def dataset_statistics(df: pd.DataFrame) -> Dict:
    statistics = {}
    exclusions = df[df["Label"].astype(int) == 0]
    inclusions = df[df["Label"].astype(int) == 1]

    len_df = len(df)
    statistics["len"] = len_df
    statistics["#exclusions"] = len(exclusions)
    statistics["%exclusions"] = len(exclusions) / len_df
    statistics["#inclusions"] = len(inclusions)
    statistics["%inclusions"] = len(inclusions) / len_df

    statistics["max_WSS@95%"] = len(exclusions) / len_df - 0.05

    statistics["avg_char_num"] = df["Abstract"].str.len().mean()
    statistics["avg_char_num_inclusions"] = inclusions["Abstract"].str.len().mean()
    statistics["avg_char_num_exclusions"] = exclusions["Abstract"].str.len().mean()

    statistics["avg_word_num"] = df["Abstract"].str.split().str.len().mean()
    statistics["avg_word_num_inclusions"] = (
        inclusions["Abstract"].str.split().str.len().mean()
    )
    statistics["avg_word_num_exclusions"] = (
        exclusions["Abstract"].str.split().str.len().mean()
    )

    return statistics


if __name__ == "__main__":
    data_dir = "../../data/processed/"
    output_file = "../../reports/dataset_statistics.csv"

    total_statistics = {}
    dataset_files = [file for file in os.listdir(data_dir) if file.endswith(".tsv")]
    for file in tqdm(dataset_files):
        dataset_name = file.split(".")[0]

        df = pd.read_csv(f"{data_dir}/{file}", sep="\t")
        total_statistics[dataset_name] = dataset_statistics(df=df)

    results = pd.DataFrame.from_dict(total_statistics).transpose()
    results.sort_index().to_csv(output_file)
