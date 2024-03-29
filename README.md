# CitationScreeningReplicability

[![arXiv](https://img.shields.io/badge/arXiv-2201.07534-b31b1b.svg)](https://arxiv.org/abs/2201.07534)

This repository is the official implementation of the ECIR 2022 paper [Automation of Citation Screening for Systematic Literature Reviews using Neural Networks: A Replicability Study](https://link.springer.com/chapter/10.1007/978-3-030-99736-6_39).


## Citing

If you find our code useful, please cite our paper:

```bibtex
@inproceedings{kusa2022automation,
  title={Automation of Citation Screening for Systematic Literature Reviews Using Neural Networks: A Replicability Study},
  author={Kusa, Wojciech and Hanbury, Allan and Knoth, Petr},
  booktitle={European Conference on Information Retrieval},
  pages={584--598},
  year={2022},
  organization={Springer}
}
```


## Installation

Tested with Python 3.8.

Install requirements with pip:

```bash
$ pip install -r requirements.txt
```

## Datasets

### Clinical

Original Clinical review datasets can be downloaded from [here](https://github.com/bwallace/citation-screening). Use `src/data/prepare_clinical_data.py` script to prepare the datasets. Make sure that the variable `repository_path` is set to a root of a `bwallace/citation-screening/` repository.

### Drug

Original Drug review datasets can be downloaded from [here](https://dmice.ohsu.edu/cohenaa/systematic-drug-class-review-data.html). 

This dataset does not contain Abstract and Title information, so this data needs to be downloaded from PubMed using the article's PubMed ID. Place `epc-ir.clean.tsv` input file in a `data/external/drug/` folder and run `src/data/prepare_drug_data.py` script.


### SWIFT

Original SWIFT review datasets can be downloaded from [here](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-016-0263-z#Sec30). 

- OHAT datasets (`PFOA/PFOS`, `Bisphenol A (BPA)`, `Transgenerational` and `Fluoride and neurotoxicity`) are stored as four sheets in one Excel [file](https://static-content.springer.com/esm/art%3A10.1186%2Fs13643-016-0263-z/MediaObjects/13643_2016_263_MOESM1_ESM.xlsx).

- CAMRADES dataset (`Neuropathic pain`) is stored as a separate Excel [file](https://static-content.springer.com/esm/art%3A10.1186%2Fs13643-016-0263-z/MediaObjects/13643_2016_263_MOESM2_ESM.xlsx).


`Fluoride and neurotoxicity`, and `Neuropathic pain` already contain a title and abstract data, so the only needed preparation step is a conversion of the Label column into a common format.

Other datasets consist only of PubMed IDs and assigned labels so, it is necessary to download abstract and title data using biopython.

`src/data/prepare_swift_data.py` script accept .tsv files, so you need to convert each dataset into separate .tsv file and place them in `data/external/SWIFT/` folder.

________

For Drug and SWIFT datasets, in order to download documents from Pubmed, you need to set `Entrez.email` variable to your email address.


## Results

Detailed results are stored in `reports/` directory

- `results-document_features.csv` file contains detailed results of input document feature influence for all models and datasets.  
- `results-precision_at_95recall.csv` file contains detailed precision@95% recall results for all models and datasets.
- `results-time.csv` file contains training time measurement results for all models and datasets.

### Figures

In order to recreate the figures, run jupyter notebook `notebooks/plotting.ipynb`.

### Dataset statistics

In order to calculate dataset statistics, run `src/data/dataset_statistics.py` script.
