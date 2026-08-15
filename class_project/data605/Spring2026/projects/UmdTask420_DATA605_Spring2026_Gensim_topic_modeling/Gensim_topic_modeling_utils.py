"""
Utility functions for LDA Topic Modeling using Gensim

Import as:

import Gensim_topic_modeling_utils as topic_utils 
"""
import warnings
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt 

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from gensim import corpora
from gensim.models import LdaModel, CoherenceModel

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from nltk.corpus import reuters


pyLDAvis.enable_notebook()

from transformers import pipeline

# #############################################################################
# Setup
# #############################################################################

def download_nltk_data():
    packages = ['punkt', 'stopwords', 'wordnet', 'punkt_tab', 'omw-1.4', 'reuters']
    for pkg in packages:
        nltk.download(pkg, quiet=True)

def sample_dataset():
    categories = ['trade', 'retail', 'cpu']
    rows = []
    for cat in categories:
        files = reuters.fileids(categories=cat)[:20]
        for f in files:
            raw  = reuters.raw(f)
            lines   = raw.strip().split('\n')
            title   = lines[0].strip()
            content = ' '.join(lines[1:]).strip()
            rows.append({
                'title'        : title,
                'content'      : content,
                'topic_actual' : cat
            })

    sample_df = pd.DataFrame(rows)
    sample_df = sample_df.drop_duplicates(subset='content').reset_index(drop=True)
    return sample_df


# #############################################################################
# Pre-processing
# #############################################################################

def get_stopwords():
    """
    Return set of NLTK stopwords.
    """
    return set(stopwords.words('english'))

def preprocess_text(text, stop_words, lemmatizer):
    """
    Return tokenized text after performing lemmatization and removing stop words.

    :param text: raw text to be tokenized
    :param stop_words: list of stop words to be removed from text
    :param lemmatizer: WordNetLemmatizer object for lemmatization 
    :return: cleaned tokens 
    """
    tokens = word_tokenize(str(text).lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens

def preprocess_corpus(texts):
    """
    Preprocess a list of texts into tokens.

    :param texts: list of texts to be preprocessed 
    :return: list of text tokens 
    """
    stop_words = get_stopwords()
    lemmatizer = WordNetLemmatizer()
    return [preprocess_text(text, stop_words, lemmatizer) for text in texts]

# #############################################################################
# Dictionary and Corpus 
# #############################################################################

def build_dictionary(docs, no_below=15, no_above=0.30, keep_n=2000):
    """
    Build and filter a Gensim Dictionary from processed documents.

    :param processed_docs: list of token lists
    :param no_below: minimum document frequency
    :param no_above: maximum document frequency proportion
    :param keep_n: maximum vocabulary size
    :return: filtered gensim Dictionary
    """

    dictionary = corpora.Dictionary(docs)
    print(f"Vocabulary before filtering : {len(dictionary)}")
    dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=keep_n)
    print(f"Vocabulary after filtering  : {len(dictionary)}")
    return dictionary

def build_corpus(docs, dictionary):
    """
    Convert processed documents to bag-of-words corpus.

    :param docs: list of token lists
    :param dictionary: gensim Dictionary
    :return: list of BoW vectors
    """
    return [dictionary.doc2bow(doc) for doc in docs]

# #############################################################################
# Model training
# #############################################################################


def compute_coherence_values(dictionary, corpus, docs, start, limit, step=5):
    """
    Compute coherence scores for a range of topic sizes.

    :param dictionary: gensim Dictionary
    :param corpus: BoW corpus
    :param docs: list of token lists 
    :param start: minimum number of topics
    :param limit: maximum number of topics
    :param step: step size between topic counts
    :return: tuple of (model_list, coherence_values)
    """
    models = []
    coherence_scores = []
    for i in range(start, limit, step):
        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=i,
            passes=15,
            alpha='auto',
            random_state=42
        )
        models.append(lda_model)
        coherence_model = CoherenceModel(
            model=lda_model,
            texts=docs,
            dictionary=dictionary,
            coherence='c_v'
        )
        score = coherence_model.get_coherence()
        coherence_scores.append(score)
    return models, coherence_scores

def train_lda_model(corpus, dictionary, num_topics, passes=20, iterations=400, random_state=42):
    """
    Train a Gensim LDA model.

    :param corpus: BoW corpus
    :param dictionary: gensim Dictionary
    :param num_topics: number of topics to discover
    :param passes: number of training passes
    :param iterations: number of iterations per pass
    :param random_state: random seed for reproducibility
    :return: trained LdaModel
    """
    model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=passes,
        iterations=iterations,
        alpha='auto',
        eta='auto',
        eval_every=None,
        random_state=random_state
    )
    print(f"LDA model trained with {num_topics} topics")
    return model


# #############################################################################
# Topic Inspection 
# #############################################################################

def inspect_topics(model, corpus, df, title_column, num_topics=10, num_words=5, num_docs=5):
    """
    Print top words and representative documents for each topic.

    :param model: trained LDA model
    :param corpus: BoW corpus
    :param df: pandas DataFrame with article data
    :param num_topics: number of topics to inspect
    :param num_words: number of top words to show per topic
    :param num_docs: number of representative docs to show per topic
    """
    doc_topics = []
    for i, doc_bow in enumerate(corpus):
        topic_dist = model.get_document_topics(doc_bow, minimum_probability=0)
        dominant_topic, confidence = max(topic_dist, key=lambda x: x[1])
        doc_topics.append({
            'doc_index'      : i,
            'dominant_topic' : dominant_topic,
            'confidence'     : confidence
        })
    topic_df = pd.DataFrame(doc_topics)
    for topic_id in range(num_topics):
        print(f"{'='*55}")
        print(f"  TOPIC {topic_id}")
        print(f"{'='*55}")
        
        print(f"\n  Top {num_words} words:")
        words = model.show_topic(topic_id, topn=num_words)
        for word, weight in words:
            print(f"    {weight:.4f}  - {word}")
        
        topic_docs = topic_df[topic_df['dominant_topic'] == topic_id]\
                     .sort_values('confidence', ascending=False)\
                     .head(num_docs)
        
        print(f"\n  Top {num_docs} representative articles:")
        if topic_docs.empty:
            print("    No documents assigned to this topic.")
        else:
            for rank, (_, row) in enumerate(topic_docs.iterrows(), 1):
                idx        = row['doc_index']
                confidence = row['confidence']
                title      = df.iloc[int(idx)][title_column]
                print(f"    {rank}. [{confidence:.2f}] {title}")
        
        print()


# #############################################################################
# Topic Assignment 
# #############################################################################

def get_dominant_topic(doc_bow, model):
    """
    Get the dominant topic and confidence for a single document.

    :param doc_bow: BoW representation of document
    :param model: trained LDA model
    :return: tuple of (dominant_topic_id, confidence)
    """
    topic_dist = model.get_document_topics(doc_bow, minimum_probability=0)
    return max(topic_dist, key=lambda x: x[1])

def assign_topics(df, corpus, model, topic_labels=None):
    """
    Assign dominant topic, confidence and label to every document.

    :param df: pandas DataFrame containing articles
    :param corpus: BoW corpus aligned with df
    :param model: trained LDA model
    :param topic_labels: dict mapping topic_id to label string
    :return: DataFrame with cluster_id, topic_confidence, topic_label columns
    """
    df = df.copy()
    results = [get_dominant_topic(doc, model) for doc in corpus]

    df['cluster_id']        = [r[0] for r in results]
    df['topic_confidence']  = [round(r[1], 4) for r in results]

    if topic_labels:
        df['topic_label'] = df['cluster_id'].map(topic_labels)
    else:
        df['topic_label'] = df['cluster_id'].astype(str)

    return df   

# #############################################################################
# Topic visualization 
# #############################################################################

def get_pyldavis_visualization(model, corpus, dictionary, mds='mmds', sort_topics=False):
    """
    Prepare and display pyLDAvis interactive visualization.

    :param model: trained LDA model
    :param corpus: BoW corpus
    :param dictionary: gensim Dictionary
    :param mds: dimensionality reduction method 
    :param sort_topics: whether to sort topics by prevalence
    :return: pyLDAvis PreparedData object
    """

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        vis = gensimvis.prepare(
            topic_model=model,
            corpus=corpus,
            dictionary=dictionary,
            mds=mds,
            sort_topics=sort_topics
        )

    return vis

# #############################################################################
# Sentiment Analysis
# #############################################################################

def load_sentiment_model():
    """
    Load RoBERTa sentiment analysis pipeline

    :return: transformers sentiment analysis pipeline 
    """
    sentiment_analysis = pipeline(
        'sentiment-analysis',
        model='cardiffnlp/twitter-roberta-base-sentiment-latest',
        truncation=True,
        max_length=512
        )
    return sentiment_analysis

def get_sentiment(text, sentiment_pipeline):
    """
    Process sentiment label, sentiment score, and confidence score for each text

    :param text: raw text string to analyse 
    :param sentiment_pipeline: RoBERTa sentiment analysis pipeline 
    :return: dictionary with sentiment label, sentiment_confidence, and sentiment_score
    """
    try:
        result = sentiment_pipeline(str(text)[:512])[0]
        label = result['label'].lower()
        score = result['score']
        if label == "positive":
            compound = score
        elif label == "negative":
            compound = -score
        else:
            compound = 0.0 
        return pd.Series({
            'sentiment_label'     : label,
            'sentiment_confidence': round(score, 4),
            'sentiment_score'     : round(compound, 4)
        }) 
    except Exception as e:
        print(f"Error: {e}")
        return pd.Series({
            'sentiment_label'     : 'neutral',
            'sentiment_confidence': 0.0,
            'sentiment_score'     : 0.0
        })
    
def get_sentiment_batch(texts, sentiment_pipeline, batch_size=32):
    """
    Run sentiment analysis in batches for faster processing.

    :param texts: list of text strings
    :param sentiment_pipeline: loaded HuggingFace pipeline
    :param batch_size: number of texts per batch
    :return: list of sentiment result dicts
    """
    truncated = [str(t)[:512] for t in texts]
    results   = []
    for i in range(0, len(truncated), batch_size):
        batch   = truncated[i:i + batch_size]
        outputs = sentiment_pipeline(batch)
        for result in outputs:
            label      = result['label'].lower()
            confidence = result['score']
            compound   = confidence if label == 'positive' \
                        else -confidence if label == 'negative' \
                        else 0.0
            results.append({
                'sentiment_label'     : label,
                'sentiment_confidence': round(confidence, 4),
                'sentiment_score'     : round(compound, 4)
            })
    return results 

def calculate_topic_polarity(df):
    polarity_data = df.groupby('topic_label').agg(
    strong_pos = ('sentiment_score', lambda x: (x >= 0.50).sum()),
    strong_neg = ('sentiment_score', lambda x: (x <= -0.50).sum()),
    total = ('sentiment_score', 'count'),
    std = ('sentiment_score', 'std')
    ).reset_index()
    polarity_data['pos_pct'] = (polarity_data['strong_pos'] / polarity_data['total'] * 100).round(1)
    polarity_data['neg_pct'] = (polarity_data['strong_neg'] / polarity_data['total'] * 100).round(1)
    polarity_data['true_polarity'] = polarity_data.apply(
        lambda row: 2 * min(row['strong_pos'], row['strong_neg']) / row['total'] * 100,
        axis=1
    ).round(1)
    polarity_data = polarity_data.sort_values('true_polarity', ascending=True)
    return polarity_data

# #############################################################################
# Sentiment visualizations 
# #############################################################################

def sentiment_dist_vis(df):
    """
    Calculate sentiment distribution for each topic for visualization 

    :param df: Pandas DataFrame consisting topic labels, sentiment scores, etc. 
    :return: Matplotlib bar chart visualization 
    """
    sentiment_by_topic = df.groupby(['topic_label', 'sentiment_label']).size().unstack(fill_value=0)
    sentiment_by_topic['total'] = sentiment_by_topic.sum(axis=1)
    sentiment_by_topic['pos_pct'] = (sentiment_by_topic['positive'] / sentiment_by_topic['total'] * 100).round(1)
    sentiment_by_topic['neg_pct'] = (sentiment_by_topic['negative'] / sentiment_by_topic['total'] * 100).round(1)
    sentiment_by_topic['neu_pct'] = (sentiment_by_topic['neutral']  / sentiment_by_topic['total'] * 100).round(1)
    sorted_df = sentiment_by_topic.sort_values('pos_pct', ascending=True)
    topics = sorted_df.index

    fig, ax = plt.subplots(figsize=(15,5))
    y = np.arange(len(topics))
    ax.barh(y, sorted_df['pos_pct'], label='Positive', color='#1D9E75')
    ax.barh(y, sorted_df['neu_pct'], left=sorted_df['pos_pct'], label='Neutral', color='#B4B2A9')
    ax.barh(y, sorted_df['neg_pct'], left=[p + n for p, n in zip(sorted_df['pos_pct'], sorted_df['neu_pct'])], label='Negative', color='#D85A30')
    ax.set_yticks(y)
    ax.set_yticklabels(topics, fontsize=11)
    ax.set_xlabel('Percentage (%)', fontsize=11)
    ax.set_title('Sentiment distribution by topic', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlim(0, 100)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.legend(loc='upper right', bbox_to_anchor=(1.12, 1), frameon=False, fontsize=10)
    return fig 

def topic_size_sentiment_vis(df):
    """
    Visualizing topic size and sentiment together  

    :param df: Pandas DataFrame consisting topic labels, sentiment scores, etc. 
    :return: Matplotlib bubble chart visualization 
    """
    bubble_data = df.groupby('topic_label').agg(sentiment=('sentiment_score', 'mean'), count=('sentiment_score', 'count')).reset_index()
    topics = list(bubble_data['topic_label'])
    scores = list(bubble_data['sentiment'])
    counts = list(bubble_data['count'])
    y = np.arange(len(topics))
    colors = ['#1D9E75' if s > 0.05 else '#D85A30' if s < -0.05 else '#B4B2A9' for s in scores]
    fig, ax = plt.subplots(figsize=(15,5))
    ax.vlines(y, 0, scores, colors=colors, linestyle='--')
    ax.axhline(y=0, color='#B4B2A9', linewidth=1, alpha=0.6)
    ax.scatter(y, scores, s=counts, c=colors, alpha=0.85, edgecolors=colors)
    ax.set_xticks(y)
    ax.set_xticklabels([t.replace('_', ' ').title() for t in topics],
                        rotation=30, ha='right', fontsize=10)
    ax.set_ylabel('Average sentiment score', fontsize=11)
    ax.set_title('Topic sentiment and size', fontsize=13, fontweight='bold')
    ax.set_xlabel('Topics', fontsize=11)
    return fig 

def topic_polarity_vis(polarity_data):
    """
    Visualizing topic polarity

    :param polarity_data: Pandas DataFrame consisting topic polarity score. 
    :return: Matplotlib chart visualization 
    """
    topics = [t.replace('_', ' ').title() for t in polarity_data['topic_label']]
    y = np.arange(len(topics))

    fig, ax = plt.subplots(figsize=(15, 6))
    ax.barh(y, -polarity_data['neg_pct'], height=0.6, color='#D85A30', alpha=0.85, label='Strongly negative (≤ -0.5)', edgecolor='none')
    ax.barh(y, polarity_data['pos_pct'], height=0.6, color='#1D9E75', alpha=0.85, label='Strongly positive (≥ +0.5)', edgecolor='none')
    for i, tp in enumerate(polarity_data['true_polarity']):
        ax.text(polarity_data['pos_pct'].iloc[i] + 1, y[i], f'{tp:.1f}%', va='center', fontsize=9, color='#D85A30' if tp > 20 else '#555')
    ax.axvline(x=0, color='#888', linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(topics, fontsize=11)
    ax.set_xlabel('% of articles with extreme sentiment scores', fontsize=11)
    ax.set_title('Polar topics with both extremely positive and negative articles',
                fontsize=12)
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{abs(int(x))}%')
    )
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), fontsize=10)
    return fig 