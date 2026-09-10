import sqlite3
import pandas as pd
import plotly.express as px
from scipy import stats

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


#PART 3

def get_miraclib_data(conn, summary):
    #get sample ids from patients who have melanoma, are treated with miraclib, have a recorded response, and are PBMC samples
    miraclib_samples = pd.read_sql_query('''
    SELECT sample, response
    FROM samples_metadata
    WHERE condition = 'melanoma' AND treatment = 'miraclib' AND response IS NOT NULL AND sample_type = 'PBMC'
    ''', conn)

    #merge with data frame including percentages from part 2
    miraclib_data = pd.merge(miraclib_samples, summary, on='sample', how='inner')
    
    return miraclib_data


def get_miraclib_boxplot(miraclib_data):
    #plot clustering by population showing responders vs. non responders and percentage on y axis
    fig = px.box(
        miraclib_data,
        x='population',
        y='percentage',
        color='response',
        title='Population Relative Frequencies of Responders vs. Non-Responders to Miraclib in Melanoma Samples',
        labels=
        {
            'response':'Response'
        }
    )
    fig.update_layout(
        xaxis_title="Population",
        yaxis_title="Relative Frequency as Percentage"
    )

    return fig


def get_miraclib_statistics(miraclib_data):
    #run statistical tests on each cell population to check significance
    statistics = []
    for pop in miraclib_data['population'].unique():
        ryes = miraclib_data[(miraclib_data['population'] == pop) & (miraclib_data['response'] == 'yes')]['percentage']
        rno = miraclib_data[(miraclib_data['population'] == pop) & (miraclib_data['response'] == 'no')]['percentage']
        
        #start with Welch's t-test, eyeballing from boxplot and taking into account large sample size suggest it is likely normally distributed data
        t_stat, t_pvalue = stats.ttest_ind(ryes, rno, equal_var=False)
        #run Mann-Whitney U test as a non-parametric alternative to Welch's in case normal distribution assumption was off
        u_stat, u_pvalue = stats.mannwhitneyu(ryes, rno)

        statistics.append({
            'population': pop,
            't_statistic': t_stat,
            't_pvalue': t_pvalue,
            'u_statistic': u_stat,
            'u_pvalue': u_pvalue,
            'significance_ttest': t_pvalue < 0.05,
            'significance_mannwhitney': u_pvalue < 0.05
        })

    statistics_df = pd.DataFrame(statistics)

    return statistics_df


#PART 4

#get the subsetted data for part 4
def get_miraclib_data_t0(conn):
    #get samples from patients who have melanoma, are treated with miraclib, are PBMC samples at time from treatment start =0
    miraclib_samples = pd.read_sql_query('''
    SELECT project, subject, age, sex, response, sample
    FROM samples_metadata
    WHERE condition = 'melanoma' AND treatment = 'miraclib' AND sample_type = 'PBMC' AND time_from_treatment_start = 0
    ''', conn)
    
    return miraclib_samples

#get counts of samples/project
def get_samples_per_project(miraclib_samples):
    project_counts = miraclib_samples['project'].value_counts()

    return project_counts

def get_responder_counts(miraclib_samples):
    unique_subjects = miraclib_samples.drop_duplicates(subset='subject')
    responder_counts = unique_subjects['response'].value_counts()

    return responder_counts

def get_sex_counts(miraclib_samples):
    unique_subjects = miraclib_samples.drop_duplicates(subset='subject')
    sex_counts = unique_subjects['sex'].value_counts()

    return sex_counts

if __name__ == "__main__":
    #SQL connection
    conn = sqlite3.connect('teiknical.db')

    #part 2
    summary = get_frequency_table(conn)
    print(summary)
    
    #part 3
    miraclib_data = get_miraclib_data(conn, summary)
    print (miraclib_data)
    
    fig = get_miraclib_boxplot(miraclib_data)
    fig.show()
    
    statistics_df = get_miraclib_statistics(miraclib_data)
    print(statistics_df)

    #part 4
    miraclib_at_t0 = get_miraclib_data_t0(conn)
    print(miraclib_at_t0)

    proj_counts = get_samples_per_project(miraclib_at_t0)
    print(proj_counts)

    response_counts = get_responder_counts(miraclib_at_t0)
    print(response_counts)

    sex_counts = get_sex_counts(miraclib_at_t0)
    print(sex_counts)

    conn.close()