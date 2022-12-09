import pandas as pd
import re
import string
import random
import itertools
from TikTokApi import TikTokApi

api = TikTokApi(custom_verifyFp = '')

def loadData(path):
    df = pd.read_csv(path)
    wordsToExamine = list(df['words'])
    return wordsToExamine

def removeVowel(word):
    vowels = ['a', 'e', 'i', 'o', 'u']
    rem_words = []
    chars = list(str.lower(word))
        # Get indexes of characters that are changeable
    idxToChange = []
    for idx, char in enumerate(chars):
        if char in vowels:
            idxToChange.append(idx)

    for L in range(1, min(3, len(idxToChange) + 1)):
        for subset in itertools.combinations(idxToChange, L):
            chars = list(str.lower(word))
            print(list(subset))
            for idx in list(subset):
                chars[idx] = ''

            rem_words.append(''.join(chars))

    return rem_words

def duplicateLast(word, max_dup = 4):
    dup_words = []
    chars = list(str.lower(word))
    last_char = chars[-1]
    for i in range(1, max_dup + 1):
        chars.append(last_char)
        dup_words.append(''.join(chars))

    return dup_words

def generateLexVar(word):
    lexVar = removeVowel(word) + duplicateLast(word)
    return set(lexVar)

def baseline_trial():
    print(f"Running baseline, lexvar")
    word_list = loadData('./CS8803 - DSN/baseline/banned_keywords.csv')
    banned_keywords = []
    df_construct_arr = []
    words_tested = []
    for word in word_list:
        wordToTest = generateLexVar(word)
        print(wordToTest)
        for wordT in wordToTest:
            words_tested.append(wordT)
            try:
                # info_full() is not used as this is mainly for logging purposes
                df_construct_arr.append(api.hashtag(wordT).info())
                print(f"{wordT} is not a banned keyword")
            except Exception as e:
                print(e)
                print(f"{wordT} is a banned keyword")
                banned_keywords.append(wordT)

    results = pd.DataFrame(df_construct_arr)
    results["videoCount"] = results.apply(lambda row: row["stats"]["videoCount"], axis=1)
    results["viewCount"] = results.apply(lambda row: row["stats"]["viewCount"], axis=1)
    results = results.drop("stats", axis=1)
    results.to_csv(f'./CS8803 - DSN/baseline/nonbanned_hate_lexvar.csv')

    with open(f'./CS8803 - DSN/baseline/banned_hate_lexvar.csv', "w") as f:
        f.write("\n".join(banned_keywords))


if __name__ == "__main__":
    baseline_trial()



        





