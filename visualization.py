'''
:: Process ::
1. Takes pandas dataframe from main.py
2. Graph is plotted using networkx
3. Graph can be queried uing specific node
'''

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class Visualization:

    @staticmethod
    def drawKnowledgeGraph(triplets:pd.DataFrame) -> None:
        k_graph = nx.from_pandas_edgelist(triplets, 'subject', 'object', create_using=nx.MultiDiGraph())
        node_deg = nx.degree(k_graph)
        layout = nx.spring_layout(k_graph, k=0.15, iterations=20)
        plt.figure(num=None, figsize=(120, 90), dpi=80)
        nx.draw_networkx(k_graph, 
            node_size=[int(deg[1]) * 500 for deg in node_deg],
            arrowsize=20,
            linewidths=1.5,
            pos=layout,
            edge_color='red',
            edgecolors='black',
            node_color='white',
        )
        labels = dict(zip(list(zip(triplets.subject, triplets.object)), triplets['relation'].tolist()))
        nx.draw_networkx_edge_labels(k_graph, pos=layout, edge_labels=labels, font_color='red')
        plt.axis('off')
        plt.show()

    @staticmethod
    def queryKnowledgeGraph(triplets:pd.DataFrame, node:str) -> None:
        print("[INFO] Quering the Knowledge Graph for '{:s}' node".format(node))
        k_graph = nx.from_pandas_edgelist(triplets, 'subject', 'object', create_using=nx.MultiDiGraph())
        try:
            node = node.capitalize()
            edges = nx.dfs_successors(k_graph, node)
            nodes = []
            for k, v in edges.items():
                nodes.extend([k])
                nodes.extend(v)
            subgraph = k_graph.subgraph(nodes)
            layout = nx.spring_layout(subgraph)
            node_deg = nx.degree(subgraph)
            plt.figure(num=None, figsize=(120, 90), dpi=80)
            nx.draw_networkx(subgraph,
                node_size=[int(deg[1]) * 500 for deg in node_deg],
                arrowsize=20,
                linewidths=1.5,
                pos=layout,
                edge_color='red',
                edgecolors='black',
                node_color='white'
            )
            labels = dict(zip((list(zip(triplets.subject, triplets.object))), triplets['relation'].tolist()))
            edges = tuple(subgraph.out_edges(data=False))
            sublabels = {k: labels[k] for k in edges}
            nx.draw_networkx_edge_labels(subgraph, pos=layout, edge_labels=sublabels, font_color='red')
            plt.axis('off')
            plt.show()
        except Exception as e:
            print('\033[91m'+"[ERR] The node which you are searching doesn't exist in the Graph !!"+'\033[0m')
            # print('\033[93m'+e+'\033[0m')


if __name__ == "__main__":
    csv_file_name = "./textual_data/triplet_data.csv"
    try:
        data = pd.read_csv(csv_file_name)
        # Complete Knowledge Graph
        Visualization.drawKnowledgeGraph(data)
        # Quering for "Albert Einstein" node
        Visualization.queryKnowledgeGraph(data, "Albert Einstein")
    except IOError:
        print('\033[91m'+"\n[ERR] CSV file with the name '{:s}' doesn't exists !!".format(csv_file_name)+'\033[0m')
