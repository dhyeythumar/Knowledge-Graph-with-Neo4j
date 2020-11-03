'''
:: Process ::
1. Picks one of the URL from unscraped list and passes this to textPreprocessing.py
2. Gets preprocessed text from textPreprocessing.py
3. Sends the preprocessed text to knowledgeExtraction.py to generate knowledge &
    Gets the knowledge representation from knowledgeExtraction.py in the form of list of triples
4. Upload/add the relaptionship data to Neo4j Graph DB using database_connection.py
5. Visualize the graph using networkx using visualization.py
'''

from textPreprocessing import TextPreprocessing
from knowledgeExtraction import KnowledgeExtraction
from mongoDBC import MongoDBC
import json
import sys
import os
os.system("")


# Used to check the process and intermediate text files.
DEBUG = {
    'saveHTML2text' : False,  # to save the text in html_2_text.txt 
    'saveEntities' : False,   # to save entity_list in a entity_list.json
    'KG2csv' : False,        
    'vis' : False
}

def vis(doc_name, list_of_dict):
    from visualization import Visualization
    import pandas as pd

    triplet_list = []
    for doc in list_of_dict:
        triplet_list.append([doc['subject'], doc['relation'], doc['object'], doc['subj_type'], doc['obj_type']])

    triplet_DF = pd.DataFrame(triplet_list, columns=['subject', 'relation', 'object', 'subj_type', 'obj_type'])

    Visualization.drawKnowledgeGraph(triplet_DF)
    Visualization.queryKnowledgeGraph(triplet_DF, doc_name)

    # Storing the data in pandas Dataframe
    if(DEBUG['KG2csv']):
        triplet_DF.to_csv("./textual_data/entity_data.csv")
        print("[INFO] Extracted knowledge has been stored in './textual_data/entity_data.csv'")


def getMiniBatch(batch_size=5):
    miniBatch = []
    temp_doc = {
        "doc_name": "",
        "wiki_url": "",
        "done": False,
        "entity_list": []
    }
    i = 0
    with open("./wiki_links_doc/wiki_links_remaining.json", "r", encoding='utf8') as f:
        whole_list = json.loads(f.read())
    for key, value in whole_list.items():
        temp_doc["doc_name"] = key
        temp_doc["wiki_url"] = value
        miniBatch.append(temp_doc.copy())  # cos its reference type
        i += 1
        if(i == batch_size):
            break
    return miniBatch

def updateRemaining_JSON(miniBatch):
    print('\033[93m'+"[WARNING] Removing the URL from remaining list !!"+'\033[0m')
    with open("./wiki_links_doc/wiki_links_remaining.json", "r+", encoding='utf8') as f:
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
    with open("./wiki_links_doc/wiki_links_completed.json", "r+", encoding='utf8') as f:
        prev_list = json.loads(f.read())
        for doc in miniBatch:
            if(doc['done'] == True):
                prev_list[doc['doc_name']] = doc['wiki_url']
        f.seek(0)
        f.truncate()
        json.dump(prev_list, f)


''' :: mini_batch structure ::
mini_batch = [ ..., 
    {
        "doc_name" : "",
        "wiki_url" : "",
        "done" : False,
        "entity_list" : [ ...,
            {
                "subject" : "",
                "relation" : "",
                "object" : "",
                "subj_type" : "",
                "obj_type" : ""
            }, ...
        ]
    }, ...
]
'''
def run():
    # Test the mongoDB, if not renning then exit !!
    try:
        mongoDBC_obj = MongoDBC()
        print("[INFO] MongoDB Atlas server is connected")
    except:
        print('\033[91m'+"\n[ERR] MongoDB Atlas server didn't responded to the connect request !!"+'\033[0m')
        print('\033[91m'+"\t>> Check the IP whitelisted addresses on which the DB is active"+'\033[0m')
        sys.exit()

    mini_batch = getMiniBatch()
    for doc in mini_batch:
        # HTML 2 Text and preprocessing of the text
        preprocessed_text = TextPreprocessing.process(doc['wiki_url'], DEBUG['saveHTML2text'])
        # Knowledge extraction
        knowledgeExtraction_obj = KnowledgeExtraction(doc['doc_name'], preprocessed_text, DEBUG['saveEntities'])
        doc['entity_list'] = knowledgeExtraction_obj.retrieveKnowledge()  # => list of dictionaries
        if(len(doc['entity_list']) != 0):
            doc['done'] = True
        print("="*100)

    # Storing the whole mini_batch to mongoDB
    mongoDBC_obj.insertMany(mini_batch)
    mongoDBC_obj.totalDocCount()

    # -- Update JSON files --
    updateCompleted_JSON(mini_batch)
    updateRemaining_JSON(mini_batch)

    '''Visualize the graphs using networkx'''
    if(DEBUG['vis']):
        vis(mini_batch[0]['doc_name'], mini_batch[0]['entity_list'])


if __name__ == "__main__":
    run()