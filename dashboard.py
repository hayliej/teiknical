import streamlit as st
from analysis import get_frequency_table, get_miraclib_data, get_miraclib_boxplot, get_miraclib_statistics, get_miraclib_data_t0, get_samples_per_project, get_responder_counts, get_sex_counts,get_melanoma_male_data_t0
import sqlite3

@st.cache_resource
def get_connection():
    return sqlite3.connect('teiknical.db', check_same_thread=False)

conn = get_connection()

@st.cache_data
def load_summary(_conn):
    return get_frequency_table(_conn)

@st.cache_data
def load_miraclib_data(_conn, summary):
    return get_miraclib_data(_conn, summary)

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

st.header("Part 3: Miraclib Response Analysis")

miraclib_data = load_miraclib_data(conn, summary)

fig = get_miraclib_boxplot(miraclib_data)
st.plotly_chart(fig)

statistics_df = get_miraclib_statistics(miraclib_data)
st.dataframe(statistics_df)

st.write('cd4_t_cell shows a significant difference between responders and non-responders')

st.header("Part 4: Data Subset Analysis")

miraclib_data_t0 = load_miraclib_data_t0(conn)
st.dataframe(miraclib_data_t0)

proj_counts = get_samples_per_project(miraclib_data_t0)
st.table(proj_counts)

response_counts = get_responder_counts(miraclib_data_t0)
st.table(response_counts)

sex_counts = get_sex_counts(miraclib_data_t0)
st.table(sex_counts)


mm_b_counts = load_melanoma_male_data_t0(conn, summary)
st.metric(label="Average B Cells (Melanoma Male Responders, t=0)", value=f"{mm_b_counts:.2f}")