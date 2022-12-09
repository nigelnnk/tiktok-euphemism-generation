import pandas as pd
import re
import string
import random
from TikTokApi import TikTokApi

api = TikTokApi(custom_verifyFp = '')

def load_data(path):
    df = pd.read_csv(path)
    wordsToExamine = list(df['words'])
    return wordsToExamine

def generateLeet(word, numChanges, numTrials = 10):
    '''
    leetDict = {'a': ['@', '4'], 'b': ['8', 'ß', '6'], 'c': ['¢', 'ç', 'ć', 'č'],
                'e': ['3', '&', '£', '€', 'ë'], 'h': ['#'], 'i': ['1', '|', '!', 'í'],
                'o': ['0', 'ø', 'ö'], 's': ['$', 'ś', 'š', 'ß', '5'], 't': ['7'], 'u': ['û', 'ü', 'ù', 'ú']}
    '''
    leetDict = {'a': ['4'], 'b': ['8', 'ß', '6'], 'c': ['ç', 'ć', 'č'],
                'e': ['3', 'ë'], 'i': ['1', '|', 'í'],
                'o': ['0', 'ø', 'ö'], 's': ['ś', 'š', 'ß', '5'], 't': ['7'], 'u': ['û', 'ü', 'ù', 'ú']}
    leetWords = []

    for trial in range(numTrials):
        # Turn word into char array
        chars = list(str.lower(word))

        # Get indexes of characters that are changeable
        idxToChange = []
        for idx, char in enumerate(chars):
            if char in leetDict.keys():
                idxToChange.append(idx)

        try:
            sampledIndex = random.sample(idxToChange, numChanges)
        except:
            sampledIndex = random.sample(idxToChange, len(idxToChange))

        for idx in sampledIndex:
            charToChange = chars[idx]
            chars[idx] = random.sample(leetDict[charToChange], 1)[0]

        leetWords.append(''.join(chars))

    return set(leetWords)

def baseline_trial(numChanges):
    print(f"Running baseline, leet with numChanges = {numChanges}")
    word_list = load_data('./CS8803 - DSN/baseline/banned_keywords.csv')
    banned_keywords = []
    df_construct_arr = []
    words_tested = []
    for word in word_list:
        wordToTest = generateLeet(word, numChanges, 10 * numChanges)
        print(wordToTest)
        for wordT in wordToTest:
            words_tested.append(wordT)
            try:
                # info_full() is not used as this is mainly for logging purposes
                df_construct_arr.append(api.hashtag(wordT).info())
                print(f"{wordT} is not a banned keyword")
            except:
                print(f"{wordT} is a banned keyword")
                banned_keywords.append(wordT)

    results = pd.DataFrame(df_construct_arr)
    results["videoCount"] = results.apply(lambda row: row["stats"]["videoCount"], axis=1)
    results["viewCount"] = results.apply(lambda row: row["stats"]["viewCount"], axis=1)
    results = results.drop("stats", axis=1)
    results.to_csv(f'./CS8803 - DSN/baseline/nonbanned_hate_leet_{numChanges}.csv')

    with open(f'./CS8803 - DSN/baseline/banned_hate_leet_{numChanges}.csv', "w") as f:
        f.write("\n".join(banned_keywords))


if __name__ == "__main__":
    for i in range(2, 4):
        if i == 0:
            continue
        baseline_trial(i)



        





