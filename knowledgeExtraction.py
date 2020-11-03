'''
⚠ Important note ⚠
'neuralcoref' is to be installed using the master branch from github

Subject-Verb-Object triplet detection

>>  Info on Language Models for english:
        1. Small model [11 MB file size]
            download:   python -m spacy download en_core_web_sm
            usage:      nlp = spacy.load('en_core_web_sm')

        2. Medium model [48 MB file size]
            download:   python -m spacy download en_core_web_md
            usage:      nlp = spacy.load('en_core_web_md')

        3. Large model [746 MB file size]
            download:   python -m spacy download en_core_web_lg
            usage:      nlp = spacy.load('en_core_web_lg')
'''

import spacy
import neuralcoref
import json

class KnowledgeExtraction:

    def __init__(self, doc_name:str, doc_content:str, saveEntities:bool=False):
        self.nlp = spacy.load('en_core_web_lg')
        neuralcoref.add_to_pipe(self.nlp)
        self.doc_name = doc_name.lower()
        self.doc_content = doc_content
        self.saveEntities = saveEntities

    def refine_entity(self, ent, sent):
        unwanted_tokens = (
            'PRON',  # pronouns
            'PART',  # particle
            'DET',   # determiner
            'SCONJ', # subordinating conjunction
            'PUNCT', # punctuation
            'SYM',   # symbol
            'X',     # other
        )
        ent_type = ent.ent_type_  # get entity type
        if ent_type == '':
            ent_type = 'NOUN_CHUNK'
            ent = ' '.join(str(t.text) for t in self.nlp(str(ent)) if t.pos_ not in unwanted_tokens and t.is_stop == False)
        elif ent_type in ('NOMINAL', 'CARDINAL', 'ORDINAL') and str(ent).find(' ') == -1:
            refined = ''
            for i in range(len(sent) - ent.i):
                if ent.nbor(i).pos_ not in ('VERB', 'PUNCT'):
                    refined += ' ' + str(ent.nbor(i))
                else:
                    ent = refined.strip()
                    break
        return str(ent), str(ent_type)

    def retrieveKnowledge(self, coref=True):
        temp = {
            "subject" : "",
            "relation" : "",
            "object" : "",
            "subj_type" : "",
            "obj_type" : ""
        }
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
            try:
                for token in sent:
                    if token.dep_ not in ('obj', 'dobj'):  # identify object nodes
                        continue
                    subject = [w for w in token.head.lefts if w.dep_ in ('subj', 'nsubj')]  # identify subject nodes
                    if subject:
                        subject = subject[0]
                        # identify relationship by root dependency
                        relation = [w for w in token.ancestors if w.dep_ == 'ROOT']
                        if relation:
                            relation = relation[0]
                            # add adposition or particle to relationship
                            if relation.nbor(1).pos_ in ('ADP', 'PART'):
                                relation = ' '.join((str(relation), str(relation.nbor(1))))
                        else:
                            relation = 'unknown'

                        subject, subject_type = self.refine_entity(subject, sent)
                        token, object_type = self.refine_entity(token, sent)

                        # don't select empty string
                        if(subject != "" and subject_type != "" and token != "" and object_type != ""):
                            if(self.doc_name.find(subject.lower()) >= 0):
                                subject = self.doc_name
                            if(self.doc_name.find(token.lower()) >= 0):
                                token = self.doc_name
                            temp['subject'] = subject.capitalize()
                            temp['relation'] = str(relation).lower()
                            temp['object'] = token.capitalize()
                            temp['subj_type'] = subject_type
                            temp['obj_type'] = object_type
                            entity_pairs.append(temp.copy())
            except:
                print('\033[91m'+"[ERR] Sentence error in '{:s}' doc".format(self.doc_name)+'\033[0m')
                continue
        if(self.saveEntities):
            with open("./textual_data/entity_list.json", 'w', encoding='utf8') as f:
                json.dump(entity_pairs, f)
        print("-"*100)
        print('[INFO] Total number of Entity pairs [Subject-Verb-Object] extracted :: ', str(len(entity_pairs)))
        print("-"*100)
        return entity_pairs


if __name__ == "__main__":
    url_list = [{
        'doc_name': "Albert Einstein",
        'wiki_url': "https://en.wikipedia.org/wiki/Albert_Einstein",
        'doc_content': "In his paper on mass–energy equivalence, Einstein produced E = mc2 as a consequence of his special relativity equations."
    }]
    knowledgeExtraction_obj = KnowledgeExtraction(url_list[0]['doc_name'], url_list[0]['doc_content'], True)
    list_of_dict = knowledgeExtraction_obj.retrieveKnowledge()  # => list of lists
    print(list_of_dict)
