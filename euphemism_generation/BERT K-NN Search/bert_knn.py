import argparse
import json
import numpy as np

from bert_embedding import BertEmbedding
from collections import Counter
from sklearn.neighbors import KDTree
from tqdm.auto import tqdm


class ContextNeighborStorage:
    def __init__(self, sentences, model):
        self.sentences = sentences
        self.model = model

    def process_sentences(self):
        result = self.model(self.sentences)

        self.sentence_ids = []
        self.token_ids = []
        self.all_tokens = []
        all_embeddings = []
        for i, (toks, embs) in enumerate(tqdm(result)):
            for j, (tok, emb) in enumerate(zip(toks, embs)):
                self.sentence_ids.append(i)
                self.token_ids.append(j)
                self.all_tokens.append(tok)
                all_embeddings.append(emb)
        all_embeddings = np.stack(all_embeddings)
        # we normalize embeddings, so that euclidian distance is equivalent to cosine distance
        self.normed_embeddings = (all_embeddings.T / (all_embeddings**2).sum(axis=1) ** 0.5).T

    def build_search_index(self):
        # this takes some time
        self.indexer = KDTree(self.normed_embeddings)

    def query(self, query_sent, query_word, k=10, filter_same_word=False):
        toks, embs = self.model([query_sent])[0]

        found = False
        for tok, emb in zip(toks, embs):
            if tok == query_word:
                found = True
                break
        if not found:
            raise ValueError('The query word {} is not a single token in sentence {}'.format(query_word, toks))
        emb = emb / sum(emb**2)**0.5

        if filter_same_word:
            initial_k = max(k, 100)
        else:
            initial_k = k
        di, idx = self.indexer.query(emb.reshape(1, -1), k=initial_k)
        distances = []
        neighbors = []
        contexts = []
        for i, index in enumerate(idx.ravel()):
            token = self.all_tokens[index]
            if filter_same_word and (query_word in token or token in query_word):
                continue
            distances.append(di.ravel()[i])
            neighbors.append(token)
            contexts.append(self.sentences[self.sentence_ids[index]])
            if len(distances) == k:
                break
        return distances, neighbors, contexts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs BERT KNN embedding")
    parser.add_argument("-y", "--year", type=int,
                        help="Year of Gab dataset from 2016-08 to 2018-10")
    parser.add_argument("-m", "--month", type=int,
                        help="Month of Gab dataset from 2016-08 to 2018-10")
    args = parser.parse_args()

    YEAR = args.year
    MONTH = args.month

    with open(f"./body_en_{YEAR}-{MONTH:02d}.csv", "r") as f:
        lines = f.readlines()
    all_sentences = np.asarray(lines)

    BERT_MODEL = BertEmbedding()
    storage = ContextNeighborStorage(sentences=all_sentences, model=BERT_MODEL)
    storage.process_sentences()
    storage.build_search_index()

    print("Embeddings processed successfully")

    with open(f"sentences_banned_{YEAR}_{MONTH:02d}.json", "w") as f:
        banned_sentences = json.load(f)
    
    euphemisms = {}
    for banned_word, sentences in banned_sentences.items():
        ctr_passed_sentences = 0
        ctr_total_checked = 0
        euphemisms[banned_word] = Counter()

        for sentence in sentences:
            if ctr_passed_sentences >= 100 or ctr_total_checked >= 1000:
                break
            ctr_total_checked += 1

            try:
                distances, neighbors, contexts = storage.query(query_sent=sentence,
                                                               query_word=banned_word,
                                                               k=5,
                                                               filter_same_word=True)
                for w in neighbors:
                    euphemisms[banned_word][w] += 1
                ctr_passed_sentences += 1
            except Exception as e:
                continue
    
    print("Euphemisms generated successfully")

    finalized_top_10 = {}
    for banned_word, euphemism_counter in euphemisms.items():
        if len(euphemism_counter) > 0:
            finalized_top_10[banned_word] = euphemism_counter.most_common(10)
        else:
            finalized_top_10[banned_word] = {}
    
    with open(f"euphemisms_knn_{YEAR}_{MONTH:02d}.json", "w") as f:
        json.dump(finalized_top_10, f)

    print("Top 10 euphemisms captured")
