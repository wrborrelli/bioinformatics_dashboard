import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rc('font', size=24)
from scipy.stats import ttest_ind
import plotly.express as px

DB_PATH = "teiko.db"

st.set_page_config(layout="wide")
st.title("Loblaw Bio Clinical Trial Dashboard")

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

df = load_data()

cell_cols = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
cell_cols_nice = ['B Cells',"CD8 T Cells",'CD4 T Cells','NK Cells','Monocyte Cells']

st.header("Cell Population Relative Frequencies")

df["total_count"] = df[cell_cols].sum(axis=1)

summary = df.melt(
    id_vars=["sample", "total_count"],
    value_vars=cell_cols,
    var_name="population",
    value_name="count"
)

summary["percentage"] = 100 * summary["count"] / summary["total_count"]

st.dataframe(summary, use_container_width=True)

st.header("Responder vs Non-Responder Analysis")

filtered = df[
    (df["condition"] == "melanoma") &
    (df["treatment"] == "miraclib") &
    (df["sample_type"] == "PBMC")
].copy()

filtered["total_count"] = filtered[cell_cols].sum(axis=1)

for c in cell_cols:
    filtered[c] = 100 * filtered[c] / filtered["total_count"]

responders = filtered[filtered["response"] == "yes"]
non_responders = filtered[filtered["response"] == "no"]

st.subheader("Boxplots")

cols = st.columns(len(cell_cols))
pvals = {}

for i, cell in enumerate(cell_cols):

    plot_df = pd.DataFrame({
        "value": pd.concat([responders[cell], non_responders[cell]]),
        "response": (["Responder"] * len(responders)) +
                    (["Non-Responder"] * len(non_responders))
    })

    fig = px.box(
        plot_df,
        x="response",
        y="value",
        points="all",
        color="response",
        title=cell_cols_nice[i],
        labels={"value": "Relative frequency (%)"}
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False
    )

    cols[i].plotly_chart(fig, use_container_width=True)

    stat, p = ttest_ind(
        responders[cell],
        non_responders[cell],
        equal_var=False,
        nan_policy="omit"
    )
    pvals[cell] = p


st.subheader("Statistical Significance")

stats_df = pd.DataFrame({
    "population": list(pvals.keys()),
    "p_value": list(pvals.values())
})

stats_df["significant (p<0.05)"] = stats_df["p_value"] < 0.05

st.dataframe(stats_df)


st.header("Baseline Melanoma PBMC (Miraclib)")

baseline = df[
    (df["condition"] == "melanoma") &
    (df["treatment"] == "miraclib") &
    (df["sample_type"] == "PBMC") &
    (df["time_from_treatment_start"] == 0)
]

col1, col2, col3 = st.columns(3)

# Samples per project
with col1:
    st.subheader("Samples per Project")

    counts = baseline["project"].value_counts().reset_index()
    counts.columns = ["project", "count"]

    fig = px.bar(
        counts,
        x="project",
        y="count",
        title=None
    )

    fig.update_layout(
        xaxis_title="Project",
        yaxis_title="Count",
        xaxis_tickangle=45
    )

    st.plotly_chart(fig, use_container_width=True)


# Responders
with col2:
    st.subheader("Subjects: Responders vs Non-Responders")

    counts = (
        baseline.drop_duplicates("subject")["response"]
        .value_counts()
        .reset_index()
    )
    counts.columns = ["response", "count"]

    fig = px.bar(
        counts,
        x="response",
        y="count"
    )

    fig.update_layout(
        xaxis_title="Response",
        yaxis_title="Subjects"
    )

    st.plotly_chart(fig, use_container_width=True)


# Sex
with col3:
    st.subheader("Subjects: Male vs Female")

    counts = (
        baseline.drop_duplicates("subject")["sex"]
        .value_counts()
        .reset_index()
    )
    counts.columns = ["sex", "count"]

    fig = px.bar(
        counts,
        x="sex",
        y="count"
    )

    fig.update_layout(
        xaxis_title="Sex",
        yaxis_title="Subjects"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Loblaw Bio Trial Analysis Dashboard")
