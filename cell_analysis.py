import numpy as np
import pandas as pd
import sqlite3
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import plotly.express as px

def load_data(db_file):
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

df = load_data('teiko.db')

# cell type names
cell_cols = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
cell_cols_nice = ['B Cells',"CD8 T Cells",'CD4 T Cells','NK Cells','Monocyte Cells']


# build Data Overview table
df["total_count"] = df[cell_cols].sum(axis=1)
summary = df.melt(
    id_vars=["sample", "total_count"],
    value_vars=cell_cols,
    var_name="population",
    value_name="count"
)
summary["percentage"] = 100 * summary["count"] / summary["total_count"]
print('Summary Statistics\n')
print(summary.to_markdown(tablefmt='grid'))
print('\n')

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

pvals = {}

fig, axes = plt.subplots(1, len(cell_cols), figsize=(18, 4), sharey=True)

for i, cell in enumerate(cell_cols):

    axes[i].boxplot(
        [responders[cell], non_responders[cell]],
        tick_labels=["Responder", "Non-Responder"],
        showfliers=True
    )

    axes[i].set_title(cell_cols_nice[i])
    axes[i].tick_params(axis='x', labelsize=10)
    axes[i].tick_params(axis='y', labelsize=10)

    axes[i].set_ylabel("Relative frequency (%)")

    stat, p = ttest_ind(
        responders[cell],
        non_responders[cell],
        equal_var=False,
        nan_policy="omit"
    )
    pvals[cell] = p
plt.tight_layout()
plt.savefig('boxplots.png')
plt.show()

stats_df = pd.DataFrame({
    "population": list(pvals.keys()),
    "p_value": list(pvals.values())
})

stats_df["significant (p<0.05)"] = stats_df["p_value"] < 0.05

print('Population Frequency Statistics\n')
print(stats_df)

baseline = df[
    (df["condition"] == "melanoma") &
    (df["treatment"] == "miraclib") &
    (df["sample_type"] == "PBMC") &
    (df["time_from_treatment_start"] == 0)
]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# -----------------------
# Samples per project
# -----------------------
counts = baseline["project"].value_counts()

axes[0].bar(counts.index, counts.values)
axes[0].set_title("Samples per Project")
axes[0].set_xlabel("Project")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis='x', rotation=45)

# -----------------------
# Responders vs Non-Responders
# -----------------------
counts = baseline.drop_duplicates("subject")["response"].value_counts()

axes[1].bar(counts.index, counts.values)
axes[1].set_title("Responders vs Non-Responders")
axes[1].set_xlabel("Response")
axes[1].set_ylabel("Subjects")

# -----------------------
# Sex distribution
# -----------------------
counts = baseline.drop_duplicates("subject")["sex"].value_counts()

axes[2].bar(counts.index, counts.values)
axes[2].set_title("Male vs Female")
axes[2].set_xlabel("Sex")
axes[2].set_ylabel("Subjects")

plt.tight_layout()
plt.savefig('bar_charts.png')
plt.show()
