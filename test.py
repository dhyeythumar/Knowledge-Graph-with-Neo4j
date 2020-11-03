# import wikipediaapi  # pip install wikipedia-api
# import concurrent.futures
# from tqdm import tqdm
# import pandas as pd
# import spacy
# import neuralcoref
# from textPreprocessing import TextPreprocessing

# nlp = spacy.load('en_core_web_lg')
# neuralcoref.add_to_pipe(nlp)

# def wiki_page(page_name):
#     wiki_api = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
#     page_name = wiki_api.page(page_name)
#     if not page_name.exists():
#         print('Page {} does not exist.'.format(page_name))
#         return

#     page_data = pd.DataFrame({
#         'page': page_name,
#         'text': page_name.text,
#         'link': page_name.fullurl,
#         'categories': [[y[9:] for y in
#                        list(page_name.categories.keys())]],
#         })
#     return page_data


# import pandas as pd
# import bs4
# import requests
# import spacy
# from spacy import displacy
# from spacy.matcher import Matcher 
# from spacy.tokens import Span 
# import networkx as nx
# import matplotlib.pyplot as plt
# from tqdm import tqdm

import json
import os
os.system("")

def getMiniBatch(batch_size=5):
    miniBatch = []
    temp_doc = {
        "doc_name": "",
        "wiki_url": "",
        "done": True,
        "entity_list": []
    }
    i = 0
    with open("./wiki_links_doc/test_wiki_links_remaining.json", "r", encoding='utf8') as f:
        whole_list = json.loads(f.read())
    for key, value in whole_list.items():
        temp_doc["doc_name"] = key
        temp_doc["wiki_url"] = value
        miniBatch.append(temp_doc.copy())  # cos its reference type
        i += 1
        if(i == batch_size):
            break
    return miniBatch

# Add back the wiki urls when there is an error in the current doc in miniBatch
def updateRemaining_JSON(miniBatch):
    print('\033[93m'+"[WARNING] Removing the URL from remaining list !!"+'\033[0m')
    with open("./wiki_links_doc/test_wiki_links_remaining.json", "r+", encoding='utf8') as f:
        prev_list = json.loads(f.read())
        for doc in miniBatch:
            if(doc['done'] == True):
                prev_list.pop(doc['doc_name'])
            else:
                print('\033[93m'+" >> [Compute ERR] Entity list was not generated for {}".format(doc['doc_name'])+'\033[0m')
        f.seek(0)
        f.truncate()
        json.dump(prev_list, f)

def updateCompleted_JSON(miniBatch):
    with open("./wiki_links_doc/test_wiki_links_completed.json", "r+", encoding='utf8') as f:
        prev_list = json.loads(f.read())
        for doc in miniBatch:
            if(doc['done'] == True):
                prev_list[doc['doc_name']] = doc['wiki_url']
        f.seek(0)
        f.truncate()
        json.dump(prev_list, f)


if __name__ == "__main__":
    mini_batch = getMiniBatch()

    # -- Update JSON files --
    updateCompleted_JSON(mini_batch)
    updateRemaining_JSON(mini_batch)
