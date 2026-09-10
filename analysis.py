import sqlite3
import pandas as pd

#SQL connection
conn = sqlite3.connect('teiknical.db')
cursor = conn.cursor()

#PART 2
#get the total count for each sample

def get_frequency_table(conn):
    query = '''
    SELECT
        pc.sample,
        totals.total_count,
        pc.population,
        pc.count,
        ROUND(pc.count * 100.0 / totals.total_count, 2) AS percentage
    FROM population_counts AS pc
    JOIN (
        SELECT sample, SUM(count) AS total_count
        FROM population_counts
        GROUP BY sample
    ) AS totals
    ON pc.sample = totals.sample;    
    '''
    df = pd.read_sql_query(query, conn)
    return df

print(get_frequency_table(conn))





conn.close()