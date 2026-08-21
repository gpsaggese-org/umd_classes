# Ideas

## Differentiable Embeddings for Math and Code

Study differentiable embeddings in math and coding
- Can the correctness of a problem or a proof in math be determined by gradient descent?

## Predicting Sports Outcomes from Player-Level Features

Predict outcome of football and basketball using the same approach as the paper
https://drive.google.com/drive/folders/1GgW3PVQeMYRP3Bvqfk1AF78T6YlXINew

Download and find What are the features of each player in madden nfl
How can be used to predict game outcomes

## Hierarchical Training

Train a NN hierarchically, projecting the loss to each block, optimizing each block and then doing a single pass to connect all of them
https://claude.ai/share/000f840b-6a9f-4eb9-a5e9-3de6419bfe86

## Progressive Growing of Network Resolution and Structure

How to learn a NN using an approach similar to increasing resolution for pictures?
- Change the number of gradient dimensions as you go

Learn a NN changing also its structure as you go
- Find the "optimal" number of parameters given the corpus
- Make the architecture differentiable

## Optimal Quantization for Training Neural Networks

What is the right amount of quantization to use to train a NN (is it better to learn and then quantize of viceversa)
- What about -1, 0, 1
- What about fp4

What if we use layers that have different level of bit precision?

## Number Representations that Speed Up Gradient Descent

Is a special representation of numbers and operations that makes gradient descent faster
Eg integer va floating point, log, …

## Learned Optimal Embedding Encoding for a Corpus

Learn the "optimal" embedding encoding for a corpus (e.g., together with the weights) and see how much smaller is the NN
- Are the embeddings similar to the standard ones?

## Packing Multiple Integers per Word for SIMD

Pack more than one integer in a single word and do simd
- Probably already done?
- E.g., learn as streaming on FPGA on very large VLIW batches

## Learned Image and Video Compression via Adaptive Regions

Compress pictures using NN to learn patterns that occur all the times (pictures have certain characteristics)
- Same for movies

Can you compress an image better by using rectangles of different size instead of pixels?
- Post the approximation problem as a loss that can be solved by gradient descent

## Math Primitives for Neural Networks

What are different math primitives that can be used in a NN
- add, mul, relu

## Faster Autoregressive Generation via Word/Stem Chunks and Diffusion

How to make autoregressive NN faster? Use words and stems (caveman style), mix diffusion and autoregression (e.g., diffusion as first step and then patch up with autoregression

## Visualizing Model Weights and Gradients to Find Compressible Parts

Visualize weights from models
Visualize magnitude of gradient to understand what parts of the network are important or can be compressed
Use models from huggingface

## Homomorphic-Style Encryption of Neural Network Weights

Give me the weights, I transform them with my key, then I apply the key to the inputs and outputs to remove the transform (like private key encoding

## Survey of Open Problems Across ML, Causal AI, and Finance

What are the most important open problems in machine learning, statistical learning, causal ai, Bayesian statistics, finance, financial mathematics, defi, blockchain

## Distribution of Complexity Across Exponential-Complexity Problems

A problem is exponential complexity but how is the distribution of the complexity over problems?

## Explainability via Distillation into an Interpretable Form

Explainability as a form of regulation
- after fitting a nn distill one that can be interpreted

What formulation of NN can be explained?
- what if it's in the form of a python program

Study distillation procedures

## Removing and Externalizing Factual Knowledge from Neural Networks

How to remove info from a NN?

Remove all the facts and make pluggable memory for facts (eg just an LlM for facts)

## Knowledge Base Construction from Papers and Hacker News for LLMs

Create knowledge bases from papers and HN that can be used by LLMs

## Learned Confidence Scoring for Model Reasoning

Learning a model to teach the machine a confidence score about its thinking

## Wealth Redistribution Policy in an AI-Driven Abundance Economy

With AI creating unbounded amount of wealth, what to do?
- One idea is to recognize that there is luck in getting rich and just spread the weatlh
- Every person can only have at most $10M adjusted for inflation (this is enough to live a very nice life)
- Why rich people behave as man baby? https://news.ycombinator.com/item?id=49317760

## Survey of LLM Quantization Techniques

- What are the Python tools?
- What are the tradeoffs?
- What are the different approaches?
