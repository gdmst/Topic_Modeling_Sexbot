import requests
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path  

# Step 1: Search PubMed using the esearch API
esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
esearch_params = {
    "db": "pubmed",
    "term": "misinformation",  # search term
    "retmax": "100",          # maximum number of results
    "retmode": "xml",          # return format
    "retstart": "0"
}

# Send the esearch request
response = requests.get(esearch_url, params=esearch_params)

# Check if the esearch request was successful
list = []

if response.status_code == 200:
    # Parse the XML response to get PubMed IDs (PMIDs)
    root = ET.fromstring(response.content)
    id_list = root.find('IdList')
    pmids = [id_elem.text for id_elem in id_list.findall('Id')]
    print(f"Found {len(pmids)} articles.")

    # Step 2: Fetch article details using the efetch API
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    efetch_params = {
        "db": "pubmed",
        "id": ','.join(pmids),   # comma-separated list of PMIDs
        "retmode": "xml",        # return format
        "rettype": "abstract",   # return the article abstracts
    }
    print("PMIDS: ", pmids)
    # Send the efetch request
    efetch_response = requests.get(efetch_url, params=efetch_params)
    
    if efetch_response.status_code == 200:
        # Parse the efetch XML response to extract titles and abstracts
        efetch_root = ET.fromstring(efetch_response.content)
        
        for article in efetch_root.findall(".//PubmedArticle"):
            title = article.find(".//ArticleTitle").text
            title = title if title is not None else "blank"
            pmid = article.find(".//PMID").text
            abstract = article.find(".//Abstract/AbstractText")
            abstract_text = abstract.text if abstract is not None else "blank"
            abstract_text = abstract_text if abstract_text is not None else "blank"
            # Filter articles that contain 'misinformation' in the title or abstract
            print("Title:", title, " PMID:", pmid)

            if "misinformation" in title.lower() or "misinformation" in abstract_text.lower():
                print("Title:", title)
                print("Abstract:", abstract_text)
                print("-------")
                dict={}
                dict['PMID'] = pmid
                dict['Title'] = title
                dict['Abstract'] = abstract_text
                list.append(dict)
    else:
        print(f"Error: Unable to fetch article details (status code: {efetch_response.status_code})")

else:
    print(f"Error: Unable to fetch data (status code: {response.status_code})")

path_name = 'results/misinformation_articles.csv'
article_df=pd.DataFrame(list)
filepath = Path(path_name)  
filepath.parent.mkdir(parents=True, exist_ok=True)  
article_df.to_csv(filepath, mode='a', index=False, header=False)
