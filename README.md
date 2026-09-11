**Instructions:**\
Run 'make setup', 'make pipeline', then 'make dashboard' in that order.

**Database Schema:**\
I split the data into 2 tables. The first table, 'samples_metadata', contains the metadata in columns 'sample', 'project', 'subject',
'condition', 'age', 'sex', 'treatment', 'response', 'sample_type', and 'time_from_treatment_start' from the original cell-count.csv.
 These columns are simply subsetted from the original csv without rearranging how the data are stored.\
 The second table, 'population_counts', has 3 columns: 'sample', 'population', and 'count'. This table rearranged the data from the 
 original csv so that each sample was split into 5 rows, one for each immune cell population, instead of one long row with counts for 
 all the populations. I did this to make downstream analyses easier, like calculating the population frequencies.\
 This schema design would scale better than if it were left in the original format because if future samples include data from 
 additional cell populations, these would be added into their own rows instead of having to create new columns with many NULL values
 from previous samples that don't have information on the newly tested populations. 

 **Code Structure:**\
 I structured my code in 3 main .py files: load_data.py, analysis.py, and dashboard.py. Each file corresponds to one section of the
 Makefile. \ 
 The load_data.py contains 3 main components: creating the samples_metadata table, creating the population_counts table, and inserting 
 data to fill out the tables. This file contains the code corresponding to Part 1 in the instructions. \
 The analysis.py file corresponds to Parts 2-4 in the instructions. It is made up of multiple functions that query the database and 
 perform data analysis using pandas. It also contains a section at the end that runs all the functions in order to get the required 
 outputs before initializing the dashboard. \
 The dashboard.py file creates the Streamlit dashboard using functions from analysis.py. I have wrapper functions with cache decorators
 at the start of the file to reduce redundant accessing of the database. Then I have all the actual Streamlit commands including titles, headers,
 tables & figures.

 **Dashboard Link:**\
 https://teiknical-hayliejarvis.streamlit.app/
