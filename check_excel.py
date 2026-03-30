import pandas as pd
df = pd.read_excel(r'c:\KMED-Tech\AI Resume Tailoring Agent\data\option2_job_links.xlsx')
print(f'Total rows in Excel: {len(df)}')
print('\nColumns:', df.columns.tolist())
print('\nFirst few rows:')
print(df.head())
