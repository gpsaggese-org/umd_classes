Ideas

Study differentiable embeddings in math and coding
- Can the correctness of a problem or a proof in math be determined by gradient descent?

Predict outcome of football and basketball using the same approach as the paper
https://drive.google.com/drive/folders/1GgW3PVQeMYRP3Bvqfk1AF78T6YlXINew

## Hierarchical training
Train a NN hierarchically, projecting the loss to each block, optimizing each block and then doing a single pass to connect all of them
https://claude.ai/share/000f840b-6a9f-4eb9-a5e9-3de6419bfe86

## 
How to learn a NN using an approach similar to increasing resolution for pictures?
- Change the number of gradient dimensions as you go

Learn a NN changing also its structure as you go
- Find the “optimal” number of parameters given the corpus
- Make the architecture differentiable

## What is the right amount of quantization to use to train a NN (is it better to learn and then quantize of viceversa)
- What about -1, 0, 1
- What about fp4

What if we use layers that have different level of bit precision?

## Is a special representation of numbers and operations that makes gradient descent faster
Eg integer va floating point, log, …

## Learn the “optimal” embedding encoding for a corpus (e.g., together with the weights) and see how much smaller is the NN
- Are the embeddings similar to the standard ones?

## Pack more than one integer in a single word and do simd
- Probably already done?
- E.g., learn as streaming on FPGA on very large VLIW batches

## Compress pictures using NN to learn patterns that occur all the times (pictures have certain characteristics)
- Same for movies

Can you compress an image better by using rectangles of different size instead of pixels?
- Post the approximation problem as a loss that can be solved by gradient descent

## What are different math primitives that can be used in a NN
- add, mul, relu

## How to make autoregressive NN faster? Use words and stems (caveman style), mix diffusion and autoregression (e.g., diffusion as first step and then patch up with autoregression

Visualize weights from models
Visualize magnitude of gradient to understand what parts of the network are important or can be compressed
Use models from huggingface

Give me the weights, I transform them with my key, then I apply the key to the inputs and outputs to remove the transform (like private key encoding 

Download and find What are the features of each player in madden nfl
How can be used to predict game outcomes

What are the most important open problems in machine learning, statistical learning, causal ai, Bayesian statistics, finance, financial mathematics, defi, blockchain

A problem is exponential complexity but how is the distribution of the complexity over problems?

Explainability as a form of regulation 
- after fitting a nn distill one that can be interpreted

What formulation of NN can be explained?
- what if it’s in the form of a python program 

Study distillation procedures

How to remove info from a NN?

Remove all the facts and make pluggable memory for facts (eg just an LlM for facts)

Create knowledge bases from papers and HN that can be used by LLMs

Learning a model to teach the machine a confidence score about its thinking

With AI creating unbounded amount of wealth, what to do?
- One idea is to recognize that there is luck in getting rich and just spread the weatlh
- Every person can only have at most $10M adjusted for inflation (this is enough to live a very nice life)
- Why rich people behave as man baby? https://news.ycombinator.com/item?id=49317760

# Write a survey on LLM quantization techniques
- What are the Python tools?
- What are the tradeoffs?
- What are the different approaches?

