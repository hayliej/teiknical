import streamlit as st
from analysis import get_frequency_table, get_miraclib_data, get_miraclib_boxplot, get_miraclib_statistics, get_miraclib_data_t0, get_samples_per_project, get_responder_counts, get_sex_counts,get_melanoma_male_data_t0
import sqlite3
import pandas as pd

import os
st.write("Current working directory:", os.getcwd())
st.write("Files here:", os.listdir())

@st.cache_resource
def get_connection():
    return sqlite3.connect('teiknical.db', check_same_thread=False)

conn = get_connection()

@st.cache_data
def load_summary(_conn):
    return get_frequency_table(_conn)

@st.cache_data
def load_miraclib_data(_conn, summary, condition, treatment):
    return get_miraclib_data(_conn, summary, condition, treatment)

@st.cache_data
def load_miraclib_data_t0(_conn):
    return get_miraclib_data_t0(_conn)

@st.cache_data
def load_melanoma_male_data_t0(_conn, summary):
    return get_melanoma_male_data_t0(_conn, summary)

st.title("Teiko Teiknical Assessment Dashboard")

st.header("Part 2: Cell Population Frequencies")

summary = load_summary(conn)
st.dataframe(summary)

st.header("Part 3: Treatment Response Analysis")

conditions = pd.read_sql_query("SELECT DISTINCT condition FROM samples_metadata", conn)['condition'].tolist()
treatments = pd.read_sql_query("SELECT DISTINCT treatment FROM samples_metadata", conn)['treatment'].tolist()

selected_condition = st.selectbox("Select Condition", conditions)
selected_treatment = st.selectbox("Select Treatment", treatments)

miraclib_data = load_miraclib_data(conn, summary, selected_condition, selected_treatment)

fig = get_miraclib_boxplot(miraclib_data)
st.plotly_chart(fig)

st.subheader("Statistical analysis data, t = Welch's t-test, u = Mann-Whitney U test")
statistics_df = get_miraclib_statistics(miraclib_data)
st.dataframe(statistics_df)

st.write('cd4_t_cell shows a significant difference between melanoma patient responders and non-responders treated with miraclib')

st.header("Part 4: Data Subset Analysis")

st.subheader('All melanoma PBMC samples at baseline (time_from_treatment_start = 0) from patients who have been treated with miraclib')
miraclib_data_t0 = load_miraclib_data_t0(conn)
st.dataframe(miraclib_data_t0)

st.subheader('Number of samples per project')
proj_counts = get_samples_per_project(miraclib_data_t0)
st.table(proj_counts)

st.subheader('Counts of responder/non-responder subjects')
response_counts = get_responder_counts(miraclib_data_t0)
st.table(response_counts)

st.subheader('Counts of male/female subjects')
sex_counts = get_sex_counts(miraclib_data_t0)
st.table(sex_counts)


st.subheader('Average number of B cells for melanoma male responders at time_from_treatment_start = 0')
mm_b_counts = load_melanoma_male_data_t0(conn, summary)
st.metric(label="Average B Cells (Melanoma Male Responders, t=0)", value=f"{mm_b_counts:.2f}")