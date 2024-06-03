import csv
import random

import requests

DATASET = "https://github.com/aiplanethub/Datasets/raw/master/Amazon%20Top%2050%20Bestselling%20Books%202009%20-%202019.csv"

with requests.Session() as s:
    download = s.get(DATASET)
    decoded_content = download.content.decode("utf-8")

cr = csv.reader(decoded_content.splitlines(), delimiter=",")
rows = []
header = next(cr)
prev = ""

for row in cr:
    lowtitle = row[0].lower()
    if lowtitle != prev:
        rows.append(row[:2])
    prev = lowtitle

random.seed(40)
random.shuffle(rows)

OUTFILE = "data/books.csv"

with open(OUTFILE, "w") as wf:
    cw = csv.writer(wf)
    cw.writerow(header[:2])
    for row in rows[:22]:
        cw.writerow(row)
