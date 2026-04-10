import csv
import sqlite3

conn = sqlite3.connect('teiko.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (project TEXT, subject TEXT, condition TEXT, age INTEGER, sex TEXT, treatment TEXT, response TEXT, sample TEXT, sample_type TEXT, time_from_treatment_start INTEGER, b_cell INTEGER, cd8_t_cell INTEGER, cd4_t_cell INTEGER, nk_cell INTEGER, monocyte INTEGER);")

with open('cell-count.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    
    cur.executemany("INSERT INTO users (project, subject, condition, age, sex, treatment, response, sample, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", reader)

conn.commit()
conn.close()
