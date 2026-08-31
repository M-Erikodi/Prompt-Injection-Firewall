import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "service/logs.db"

st.title("Injection Detection Firewall — Dashboard")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM requests ORDER BY id DESC", conn)
conn.close()

st.subheader("Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total requests", len(df))
col2.metric("Blocked", (df["verdict"] == "block").sum())
col3.metric("Flagged", (df["verdict"] == "flag").sum())

st.subheader("Verdicts breakdown")
st.bar_chart(df["verdict"].value_counts())

st.subheader("Recent requests")
st.dataframe(df)