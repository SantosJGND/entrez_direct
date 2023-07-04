import csv
import os
import random

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *

from modules.entrez_wrapper import EntrezWrapper
from modules.utils import read_taxid_file

output_dir = "assets/"
bindir= "entrez_direct_env/bin"

def app():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    ## get session id
    session_id = random.randint(0, 100000)
    # session_id = session_id.split("-")[0]

    put_markdown("## Metadata Entrez Direct Query")

    put_markdown("### 1. upload files")
    put_markdown("upload tsv file with taxid column")
    file1 = file_upload("upload taxid file", accept="*")

    put_markdown("### 2. requesting metadata")
    ## read files using pandas

    open(output_dir + f"{session_id}_metadata.tsv", "wb").write(file1["content"])

    ## display waiting message
    put_markdown("### processing files...")

    televir_reports = read_taxid_file(output_dir + f"{session_id}_metadata.tsv")
    
    if "taxid" not in televir_reports.columns:
        raise Exception("taxid column not found in metadata file")
    
    entrez_conn= EntrezWrapper(
        bindir= bindir,
        outdir= output_dir,
        outfile= f"{session_id}_query.tsv",
        query_type= "fetch_taxid_description",
        chunksize= 1000
    )


    try:


        taxids= televir_reports["taxid"].tolist()
        taxids= [str(taxid) for taxid in taxids]

        entrez_conn.run_queries(taxids)
        metad= entrez_conn.read_output()
        metad.to_csv(entrez_conn.output_path, sep= "\t", index= False)
        
        ## file to bytes

        merged_panel_bytes = open(
            entrez_conn.output_path, "rb"
        ).read()

        put_markdown("### 3. download requested metadata")
        put_file(f"request_metadata.tsv", merged_panel_bytes)

    except Exception as e:
        raise (e)

    finally:
        # remove files
        os.remove(entrez_conn.output_path)


if __name__ == "__main__":
    start_server(app, host="127.0.0.1", port=8000, debug=False)
