import requests
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path  
import argparse
import re

def extract_text(element):
    text = []
    for subelement in element:
        if subelement.tag == 'b':
            text.append(f"{subelement.text}:")  # Bold text followed by a colon
        elif subelement.tag == 'i':
            text.append(f"{subelement.text}")  # Italics
        else:
            text.append(subelement.text.strip())  # Normal text
    return ' '.join(text).replace('  ', ' ')  # Remove extra spaces


# Create the argument parser
parser = argparse.ArgumentParser(description="Process retstart value")
parser.add_argument('--retstart', type=int, help='Start position for PubMed query')

# Parse the arguments
args = parser.parse_args()

# Access the retstart argument
print(f"Running script with retstart={args.retstart}")
retstart=args.retstart

# Step 1: Search PubMed using the esearch API
esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
esearch_params = {
    "db": "pubmed",
    "term": "misinformation[Title/Abstract]",  # search term
    "retmax": "10",          # maximum number of results
    "retmode": "xml",          # return format
    "sort": "pub_date",
    "retstart": retstart 
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
    count = root.find(".//Count").text
    ret_start = root.find(".//Count").text
    print(count," ", retstart)
    # Step 2: Fetch article details using the efetch API
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    efetch_params = {
        "db": "pubmed",
        "id": ','.join(pmids),   # comma-separated list of PMIDs
        # "id": "36569790",   # comma-separated list of PMIDs
        "retmode": "xml",        # return format
        "rettype": "abstract",   # return the article abstracts
    }
    # print("PMIDS: ", pmids)
    # Send the efetch request
    efetch_response = requests.get(efetch_url, params=efetch_params)
    
    if efetch_response.status_code == 200:
        # Parse the efetch XML response to extract titles and abstracts
        efetch_root = ET.fromstring(efetch_response.content)
        
        for article in efetch_root.findall(".//PubmedArticle"):
            title = article.find(".//ArticleTitle").text
            title = title if title is not None else "blank"
            pmid = article.find(".//PMID").text
            revised_day = article.find(".//DateRevised/Day").text
            revised_month = article.find(".//DateRevised/Month").text
            revised_year = article.find(".//DateRevised/Year").text
            # abstract = article.find(".//Abstract/AbstractText")
            # abstract_text = abstract.text if abstract is not None else "blank"
            # abstract_text = abstract_text if abstract_text is not None else "blank"


            # Filter articles that contain 'misinformation' in the title or abstract
            print("PMID:", pmid)
            
            abstract_texts = []
            for abstract in article.findall('.//Abstract/AbstractText'):
                xml_output = ET.tostring(abstract, encoding='unicode', method='xml')
                xml_output = xml_output.replace("<b>", "")
                xml_output = xml_output.replace("</b>", "")
                xml_output = xml_output.replace("<i>", "")
                xml_output = xml_output.replace("</i>", "")
                xml_output = xml_output.replace("<AbstractText>", "")
                xml_output = xml_output.replace("</AbstractText>", "")

                pattern = r'<AbstractText.*?>'
                cleaned_text = re.sub(pattern, '', xml_output, flags=re.DOTALL)
                # print("text ", cleaned_text)
                # text = abstract.text.strip()
                abstract_texts.append(cleaned_text)
                # print(text)
            abstract_text = " ".join(abstract_texts)

            # if abstract_text == "":
            #     break

            keywords = []
            for keyword in article.findall('.//KeywordList/Keyword'):
                text = keyword.text.strip()
                keywords.append(text)
                # print(text)
            keywords_text = ", ".join(keywords)
            
            authors = []
            for author in article.findall('.//AuthorList/Author'):
                first_name = author.find('.//ForeName')
                first_name_text = "" if first_name is None else first_name.text.strip()
                last_name = author.find('.//LastName')
                last_name_text = "" if last_name is None else last_name.text.strip()
                authors.append(f"{first_name_text} {last_name_text}")
                # print(text)
            authors_text = ", ".join(authors)
            

            # if "misinformation" in title.lower() or "misinformation" in abstract_text.lower(): #todo: remove this and use term instead
            # print("Title:", title)
            # print("Abstract:", abstract_text)
            # print("-------")
            dict={}
            dict['PMID'] = pmid
            dict['Title'] = title
            dict['Abstract'] = abstract_text
            dict['Revised_Year'] = revised_year
            dict['Revised_Month'] = revised_month
            dict['Revised_Day'] = revised_day
            dict['Keywords'] = keywords_text
            dict['Authors'] = authors_text
            list.append(dict)
    else:
        print(f"Error: Unable to fetch article details (status code: {efetch_response.status_code})")

else:
    print(f"Error: Unable to fetch data (status code: {response.status_code})")

path_name = 'results/misinformation_articles_full_4.csv'
article_df=pd.DataFrame(list)
filepath = Path(path_name)  
filepath.parent.mkdir(parents=True, exist_ok=True)  
article_df.to_csv(filepath, mode='a', index=False, header=False)
