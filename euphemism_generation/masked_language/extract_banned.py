import argparse
import pandas as pd
import re
import json


parser = argparse.ArgumentParser(description="Downloads cleaned English text body from Gab dataset")
parser.add_argument("-y", "--year", type=int,
                    help="Year of Gab dataset from 2016-08 to 2018-10")
parser.add_argument("-m", "--month", type=int,
                    help="Month of Gab dataset from 2016-08 to 2018-10")
args = parser.parse_args()

YEAR = args.year
MONTH = args.month

banned_words = pd.read_csv("./banned_keywords.csv", header=None).dropna().squeeze().tolist()
source_file = f"./body_en_{YEAR}-{MONTH:02d}.csv"
gab_body = pd.read_csv(source_file, header=None).dropna().squeeze().tolist()

ans = {}
for banword in banned_words:
    ans[banword] = []
    pattern = re.compile(r"\W+" + banword + r"\W+", re.IGNORECASE)
    for line in gab_body:
        if pattern.search(line):
            ans[banword].append(line)
    print(f"{banword}:\t{len(ans[banword])}")


with open(f"sentences_banned_{YEAR}_{MONTH:02d}.json", "w") as f:
    json.dump(ans, f, indent=0)
