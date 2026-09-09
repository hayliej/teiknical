import sqlite3
import pandas as pd
import os

#delete .db file if it exists
if os.path.exists('teiknical.db'):
    os.remove('teiknical.db')

#read in csv
cell_count = pd.read_csv('cell-count.csv')

#create a list of tuples from csv data to insert into tables
metadata = cell_count[['sample', 'project', 'subject', 'condition', 'age', 'sex', 'treatment', 'response', 'sample_type', 'time_from_treatment_start']].values.tolist()

populations = []
for row in cell_count.itertuples():
  b = [row.sample, 'b_cell', row.b_cell]
  cd8_t = [row.sample, 'cd8_t_cell', row.cd8_t_cell]
  cd4_t = [row.sample, 'cd4_t_cell', row.cd4_t_cell]
  nk = [row.sample, 'nk_cell', row.nk_cell]
  mono = [row.sample, 'monocyte', row.monocyte]
  populations.extend([b, cd8_t, cd4_t, nk, mono])


#SQL connection
conn = sqlite3.connect('teiknical.db')
cursor = conn.cursor()

#make sure the tables can connect
cursor.execute('PRAGMA foreign_keys = ON')

#create the metadata table
cursor.execute('''
CREATE TABLE IF NOT EXISTS samples_metadata (
    sample TEXT PRIMARY KEY,
    project TEXT,
    subject TEXT,
    condition TEXT,
    age INTEGER,
    sex TEXT,
    treatment TEXT,
    response TEXT,
    sample_type TEXT,
    time_from_treatment_start INTEGER
);
'''
)

#create the cell populations count table
cursor.execute('''
CREATE TABLE IF NOT EXISTS population_counts (
    sample TEXT,
    population TEXT,
    count INTEGER,
    PRIMARY KEY (sample, population),
    FOREIGN KEY (sample) REFERENCES samples_metadata(sample)
);
'''
)


# Insert data
cursor.executemany('''
INSERT INTO samples_metadata (sample, project, subject, condition, age, sex, treatment, response, sample_type, time_from_treatment_start)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
''',
metadata
)
conn.commit()

cursor.executemany('''
INSERT INTO population_counts (sample, population, count)
VALUES (?, ?, ?);
''',
populations
)
conn.commit()

conn.close()