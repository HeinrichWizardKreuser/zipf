import re
from operator import itemgetter
import sys
import pandas as pd
import matplotlib.pyplot as plt
from math import log

file_name = sys.argv[1]

frequency = {}
open_file = open(file_name, 'r')
file_to_string = open_file.read()
words = re.findall(r'(\b[A-Za-z][a-z]{2,9}\b)', file_to_string)

for word in words:
    w = word.lower()
    count = frequency.get(w,0)
    frequency[w] = count + 1

sum_of_values = len(words)
data = {
    'rank': [],
    'word': [],
    'value': [],
    'freq': [],
    'approx': [],
    'log(rank)': [],
    'log(freq)': [],
}

rank = 0
for word, value in reversed(sorted(frequency.items(), key = itemgetter(1))):
    rank += 1
    if (rank == 1):
        top_freq = value/sum_of_values
    data['rank'].append(rank)
    data['word'].append(word)
    data['value'].append(value)
    freq = value/sum_of_values
    data['freq'].append(freq)
    data['approx'].append(top_freq * 1/rank)

    data['log(rank)'].append(log(rank))
    data['log(freq)'].append(log(freq))

total_ranks = rank

dataframe = pd.DataFrame(data=data)
# gather how data for Pareto principle
values_80 = sum_of_values * 0.8
curr_total_values = 0
print("values_80 =", values_80)
for row in dataframe.iterrows():
    curr_total_values += row[1]['value']
    if curr_total_values > values_80:
        curr_rank = row[1]['rank']
        print("curr_rank =", curr_rank)
        print("curr_total_values =", curr_total_values)
        print(f'~80% = {curr_total_values}/{sum_of_values} filled with {curr_rank}/{total_ranks}% of words')
        print(f'~80% = {curr_total_values/sum_of_values} filled with {curr_rank/total_ranks}% of words')
        break
# cut down to top 50
full_dataframe = dataframe
dataframe = dataframe[:50]
print(dataframe)



''' FREQUENCY '''
xs = [ rank for rank in dataframe['rank'] ]
ys = [ value for value in dataframe['value'] ]
plt.plot(xs, ys, 'ro')
plt.title("word frequency in " + file_name)
plt.xlabel('rank')
plt.ylabel('# occurences')
plt.axis([min(xs), max(xs), min(ys), max(ys)])
# annotate with titles
for word, x, y in zip(dataframe['word'], xs, ys):
    plt.annotate(word, (x, y))
plt.show()


''' LOG FREQUENCY '''
xs = [ rank for rank in dataframe['log(rank)'] ]
ys = [ value for value in dataframe['log(freq)'] ]
plt.plot(xs, ys, 'ro')
plt.title("log frequency in " + file_name)
plt.xlabel('log(rank)')
plt.ylabel('log(# occurences)')
plt.axis([min(xs), max(xs), min(ys), max(ys)])
# draw straight line
plt.plot([max(xs), min(xs)], [min(ys), max(ys)])
# annotate with titles
for word, x, y in zip(dataframe['word'], xs, ys):
    plt.annotate(word, (x, y))
plt.show()

# now draw for the pareto principle
''' PARETO '''
xs = [ rank for rank in full_dataframe['rank'] ]
ys = [ value for value in full_dataframe['value'] ]
plt.plot(xs, ys, 'ro')
plt.title("word frequency in " + file_name)
plt.xlabel('rank')
plt.ylabel('# occurences')
plt.axis([min(xs), max(xs), min(ys), max(ys)])
# draw rank line
plt.plot([curr_rank, curr_rank], [min(ys), max(ys)])
# annotate with titles
for word, x, y in zip(full_dataframe['word'], xs, ys):
    plt.annotate(word, (x, y))
plt.show()
