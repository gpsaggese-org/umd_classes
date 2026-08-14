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
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Gensim: BBC News Data LDA Topic Modeling using Gensim

# %%
# %load_ext autoreload
# %autoreload 2

import logging
import Gensim_topic_modeling_utils as topic_utils 

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
# Importing libraries 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# # Data loading and cleaning
#
# Dataset used for this project is the BBC news data taken from Kaggle 
# https://www.kaggle.com/datasets/hgultekin/bbcnewsarchive 

# %%
# Loading BBC news dataset into a pandas dataframe 

df = pd.read_csv('bbc-news-data.csv',sep='\t')
df.head()

# %%
# Checking for duplicates 

df['title'].duplicated().sum()

# %%
# Dropping duplicates 

df = df.drop_duplicates(subset='title', keep='first').reset_index(drop=True)

# %%
df.info()

# %%
(df['content'] == "").sum()

# %%
# Plotting news category distribution

fig, ax = plt.subplots(figsize=(5, 5))
counts = df['category'].value_counts()
ax.pie(
    counts,
    labels    = counts.index,
    autopct   = '%1.1f%%',
    colors    = plt.cm.Pastel1.colors,
    startangle= 140,
    wedgeprops= dict(edgecolor='white', linewidth=1.5)
)
ax.set_title("News Category Distribution", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.show()

# %% [markdown]
# # Data Pre-processing
#
# Processing the data first as LDA cannot be implemented on raw data. This step involves cleaning and tokenizing texts followed by lemmatization and stop word removal. These tokens can then be processed by Gensim.

# %%
# Importing NLTK library along with stopwords, tokenzier and lemmatizer 
topic_utils.download_nltk_data()

# %%
# Tokenzing article content 

df['clean_tokens'] = topic_utils.preprocess_corpus(list(df['content']))

# %%
# Final cleaned dataset 

df.head()

# %% [markdown]
# # Topic Modeling
#
# The processed documents are used to create a dictionary and corpus which are needed for LDA to map each word to an integer as LDA cannot operate on strings.

# %%
# Creating word dictionary out of cleaned tokens 
# This will be used to build the LDA model

docs = list(df['clean_tokens'])
word_dict = topic_utils.build_dictionary(docs)

# %%
# Building corpus using BoW representation of the documents so LDA can work with the documents mathematically 

corpus = topic_utils.build_corpus(docs, word_dict)
print("BoW for doc 1: ", corpus[0])

# %%
# Getting coherence values of LDA models for topic sizes between 10 and 20 

models, scores = topic_utils.compute_coherence_values(word_dict, corpus, docs, start=10, limit=20, step=1)

# %%
# Coherence scores for each topic size 

score_dict = {}
for i, cv in enumerate(scores):
    score_dict[i+10] = cv
    print(f"Num topics: {i+10:2d} | Coherence: {cv:.4f}")


# %%
# Visualizing the coherence scores to pick the best topic size for the final model 

x = range(10,20)
best_topic = max(score_dict, key=score_dict.get)
plt.figure(figsize=(10,5))
plt.plot(x, scores, marker='o', color="#4287F7")
plt.axvline(x=best_topic, color='red', linestyle='--', label='best topic size')
plt.xlabel("Topic size")
plt.ylabel("Coherence Score")
plt.title("Coherence scores for given topic sizes")
plt.legend()
plt.show()

# %%
print(f"Best topic size: {best_topic} with coherence score {max(score_dict.values()):.4f}")

# %% [markdown]
# Hence, the best topic size is 10 as it gives the maximum coherence score of 0.56

# %%
# Building the final LDA model for topic size = 10 

lda_model = topic_utils.train_lda_model(corpus, word_dict, num_topics=10)

# %%
topic_utils.inspect_topics(lda_model, corpus, df, title_column="title")

# %%
# Defining topic labels for the 10 topics found by LDA 

topic_labels = {
    9: "government_labour",
    8: "laptop_computers",
    7: "search_engine",
    6: "gaming",
    5: "company_leaks",
    4: "spam_hackers",
    3: "cybersecurity",
    2: "broadband_net_services", 
    1: "mobile_advancement",
    0: "sports"
}

# %%
df = topic_utils.assign_topics(
    df           = df,
    corpus       = corpus,
    model        = lda_model,
    topic_labels = topic_labels
)

# %%
df.head()

# %%
# Visualizing topics with pyLDAvis

topic_utils.get_pyldavis_visualization(lda_model, corpus, word_dict)

# %% [markdown]
# The graph shows that topics 1 and 10 are huge and almost overlapping which means both topics cover similar themes and the model struggled to cleanly separate them. However, given that the topic 10 has top words like government, minister, labour, party and topic 1 has words related to UK sports, we can say these are indeed distinct topics. 

# %%
# Visualizing topic distribution 

topic_counts = df['topic_label'].value_counts()
plt.figure(figsize=(10,5))
plt.bar(topic_counts.index, topic_counts, color="#F3A7A0")
plt.xlabel("Topics")
plt.ylabel("Article count")
plt.xticks(rotation=45, ha='right')
plt.show()

# %% [markdown]
# As we also saw above, government_labour is the largest topic followed by sports. This matches with the distribution of the categories present in the original dataset where the largest category is goverment followed by sports.

# %%
# Visualizing topic confidence distribution

plt.figure(figsize=(10,5))
plt.hist(df['topic_confidence'], color="#58AB90")
plt.xlabel("Topic Confidence")
plt.ylabel("Count")
plt.title("Topic confidence distribution")
plt.show()

# %% [markdown]
# The distribution of the topic confidence shows that the majority of the documents fall within the 0.4 and 1.0 confidence range. As a result, the graph looks more like a plateau rather than a sharp right-skewed peak. This pattern is largely due the two dominating topics which account for nearly 62% of the dataset. Since BBC news articles frequently intersect multiple domains, LDA correctly captures this ambiguity through the majority of mid-range confidence scores. Topics that were easily distinguishable have a high confidence score between 0.8 and 1.0.

# %%
# Saving the topic assignment for downstream processing 

df.to_csv('processed/news_articles_topic_assignment.csv')

# %% [markdown]
# # Sentiment Analysis
#
# Sentiment analysis will reveal the tone of the topics which will indicate which topics are polar, which are neutral, and which topics lean towards a single sentiment. RoBERTa model is used for this purpose as the model is trained on news data and works well with longform articles. 

# %%
df = pd.read_csv('processed/news_articles_topic_assignment.csv')

# %%
df.head()

# %%
# Defining sentiment analysis model using RoBERTa 

sentiment_pipeline = topic_utils.load_sentiment_model()

# %%
# Getting sentiment label, score and confidence score for each article content 

results = topic_utils.get_sentiment_batch(df['content'].tolist(), sentiment_pipeline)
sentiment_result = pd.DataFrame(results)

# %%
df = pd.concat([df, sentiment_result], axis=1)

# %%
df.head()

# %%
# Visualising distribution of sentiment scores (left) and confidence score (right)

fig, ax = plt.subplots(1,2,figsize=(15,5))
ax[0].hist(df['sentiment_score'], color="#80CBF9")
ax[0].set_xlabel("Sentiment Scores")
ax[0].set_ylabel("Counts")
ax[0].set_title("Distribution of Compound Sentiment Scores")

ax[1].hist(df['sentiment_confidence'], color="#F98086")
ax[1].set_xlabel("Sentiment Confidence")
ax[1].set_ylabel("Counts")
ax[1].set_title("Distribution of Sentiment Confidence")
plt.show()

# %% [markdown]
# The sentiment scores show that while the majority of the articles are neutral, the rest are either extremely negative or extremely positive. The confidence score is between 0.45 to 0.80, most of the scores are mid to high range which means the model is moderately to highly confident in the classification. The visualization of topics vs sentiment will reveal if the topics themselves are polar or the extremely negative or positive articles are present in every topic.

# %%
df['sentiment_label'].value_counts()

# %%
# Visualizing % of each sentiment label within a topic 

dist_vis = topic_utils.sentiment_dist_vis(df)
plt.tight_layout()
plt.show()


# %% [markdown]
# Hence, broadband_net_services has mostly positive articles whereas company_leaks has around 50% negative and 50% neutral articles making it the only topic with no positive articles within it. Interestingly, neutral articles are dominant in topics with low to none positive articles i.e they are more neutral and negative. 

# %%
# Calculating average sentiment for each topic 

bubble_data = df.groupby('topic_label').agg(sentiment=('sentiment_score', 'mean'), count=('sentiment_score', 'count')).reset_index()
bubble_data

# %%
# Visualizing topic size x average sentiment 

topic_size_vis = topic_utils.topic_size_sentiment_vis(df)
plt.tight_layout()
plt.show()

# %% [markdown]
# The graph presents some interesting results. Government Labour is the largest topic and mean negative sentiment. Company leaks is a small topic however it is also the most negative meaning there are not many articles but when they are appear they are strongly negative. Similarly, broadband net services is a small topic but with the highest positive sentiment. Sports is also a large topic but with positive average sentiment. It is interesting to note that both the largest topics have polar sentiments but mid-range average sentiments. 
#
# The main takeaway here is that size does not correlate with the sentiment.

# %%
# Calculating the polarity of each topic i.e. percentage of extremely negative and extremely positive articles 
# Polarity is calculated using 2 × min(% strongly positive, % strongly negative) 

polarity_data = topic_utils.calculate_topic_polarity(df)

# %%
# Visualizing polarity of each topic 

topic_polarity_vis = topic_utils.topic_polarity_vis(polarity_data)
plt.tight_layout()
plt.show()

# %% [markdown]
# Interestingly, the Cybersecurity topic is a small topic however it has the highest polarity at 36.4% meaning 36.4% of the articles show genuine polarity i.e there are both extremely positive and negative articles. Sports and government labour are also interesting topics depicting polarity as both are the largest topics in the dataset. Company leaks, being the most negative topic only has extremely negative articles exhibiting no polarity.

# %% [markdown]
# # Result
#
# ## Topic Modeling 
#
# This project applied Latent Dirichlet Allocation (LDA) using Gensim to a dataset of 2000 BBC News articles, identifying 10 distinct topics through rigorous data preprocessing including tokenziation, stopword removal, lemmatization, and vocabulary filtering to approximately 2000 tokens. Optimal topic size was determined using coherence scores for each topic size between 10 and 20, picking the topic size with the highest coherence score which was 10 with the score of 0.53 which is reasonable for news dataset where articles might span multiple topics. The two dominant topics are Sports and Government Labour together amounting for over 60% of the dataset. The remaining topics are smaller but clearly distinct. 
#
# ## Sentiment Analysis 
#
# Sentiment analysis was done using RoBERTa as it is able to handle large news content for calculating sentiment. The sentiment distribution is trimodal with most of the articles being neutral, however, rest of the articles are either extremely negative or extremely positive Government Labour emerged as the largest yet negative topic, while tech-oriented topics such as Gaming, Broadband and Laptop Computers exhibited consistently positive sentiment. Polarity analysis, quantified as 2 × min(% strongly positive, % strongly negative), revealed that Cybersecurity (36.4%) and Search Engine (35.0%) were the most genuinely polarized topics with substantial representation on both extreme sentiments, whereas Company Leaks scored 0.0% polarity, confirming it as consistently negative rather than truly polarized.
#
