import pandas as pd

file_path = 'C:/Users/simas/PycharmProjects/selenium_project/data/raw/review_comments.csv'

df = pd.read_csv(file_path)

# Pasiliname pasikartojancius irasus
df = df.drop_duplicates()

# Isvalome failus
df['Star Score'] = df['Star Score'].str.replace("s", "").str.replace("žvaigždutė", "").str.strip()
df['Star Score'] = pd.to_numeric(df['Star Score'], errors='coerce')

df['Comment'] = df['Comment'].str.replace("\n", " ").str.strip()

df = df.dropna(subset=['Comment', "Star Score"])

df.to_csv("C:/Users/simas/PycharmProjects/selenium_project/data/processed/cleaned_review_comments.csv", index=False)