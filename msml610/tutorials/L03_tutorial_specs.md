# Knowledge Representation Notebooks - Specifications

## Overview
This document outlines 5 Jupyter notebooks designed to explore key topics from
**Lesson 03: Knowledge Representation** (MSML610). Each notebook bridges theory
and practice, with hands-on implementation and interactive visualization

## 1. Interactive Logic Explorer

### Goal
Students gain intuitive understanding of propositional logic by building and
analyzing logical formulas, truth tables, and inference rules. Explore the
relationship between syntax, semantics, and computation

### Learning Objectives
- Construct propositional formulas and evaluate truth values
- Enumerate all models and check entailment
- Understand SAT solving and computational complexity
- Visualize how expressiveness and tractability trade off

### Core Concepts
- Propositional logic syntax (operators: ¬, ∧, ∨, ⟹, ⟺)
- Semantics via truth tables and model interpretation
- Inference rules (Modus Ponens, Modus Tollens, Resolution)
- Model checking algorithm (sound and complete)
- Satisfiability and NP-completeness

### Key Packages
- **sympy**: symbolic logic, propositional formula manipulation
- **python-sat**: SAT solver backends

### Learning Activities
1. Build formulas interactively: `(Rain ∧ Cold) ∨ Sunny`
2. Generate and display truth tables for arbitrary formulas
3. Test entailment between two formulas: does KB ⊨ α?
4. Explore inference rules (modus ponens, resolution)
5. Measure SAT solver complexity as # variables increases
6. Interactive "Wumpus World" knowledge base reasoning

## 2. Ontology Design & Reasoning Workshop

### Goal
Students design a formal ontology from scratch, define reasoning tasks, and
implement core inference operations. Understand the structure-semantics
relationship in knowledge representation

### Learning Objectives
- Define ontologies using classes, individuals, properties, axioms
- Implement subsumption checking and classification
- Check consistency and satisfiability of concepts
- Perform instance checking and property inheritance
- Query and retrieve knowledge from ontologies

### Core Concepts
- Ontology components (classes, individuals, properties, constraints,
  hierarchies)
- Description logic (ALC basics, SHOIN expressiveness)
- Reasoning tasks (subsumption, satisfiability, classification, instance
  checking)
- Semantic web foundations (OWL, RDF)
- Grounding and interpretation

### Key Packages
- **owlready2**: OWL ontology construction and reasoning
- **rdflib**: RDF/OWL serialization and querying
- **networkx**: graph operations, hierarchy traversal
- **pyvis**: ontology visualization

### Learning Activities
1. Build university ontology: `Student`, `Professor`, `Course`, `Department`
2. Define class hierarchies and properties
3. Add axioms and constraints
4. Check subsumption: is `PhDStudent` a `Student`?
5. Perform instance checking: is Alice an instance of `Student`?
6. Classify new concepts into hierarchy automatically
7. Detect inconsistencies (e.g., conflicting axioms)
8. Visualize ontology as interactive class diagram

## 3. Rule-Based Expert System Simulator

### Goal
Students implement forward and backward chaining inference engines, encode
domain knowledge as rules, and explore how reasoning and uncertainty handling
work in practice

### Learning Objectives
- Implement forward chaining (data-driven) inference
- Implement backward chaining (goal-driven) inference
- Encode domain rules and facts clearly
- Understand conflict resolution strategies
- Reason under uncertainty (probabilistic rules)
- Debug and explain inference chains

### Core Concepts
- Rule-based systems (rules, facts, working memory, inference engine)
- Forward chaining (match-conflict resolution-act cycle)
- Backward chaining (goal reduction, proof search)
- Conflict resolution strategies
- Declarative vs procedural reasoning
- Uncertainty and probabilistic inference

### Key Packages
- **experta**: forward/backward chaining expert system framework
- **pyke**: logic programming engine (alternative)

### Learning Activities
1. Build medical diagnosis expert system:
   - Rules: `if fever AND rash then measles`
   - Facts: patient symptoms
   - Reasoning: derive diagnoses
2. Implement conflict resolution (specificity, recency, priority)
3. Trace inference chains step-by-step
4. Compare forward vs backward chaining on same KB
5. Add certainty factors to rules and propagate uncertainty
6. Visualize rule dependency graph and inference tree
7. Compare symbolic reasoning vs. learned ML classifier

## 4. Knowledge Graph Querying & Construction

### Goal
Students build and query knowledge graphs using RDF-style triples, connect to
real knowledge bases (DBpedia, WikiData), and implement graph-based reasoning
via path traversal

### Learning Objectives
- Model entities and relations as graphs (nodes, edges)
- Construct RDF triples and reason over them
- Query SPARQL endpoints (DBpedia, WikiData)
- Implement path-based reasoning and schema inference
- Visualize large graphs interactively
- Integrate multiple knowledge sources

### Core Concepts
- Knowledge graphs (entities, relations, RDF triples)
- Subject-Predicate-Object model
- SPARQL query language
- Semantic web (RDF, OWL, linked data)
- Schema inference and transitive relations
- WikiData and DBpedia structure
- Graph traversal for reasoning

### Key Packages
- **networkx**: graph construction and algorithms
- **SPARQLwrapper**: query remote SPARQL endpoints
- **rdflib**: RDF triple handling and in-memory graphs
- **pandas**: triple storage and result display
- **pyvis**: interactive large-scale graph visualization
- **requests**: WikiData JSON API calls

### Learning Activities
1. Build small university knowledge graph manually
   - Entities: Alice, Bob, CS101, ComputerScience
   - Relations: `takesCourse`, `teachesCourse`, `belongsToDepartment`
2. Query the graph: "Find all students in ComputerScience"
3. Implement transitive relations: `ancestorOf` via path traversal
4. Query DBpedia: "Which actors appeared in Inception?"
5. Query WikiData: "Find all Nobel Prize winners in Physics born in Germany"
6. Load and visualize subgraph interactively
7. Perform schema inference (entity typing, relation discovery)
8. Compare structured queries (SPARQL) vs. embedding-based search

## 5. Symbolic vs Neural Representations Hybrid

### Goal
Students compare how knowledge is encoded symbolically vs. as learned vector
representations, implement both approaches, and explore the
expressiveness-interpretability tradeoff

### Learning Objectives
- Access structured symbolic knowledge (WordNet, semantic networks)
- Generate and interpret word embeddings
- Implement similarity measures in both representations
- Compare symbolic inference vs. embedding-based "reasoning"
- Build neuro-symbolic hybrid systems
- Understand grounding: linking symbols to vectors

### Core Concepts
- Symbolic knowledge: discrete symbols, explicit structure
- Sub-symbolic knowledge: learned vectors, distributed representations
- Conceptual spaces: spatial geometry for concepts
- Word embeddings (Word2Vec, GloVe, contextual)
- Neuro-symbolic approaches: reasoning over learned concepts
- Similarity metrics in symbolic and vector spaces
- Grounding and interpretability

### Key Packages
- **nltk**: WordNet access, synsets, semantic similarity
- **networkx**: semantic network graph structure
- **scikit-learn**: embeddings, similarity metrics, dimensionality reduction
- **gensim**: Word2Vec, FastText embedding training
- **torch** / **tensorflow**: optional: graph neural networks
- **umap-learn**: embedding space visualization (t-SNE, UMAP)

### Learning Activities
1. Load WordNet and explore:
   - Synsets (synonym sets)
   - Is-a hierarchies
   - Part-whole relations
2. Compute semantic similarity (path-based, information-theoretic)
3. Train Word2Vec embeddings on text corpus
4. Compare symbolic hierarchy to embedding space:
   - Nearest neighbors in embedding space
   - Analogy reasoning: king - man + woman ≈ queen
5. Visualize 100-dim embeddings in 2D via t-SNE/UMAP
6. Implement simple neuro-symbolic reasoning:
   - Encode rules as constraints in embedding space
   - Retrieve facts via similarity search
   - Compare to symbolic retrieval
7. Measure interpretability: can you explain why two concepts are similar?
8. Discuss hybrid approaches: knowledge graphs + embeddings
