'''
>> 'neomodel' is a python package for Object Graph Mapping.

:: Rules to add the data in Neo4j DB ::
1. Duplicate nodes are not allowed(uses the node if it exists).
2. Duplicate edges/relations b/w to same pair of nodes (source, dest) are not allowed. 
3. Adds multiple edges from one node to multiple different nodes.
4. Self looping can't occur because source and destination nodes are of different types.

Command to get all node & connections in Neo4j browser:
    match(n) return(n)

Provides the interface to Populates Neo4j DB
'''

from neomodel import (StructuredNode, StringProperty, RelationshipTo, config, StructuredRel, ZeroOrMore)
import sys
import os
os.system("")

config.DATABASE_URL = 'bolt://neo4j:admin@localhost:11005' # bolt://user:password@url

class RelationshipModel(StructuredRel):
    relationType = StringProperty()

class Object(StructuredNode):
    object_name = StringProperty(unique_index=True, required=True)
    object_type = StringProperty()
    # link from other node to this node " <= "
    # link_from = RelationshipFrom(Subject, 'predicate')

class Subject(StructuredNode):
    subject_name = StringProperty(unique_index=True, required=True)
    subject_type = StringProperty()
    # link to other nodes from this node " => "
    predicate = RelationshipTo(Object, 'predicate', cardinality=ZeroOrMore, model=RelationshipModel)


class Neo4jDBC:

    @staticmethod
    def insertEntities(doc_name:str, entity_list) -> None:
        print("\n[INFO] Adding the knowledge triplets on '{:s}' wiki doc to Neo4j graph DB".format(doc_name))
        for doc in entity_list:
            if(doc['subject'] == doc['object']):
                print('\033[93m'+"[WARNING] Discarding the self loop for '{:s}'".format(doc['subject'])+'\033[0m')
                continue

            subject_node = Subject.get_or_create({
                                    'subject_name': doc['subject'],
                                    'subject_type': doc['subj_type']
                                })[0]
            object_node = Object.get_or_create({
                                    'object_name': doc['object'],
                                    'object_type': doc['obj_type']
                                })[0]

            # Dynamically changing relation type using neomodel :: default name on edge ('predicate')
            # The relation is of type ZeroOrOne which has properties source and definition.
            subject_node.predicate.definition['relation_type'] = doc['relation']
            subject_node.predicate.connect(object_node, {'relationType': doc['relation']}).save()

    @staticmethod
    def printAllNodes():
        print("\n", "-"*100)
        print("[INFO] Printing all the existing Subject (link from) nodes >>")
        all_subject_nodes = Subject.nodes.all()
        for node in all_subject_nodes:
            print("{:s}  ".format(str(node)), end='')
        print("\n", "-"*100)

        print("\n", "-"*100)
        print("[INFO] Printing all the existing Object (link to) nodes >>")
        all_object_nodes = Object.nodes.all()
        for node in all_object_nodes:
            print("{:s}  ".format(str(node)), end='')
        print("\n", "-"*100)

    @staticmethod
    def deleteAllNodes():
        print('\033[93m'+"\n[WARNING] Deleting all the existing Subject (link from) & Object (link to) nodes\n"+'\033[0m')
        all_subject_nodes = Subject.nodes.all()
        for node in all_subject_nodes:
            node.delete()
        all_object_nodes = Object.nodes.all()
        for node in all_object_nodes:
            node.delete()


if __name__ == "__main__":
    test_data = [
        {
            "subject": "Albert einstein",
            "relation": "published",
            "object": "300 scientific papers",
            "subj_type": "ORG",
            "obj_type": "NOUN_CHUNK"
        },
        {
            "subject": "Albert einstein",
            "relation": "published",
            "object": "300 scientific papers",
            "subj_type": "ORG",
            "obj_type": "NOUN_CHUNK"
        },
        {
            "subject": "Albert einstein",
            "relation": "new relation",
            "object": "300 scientific papers",
            "subj_type": "ORG",
            "obj_type": "NOUN_CHUNK"
        },
        {
            "subject": "Loss",
            "relation": "forced",
            "object": "Sale",
            "subj_type": "NOUN_CHUNK",
            "obj_type": "NOUN_CHUNK"
        },
        {
            "subject": "Albert einstein",
            "relation": "took",
            "object": "Entrance examinations",
            "subj_type": "PERSON",
            "obj_type": "NOUN_CHUNK"
        },
        {
            "subject": "Albert einstein",
            "relation": "took",
            "object": "Swiss citizenship",
            "subj_type": "PERSON",
            "obj_type": "NOUN_CHUNK"
        },
    ]
    try:
        # Neo4jDBC().insertEntities("Albert einstein", test_data)
        Neo4jDBC().printAllNodes()
        # Neo4jDBC().deleteAllNodes()
    except Exception as e:
        print('\033[91m'+"\n[ERR] Neo4j DB didn't responded to the connect request !!"+'\033[0m')
        print('\033[91m'+"\t>> Check the port number on which the DB is active"+'\033[0m')
        # print('\033[93m'+e+'\033[0m')
        sys.exit()


'''
# ---- First finding the node & if not found then create one ----
# Check if the subject node already exists
subject_exists = Subject.nodes.first_or_none(subject_name=entity_pair[0])
subject_node = None
if subject_exists == None:
    subject_node = Subject(subject_name=entity_pair[0], subject_type=entity_pair[3]).save()
else:
    subject_node = subject_exists

# Check if the object node already exists
object_exists = Object.nodes.first_or_none(object_name=entity_pair[2])
object_node = None
if object_exists == None:
    object_node = Object(object_name=entity_pair[2], object_type=entity_pair[4]).save()
else:
    object_node = object_exists
'''

'''
# Checking if the predicate already exists b/w the nodes.
if subject_node.predicate.is_connected(object_node):
        rels = subject_node.predicate.relationship(object_node)
        print(rels.relationType)
        relExist = False
        for rel in rels:
            if rel.relationType == entity_pair[1]:
                relExist = True
        if relExist == False:
            subject_node.predicate.connect(object_node, {'relationType': entity_pair[1]}).save()
'''