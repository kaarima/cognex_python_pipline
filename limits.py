import pandas as pd
import numpy as np


INPUT_FILE = "GOOD_parts.csv"
OUTPUT_FILE = "tolerance_limits.csv"


# ==========================
# Load good parts
# ==========================

df = pd.read_csv(INPUT_FILE)


print("Loaded:")
print(df.shape)


# remove Image column

features = df.drop(columns=["Image"])



# ==========================
# Calculate statistics
# ==========================

results = []


for column in features.columns:

    data = features[column].dropna()


    mean = data.mean()

    std = data.std()


    minimum = data.min()

    maximum = data.max()


    # 3 sigma tolerance

    lower = mean - 3*std

    upper = mean + 3*std



    results.append([

        column,
        mean,
        std,
        minimum,
        maximum,
        lower,
        upper

    ])



# ==========================
# Save results
# ==========================


result_df = pd.DataFrame(

    results,

    columns=[
        "Feature",
        "Mean",
        "Std",
        "Measured_Min",
        "Measured_Max",
        "Lower_Limit",
        "Upper_Limit"
    ]

)


result_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nDONE")
print("Saved:", OUTPUT_FILE)



print("\nTolerance table:")
print(result_df)