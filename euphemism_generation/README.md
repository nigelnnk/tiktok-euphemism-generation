# Environments

## Masked Language Modelling
Refer to `mlm_environment.yml`. This method mainly relies on huggingface's transformers library. 

## KNN Embedding
This uses a depreciated library `bert-embeddings`. Thus, it would be difficult to set up using conda. A reproducible environment would be to use python=3.7 and then run `pip install bert-embeddings`. 


# Notable Files

## euphemism_generation\BERT K-NN Search\100000_VERSION_BERT_KNN_Search.ipynb
This jupyter notebook has been used to easily explore/test our method through google colab. It will output the top_10_100000_corpus.json file.