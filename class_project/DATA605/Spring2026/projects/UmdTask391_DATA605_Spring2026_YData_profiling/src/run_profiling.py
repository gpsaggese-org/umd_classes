import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
data_path = project_root / "data" / "baltim.csv"
output_path = project_root / "outputs" / "baltim_profile_report.html"

df = pd.read_csv(data_path)

print("Data shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

profile = ProfileReport(
    df,
    title="Baltimore Housing Data Profiling Report",
    explorative=True
)

profile.to_file(output_path)

print(f"\nReport saved to: {output_path}")