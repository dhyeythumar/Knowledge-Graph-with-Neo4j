import spacy
from spacy.matcher import Matcher 
# from spacy.tokens import Span
import neuralcoref
# from tqdm import tqdm

class KnowledgeExtraction:

    def __init__(self, doc_name, doc_content, saveEntities:bool=False):
        # self.nlp = spacy.load('en_core_web_sm')
        self.nlp = spacy.load('en_core_web_lg')
        neuralcoref.add_to_pipe(self.nlp)
        self.doc_name = doc_name.lower()
        self.doc_content = doc_content
        self.saveEntities = saveEntities

    def get_relation(self, doc:str):
        # Matcher class object 
        matcher = Matcher(self.nlp.vocab)
        #define the pattern 
        pattern = [{'DEP':'ROOT'}, 
                    {'DEP':'prep','OP':"?"},
                    {'DEP':'agent','OP':"?"},  
                    {'POS':'ADJ','OP':"?"}] 
        matcher.add("matching_1", None, pattern) 
        matches = matcher(doc)
        k = len(matches) - 1
        span = doc[matches[k][1]:matches[k][2]] 
        return str(span.text)

    def retrieveKnowledge_1(self, coref=True):
        doc = self.nlp(self.doc_content)
        if coref:
            doc = self.nlp(doc._.coref_resolved)  # resolve coreference clusters

        sentences = [sent.string.strip() for sent in doc.sents]  # split doc into sentences
        entity_pairs = []
        for sent in sentences:
            sent = self.nlp(sent)
            spans = list(sent.ents) + list(sent.noun_chunks)  # collect nodes
            spans = spacy.util.filter_spans(spans)
            with sent.retokenize() as retokenizer:
                [retokenizer.merge(span, attrs={'tag': span.root.tag, 'dep': span.root.dep}) for span in spans]
            deps = [token.dep_ for token in sent]

            # limit our example to simple sentences with one subject and object
            if (deps.count('obj') + deps.count('dobj')) != 1 or (deps.count('subj') + deps.count('nsubj')) != 1:
                continue

            relation = self.get_relation(sent)
            ## chunk 1
            ent1 = ""
            ent2 = ""
            prv_tok_dep = ""    # dependency tag of previous token in the sentence
            prv_tok_text = ""   # previous token in the sentence
            prefix = ""
            modifier = ""
            for tok in sent:
                ## chunk 2
                # if token is a punctuation mark then move on to the next token
                if tok.dep_ != "punct":
                    # check: token is a compound word or not
                    if tok.dep_ == "compound":
                        prefix = tok.text
                        # if the previous word was also a 'compound' then add the current word to it
                        if prv_tok_dep == "compound":
                            prefix = prv_tok_text + " "+ tok.text

                    # check: token is a modifier or not
                    if tok.dep_.endswith("mod") == True:
                        modifier = tok.text
                        # if the previous word was also a 'compound' then add the current word to it
                        if prv_tok_dep == "compound":
                            modifier = prv_tok_text + " "+ tok.text

                    ## chunk 3
                    if tok.dep_.find("subj") == True:
                        ent1 = modifier +" "+ prefix + " "+ tok.text
                        prefix = ""
                        modifier = ""
                        prv_tok_dep = ""
                        prv_tok_text = ""

                    ## chunk 4
                    if tok.dep_.find("obj") == True:
                        ent2 = modifier +" "+ prefix +" "+ tok.text

                    ## chunk 5  
                    # update variables
                    prv_tok_dep = tok.dep_
                    prv_tok_text = tok.text
            entity_pairs.append([ent1.strip(), relation.strip(), ent2.strip()])
        with open("./textual_data/newmethod_text.txt", 'w', encoding='utf8') as f:
            f.write(str(entity_pairs))
        print('[INFO] Total number of Entity pairs [Subject-Verb-Object] extracted :: ', str(len(entity_pairs)))
        return entity_pairs

    def retrieveKnowledge_2(self):
        doc = self.nlp(self.doc_content)
        sentences = [sent.string.strip() for sent in doc.sents]  # split doc into sentences
        entity_pairs = []
        for sent in sentences:
            ## chunk 1
            ent1 = ""
            ent2 = ""
            prv_tok_dep = ""    # dependency tag of previous token in the sentence
            prv_tok_text = ""   # previous token in the sentence
            prefix = ""
            modifier = ""
            for tok in self.nlp(sent):
                ## chunk 2
                # if token is a punctuation mark then move on to the next token
                if tok.dep_ != "punct":
                    # check: token is a compound word or not
                    if tok.dep_ == "compound":
                        prefix = tok.text
                        # if the previous word was also a 'compound' then add the current word to it
                        if prv_tok_dep == "compound":
                            prefix = prv_tok_text + " "+ tok.text

                    # check: token is a modifier or not
                    if tok.dep_.endswith("mod") == True:
                        modifier = tok.text
                        # if the previous word was also a 'compound' then add the current word to it
                        if prv_tok_dep == "compound":
                            modifier = prv_tok_text + " "+ tok.text

                    ## chunk 3
                    if tok.dep_.find("subj") == True:
                        ent1 = modifier +" "+ prefix + " "+ tok.text
                        prefix = ""
                        modifier = ""
                        prv_tok_dep = ""
                        prv_tok_text = ""

                    ## chunk 4
                    if tok.dep_.find("obj") == True:
                        ent2 = modifier +" "+ prefix +" "+ tok.text

                    ## chunk 5  
                    # update variables
                    prv_tok_dep = tok.dep_
                    prv_tok_text = tok.text
            relation = self.get_relation(sent)
            entity_pairs.append([ent1.strip(), relation.strip(), ent2.strip()])
        with open("./textual_data/newmethod_text.txt", 'w', encoding='utf8') as f:
            f.write(str(entity_pairs))
        print('[INFO] Total number of Entity pairs [Subject-Verb-Object] extracted :: ', str(len(entity_pairs)))
        return entity_pairs


if __name__ == "__main__":
    url_list = [{
        'doc_name': "Albert Einstein",
        'wiki_url': "https://en.wikipedia.org/wiki/Albert_Einstein",
        'doc_content': "In his paper on mass–energy equivalence, Einstein produced E = mc2 as a consequence of his special relativity equations."
    }]
    knowledgeExtraction_obj = KnowledgeExtraction(url_list[0]['doc_name'], url_list[0]['doc_content'], True)
    triplet_list = knowledgeExtraction_obj.retrieveKnowledge_1()  # => list of lists
    print(triplet_list) # => [['Einstein', 'produced', 'his special relativity equations']]
