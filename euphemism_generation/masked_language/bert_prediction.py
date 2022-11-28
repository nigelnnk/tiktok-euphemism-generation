import argparse
import json
from collections import Counter
from transformers import pipeline, AutoTokenizer


parser = argparse.ArgumentParser(description="Downloads cleaned English text body from Gab dataset")
parser.add_argument("-y", "--year", type=int,
                    help="Year of Gab dataset from 2016-08 to 2018-10")
parser.add_argument("-m", "--month", type=int,
                    help="Month of Gab dataset from 2016-08 to 2018-10")
args = parser.parse_args()

YEAR = args.year
MONTH = args.month

with open(f"sentences_banned_{YEAR}_{MONTH:02d}.json", "r") as f:
    sen_dict = json.load(f)

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased', truncation=True, model_max_length=512)
unmasker = pipeline('fill-mask', model='distilbert-base-uncased', tokenizer=tokenizer)

ans = {}
for banword in sen_dict:
    ans[banword] = Counter()
    sentences = sen_dict[banword]
    for s in sentences:
        masked_s = s.lower().replace(banword, tokenizer.mask_token, 1)

        try:
            results = unmasker(masked_s)
        except:
            continue

        for r in results:
            ans[banword][r['token_str']] += 1
    print(f"{banword}:\t{ans[banword].most_common(10)}")

with open(f"euphemisms_{YEAR}_{MONTH:02d}.json", "w") as f:
    json.dump(ans, f)

