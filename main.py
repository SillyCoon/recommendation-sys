import recommendation_class as rcm
import csv
import numpy as np

data = []
context_day = []
context_place = []

with open("data/data.csv", "r") as dt:
    reader = csv.reader(dt, quoting=csv.QUOTE_ALL)
    for row in reader:
        data.append(row)

with open("data/context_day.csv", 'r') as dt:
    reader = csv.reader(dt, quoting=csv.QUOTE_ALL)
    for row in reader:
        context_day.append(row)

with open("data/context_place.csv", 'r') as dt:
    reader = csv.reader(dt, quoting=csv.QUOTE_ALL)
    for row in reader:
        context_place.append(row)

data.pop(0)
context_place.pop(0)
context_day.pop(0)

for i in range(0, len(data)):
    data[i].pop(0)
    context_place[i].pop(0)
    context_day[i].pop(0)
    for j in range(0, len(data[0])):
        data[i][j] = data[i][j].lstrip()

recommendation = rcm.Recommendation(data, context_day, context_place)
#recommendation.fillEmpty()
recommendation.debugging()
