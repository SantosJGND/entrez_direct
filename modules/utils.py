

import pandas as pd


def read_taxid_file(taxid_filepath):
    """
    read tsv file from televir export
    """
    reports = pd.read_csv(taxid_filepath, sep="\t")
    return reports