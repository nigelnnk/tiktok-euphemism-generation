import argparse
import pandas as pd
import requests
from cleantext import clean


parser = argparse.ArgumentParser(description="Downloads cleaned English text body from Gab dataset")
parser.add_argument("-y", "--year", type=int,
                    help="Year of Gab dataset from 2016-08 to 2018-10")
parser.add_argument("-m", "--month", type=int,
                    help="Month of Gab dataset from 2016-08 to 2018-10")
args = parser.parse_args()

YEAR = args.year
MONTH = args.month
filename = f"GABPOSTS_{YEAR}-{MONTH:02d}.xz"

r = requests.get(f"https://files.pushshift.io/gab/GABPOSTS_{YEAR}-{MONTH:02d}.xz")
with open(filename, "wb") as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
print("XZ dataset downloaded successfully")

with open(filename, "rb") as f:
    dataset = pd.read_json(f, lines=True, compression='xz', encoding_errors='ignore')

en_data = dataset.query("language == 'en'")
body = en_data["body"]
print(body.head())

cleaner = lambda x: clean(x,
    fix_unicode=True,               # fix various unicode errors
    to_ascii=True,                  # transliterate to closest ASCII representation
    lower=True,                     # lowercase text
    no_line_breaks=True,            # fully strip line breaks as opposed to only normalizing them
    no_urls=True,                   # replace all URLs with a special token
    no_emails=True,                 # replace all email addresses with a special token
    no_phone_numbers=True,          # replace all phone numbers with a special token
    no_numbers=True,                # replace all numbers with a special token
    no_digits=True,                 # replace all digits with a special token
    no_currency_symbols=True,       # replace all currency symbols with a special token
    no_punct=True,                  # remove punctuations
    replace_with_punct="",          # instead of removing punctuations you may replace them
    replace_with_url="",
    replace_with_email="",
    replace_with_phone_number="",
    replace_with_number="",
    replace_with_digit="",
    replace_with_currency_symbol="",
    lang="en"                       # set to 'de' for German special handling
)

cleaned_body = body.apply(cleaner)
print("Cleaned!")

cleaned_body.to_csv(f"./body_en_{YEAR}-{MONTH:02d}.csv", header=False, index=False)

print("Done!")
