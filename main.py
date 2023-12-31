from modules.entrez_wrapper import EntrezWrapper

# +
# Path: main.py
#

if __name__ == "__main__":
        
    # Get command line arguments
    #args = get_args()
    
    # Get the query
    #query = get_query(args)
    
    # Run the query
    entrez_conn= EntrezWrapper(
        bindir= "entrez_direct_env/bin",
        outdir= "test",
        outfile= "test.txt",
        query_type= "fetch_taxid_description",
        chunksize= 1
    )

    entrez_conn.run_queries(["1562566", "69395", "507626"])
    df= entrez_conn.read_output()
    print(df)