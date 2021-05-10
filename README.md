# Knowledge Graph with Neo4j

<p align="center">
    <a href="https://lgtm.com/projects/g/Dhyeythumar/Knowledge-Graph-with-Neo4j/alerts/">
      <img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/Dhyeythumar/Knowledge-Graph-with-Neo4j.svg?logo=lgtm&logoWidth=20&style=for-the-badge" />
    </a>
    <a href="https://lgtm.com/projects/g/Dhyeythumar/Knowledge-Graph-with-Neo4j/context:python">
      <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/Dhyeythumar/Knowledge-Graph-with-Neo4j.svg?logo=lgtm&logoWidth=20&style=for-the-badge" />
    </a>
</p>

<h4 align="center">
    Analyzing Knowledge Graph by scraping Wikipedia pages based on famous personalities.
</h4>

<h5 align="center">
    <a href="https://spacy.io/">spaCy</a>
    <span> ● </span>
    <a href="https://github.com/huggingface/neuralcoref">neuralcoref</a> by <a href="https://github.com/huggingface">huggingface</a>
    <span> ● </span>
    <a href="https://neo4j.com/">Neo4j DB</a>
    <span> ● </span>
    <a href="https://www.mongodb.com/cloud/atlas">MongoDB Atlas</a>
    <span> ● </span>
    <a href="https://networkx.org/">NetworkX</a>
</h5>


## What’s In This Document
- [**Introduction**](#introduction)
- [**Setup Instructions**](#setup-instructions)
- [**Getting Started**](#getting-started)
- [Abstract Idea and Problem](./implementation.md#abstract-idea-and-problem)
- [Tradeoff between RAM size and DB access time with the solution](./implementation.md#tradeoff-between-ram-size-and-db-access-time-with-the-solution)
- [Implementation](./implementation.md#implementation)
- [Future Development](./implementation.md#future-development)
- [Results](./implementation.md#results)
- [**License**](#license)
- [**Acknowledgements**](#acknowledgements)


## Introduction
This repo aims to analyze the Wikipedia pages to understand and extract the information crux, which can make our web searches a lot easier. I am exploiting the opportunity to mine the massive information available on famous personalities around the world on the internet (through Wikipedia pages).

I have used the Knowledge Graph technique to analyze, discover patterns and trends. This repo makes use of spaCy for natural language processing and its compiled language model (only for English textual data) for named entities recognition (NER) and extraction. And it also makes use of the "Fast Coreference Resolution in spaCy with Neural Networks" package neuralcoref to resolve the referencing issues while extracting NER. The extracted knowledge graph is finally stored in a graph database Neo4j for better visualization of links between the collected information.


## Setup Instructions
- Clone this repo:
```bash
$ git clone https://github.com/Dhyeythumar/Knowledge-Graph-with-Neo4j.git
```

- Create and activate the python virtual environment (Use python 3.8.7):
```bash
$ virtualenv KG_env -p path/to/your/python/3.8/exe/file
$ KG_env\Scripts\activate
```

- Install the requirements:
```bash
$ cd Knowledge-Graph-with-Neo4j
$ pip install -r requirements.txt
```

- Install spaCy's [English language model](https://spacy.io/models/en):
```bash
$ python -m spacy download en_core_web_md
```

- Build the neuralcoref from the source code (because the package from PyPI is not compatible with spaCy's language model)
```bash
$ git clone https://github.com/huggingface/neuralcoref.git
$ cd neuralcoref
$ pip install -r requirements.txt
$ pip install -e .
```


## Getting Started
Run this project by just executing:
```bash
$ python main.py
```
With the above setting you are good to go ✌.

<br />
<h3>
But if you want a deeper understanding of how the project is implemented and what trade-off I faced while developing 😀, then check this <a href="./implementation.md">README file</a>. Other tables of contents are in that file.
</h3>
<br />


## License
Licensed under the [MIT License](./LICENSE).


## Acknowledgements
1. Medium article on ["Auto-Generated Knowledge Graphs"](https://towardsdatascience.com/auto-generated-knowledge-graphs-92ca99a81121) for Knowledge Graph implementation and visualization using networkx.
