# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Gensim: LDA Topic Modeling using Gensim

# %%
# %load_ext autoreload
# %autoreload 2

import logging
import Gensim_topic_modeling_utils as topic_utils 


logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

_LOG.info("Setup complete")

# %%
import pandas as pd
import numpy as np

# %% [markdown]
# ## Text Pre-processing
#
# Before topic modeling, the text must be cleaned and converted into tokens which makes it easier for the model to understand the words
#
# - **Tokenization**: split text into individual words
# - **Stopword removal**: remove common words like "the", "is"
# - **Lemmatization**: reduce words to base form ("running" → "run")

# %%
topic_utils.download_nltk_data()

# %%
sample_df = topic_utils.sample_dataset()
sample_df.head()

# %%
sample_df.shape

# %%
# Preprocess all documents 
processed_docs = topic_utils.preprocess_corpus(list(sample_df['content']))

print("Output tokens of the first sample document: \n",processed_docs[0])

# %% [markdown]
# ## Word dictionary and corpus
#
# Gensim LDA requires two structures:
#
# - **Dictionary**: maps every unique token to an integer ID
# - **Corpus**: converts each document into a bag-of-words (BoW) vector, i.e. a list of `(token_id, count)` pairs
#
# Filtering the dictionary removes tokens that are too rare or too common,
# keeping only the most informative vocabulary.
#

# %%
# Build dictionary from processed documents
# no_below=2: token must appear in at least 2 docs
# no_above=0.85: token must not appear in more than 85% of docs
# keep_n=500: hard cap on vocabulary size
dictionary = topic_utils.build_dictionary(
    processed_docs,
    no_below=2,
    no_above=0.85,
    keep_n=500
)

# Convert each document to BoW representation
corpus = topic_utils.build_corpus(processed_docs, dictionary)

# Inspect BoW for first document
print("BoW for doc 1: \n", corpus[0])
# Each tuple is (token_id, count)

# %% [markdown]
# ## Coherence Evaluation and Topic Selection
#
# Choosing the right number of topics is critical. We use the **c_v coherence score** which measures how semantically similar the top words in each topic are.
#
# - Higher coherence → more interpretable topics
# - We train models for a range of topic counts and pick the one with the
#   highest coherence score
# - Look for a clear **peak** or **elbow** in the coherence curve

# %%
# Compute coherence for topic counts 2 through 6

model_list, coherence_values = topic_utils.compute_coherence_values(
    dictionary = dictionary,
    corpus     = corpus,
    docs    = processed_docs,
    start      = 2,
    limit      = 7,
    step       = 1
)

# Coherence scores for each topic size 

score_dict = {}
for i, cv in enumerate(coherence_values):
    score_dict[i+2] = cv
    print(f"Num topics: {i+2:2d} | Coherence: {cv:.4f}")

# %% [markdown]
# ## LDA Model Training
#
# Latent Dirichlet Allocation (LDA) is a generative probabilistic model that discovers hidden topics in a corpus. Each document is modelled as a mixture of topics, and each topic is modelled as a mixture of words.
#
# Key parameters:
# - **num_topics**: number of topics to discover
# - **passes**: number of full training passes over the corpus (more = better convergence)
# - **iterations**: number of E-step iterations per document per pass
# - **alpha**: document-topic distribution prior (`'auto'` = learned from data)
# - **eta**: topic-word distribution prior (`'auto'` = learned from data)

# %%
# Train LDA model with 3 topics on sample data
lda_model = topic_utils.train_lda_model(
    corpus     = corpus,
    dictionary = dictionary,
    num_topics = 3,
    passes     = 10,      
    iterations = 100
)

# Print top 5 words per topic
for idx, topic in lda_model.print_topics(num_words=5):
    _LOG.info("Topic %d: %s", idx, topic)

# %% [markdown]
# ## Topic Inspection and Labelling
#
# After training, topics need to be inspected manually as LDA only clusters the documents into topics but doesn't provide human understandable labels. Topic inspection here includes inspecting top words and representative documents per topic, then manually assign human-readable labels.
#
# Workflow:
# - `inspect_topics()`: read output, decide labels
# - Define `topic_labels` dict as `{topic_id: label}`
# - `assign_topics()`: adds columns to dataframe

# %%
# Step 1 — inspect topics, no labels needed yet
topic_utils.inspect_topics(
    model       = lda_model,
    corpus      = corpus,
    df   = sample_df,
    title_column='title',
    num_topics  = 3,
    num_words   = 5,
    num_docs    = 5
)

# %%
topic_labels = {
    0: 'Tech',
    1: 'Trade',
    2: 'Retail'
}

# %%
sample_df = topic_utils.assign_topics(
    df           = sample_df,
    corpus       = corpus,
    model        = lda_model,
    topic_labels = topic_labels
)

# %%
sample_df.head()

# %% [markdown]
# ## Topic Visualization with pyLDAvis
#
# pyLDAvis provides an interactive visualization of the LDA model with two panels:
#
# - **Left panel** — intertopic distance map. Each bubble is a topic, size
#   represents prevalence, distance represents similarity between topics
# - **Right panel** — top 30 most relevant terms for the selected topic
#
# Interpretation
# - Well-separated bubbles: distinct, high-quality topics
# - Overlapping bubbles: topics too similar 
# - Setting **λ = 0.6** shows the most meaningful word rankings

# %%
topic_utils.get_pyldavis_visualization(lda_model, corpus, dictionary)

# %%
