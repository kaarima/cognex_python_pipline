import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "tolerance_limits.csv"


df = pd.read_csv(INPUT_FILE)


# Filter for blob features only
blob_df = df[df["Feature"].str.startswith("B")]


plt.figure(figsize=(12, 6))
plt.bar(blob_df["Feature"], blob_df["Std"])
plt.xticks(rotation=45, ha='right')
plt.xlabel("Feature")
plt.ylabel("Standard Deviation")
plt.title("Standard Deviation of Blob Features")
plt.tight_layout()
plt.savefig("std_plot.png", dpi=150)
plt.show()


print("Plot saved as std_plot.png")
