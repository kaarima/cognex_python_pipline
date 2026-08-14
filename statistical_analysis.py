import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path


INPUT_FILE = "GOOD_parts.csv"
PLOTS_DIR = "plots"


# Create plots directory
Path(PLOTS_DIR).mkdir(exist_ok=True)


# ==========================
# 1. Data Analysis
# ==========================

print("=" * 60)
print("1. DATA ANALYSIS")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)
print(f"Loaded dataset: {df.shape[0]} images, {df.shape[1]-1} features")

# Remove Image column
features = df.drop(columns=["Image"])

# Calculate statistics
results = []
for column in features.columns:
    data = features[column].dropna()
    
    mean = data.mean()
    std = data.std()
    minimum = data.min()
    maximum = data.max()
    range_val = maximum - minimum
    cv = std / mean if mean != 0 else np.inf
    
    results.append({
        "Feature": column,
        "Mean": mean,
        "Std": std,
        "Min": minimum,
        "Max": maximum,
        "Range": range_val,
        "CV": cv
    })

stats_df = pd.DataFrame(results)
stats_df = stats_df.sort_values("CV")

print("\nSummary Statistics (sorted by Coefficient of Variation):")
print(stats_df.to_string(index=False))

# Save summary table
stats_df.to_csv("summary_statistics.csv", index=False)
print("\nSaved: summary_statistics.csv")


# ==========================
# 2. Distribution Plots
# ==========================

print("\n" + "=" * 60)
print("2. GENERATING DISTRIBUTION PLOTS")
print("=" * 60)

for column in features.columns:
    data = features[column].dropna()
    mean = data.mean()
    std = data.std()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generate x values for Gaussian curve
    x = np.linspace(mean - 4*std, mean + 4*std, 1000)
    
    # Calculate Gaussian curve (normal distribution)
    y = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)
    
    # Plot Gaussian curve
    ax.plot(x, y, 'b-', linewidth=2, label='Gaussian Distribution')
    
    # Fill area under curve
    ax.fill_between(x, y, alpha=0.3, color='steelblue')
    
    # Sigma lines
    ax.axvline(mean, color='red', linestyle='-', linewidth=2, label='Mean')
    ax.axvline(mean + std, color='orange', linestyle='--', linewidth=1.5, label='±1σ')
    ax.axvline(mean - std, color='orange', linestyle='--', linewidth=1.5)
    ax.axvline(mean + 2*std, color='yellow', linestyle='--', linewidth=1.5, label='±2σ')
    ax.axvline(mean - 2*std, color='yellow', linestyle='--', linewidth=1.5)
    ax.axvline(mean + 3*std, color='green', linestyle='--', linewidth=1.5, label='±3σ')
    ax.axvline(mean - 3*std, color='green', linestyle='--', linewidth=1.5)
    
    ax.set_xlabel(column)
    ax.set_ylabel('Probability Density')
    ax.set_title(f'Gaussian Distribution of {column}')
    ax.legend()
    
    # Add statistics text
    stats_text = f'Mean = {mean:.3f}\nStd = {std:.3f}\n3σ range = {mean-3*std:.3f} → {mean+3*std:.3f}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/{column}.png', dpi=150)
    plt.close()
    
    print(f"Generated: {PLOTS_DIR}/{column}.png")


# ==========================
# 3. Gaussian Analysis - 3-Sigma Tolerances
# ==========================

print("\n" + "=" * 60)
print("3. GAUSSIAN ANALYSIS - 3-SIGMA TOLERANCES")
print("=" * 60)

tolerance_results = []
for column in features.columns:
    data = features[column].dropna()
    mean = data.mean()
    std = data.std()
    
    lower_3sigma = mean - 3*std
    upper_3sigma = mean + 3*std
    
    tolerance_results.append({
        "Feature": column,
        "Mean": mean,
        "Std": std,
        "Lower_3Sigma": lower_3sigma,
        "Upper_3Sigma": upper_3sigma
    })

tolerance_df = pd.DataFrame(tolerance_results)
tolerance_df.to_csv("statistical_tolerances.csv", index=False)
print("Saved: statistical_tolerances.csv")
print(tolerance_df.to_string(index=False))


# ==========================
# 4. Identify Stable and Unstable Features
# ==========================

print("\n" + "=" * 60)
print("4. STABLE vs UNSTABLE FEATURES")
print("=" * 60)

# Define thresholds
CV_THRESHOLD_STABLE = 0.01  # 1% variation
CV_THRESHOLD_UNSTABLE = 0.05  # 5% variation

stable_features = stats_df[stats_df["CV"] < CV_THRESHOLD_STABLE]
unstable_features = stats_df[stats_df["CV"] >= CV_THRESHOLD_UNSTABLE]
moderate_features = stats_df[(stats_df["CV"] >= CV_THRESHOLD_STABLE) & (stats_df["CV"] < CV_THRESHOLD_UNSTABLE)]

print(f"\nSTABLE FEATURES (CV < {CV_THRESHOLD_STABLE*100}%):")
print(f"Count: {len(stable_features)}")
print(stable_features[["Feature", "CV"]].to_string(index=False))

print(f"\nMODERATE FEATURES ({CV_THRESHOLD_STABLE*100}% <= CV < {CV_THRESHOLD_UNSTABLE*100}%):")
print(f"Count: {len(moderate_features)}")
print(moderate_features[["Feature", "CV"]].to_string(index=False))

print(f"\nUNSTABLE FEATURES (CV >= {CV_THRESHOLD_UNSTABLE*100}%):")
print(f"Count: {len(unstable_features)}")
print(unstable_features[["Feature", "CV"]].to_string(index=False))


# ==========================
# 5. Feature Analysis for Inspection Strategy
# ==========================

print("\n" + "=" * 60)
print("5. FEATURE ANALYSIS FOR INSPECTION STRATEGY")
print("=" * 60)

# Group features by type
dx_features = [col for col in features.columns if col.startswith("DX")]
dy_features = [col for col in features.columns if col.startswith("DY")]
blob_row_features = [col for col in features.columns if "Row" in col]
blob_col_features = [col for col in features.columns if "Col" in col]
blob_area_features = [col for col in features.columns if "Area" in col]

print("\nDX Features (Horizontal distances):")
for feat in dx_features:
    row = stats_df[stats_df["Feature"] == feat].iloc[0]
    print(f"  {feat}: CV = {row['CV']:.4f}")

print("\nDY Features (Vertical distances):")
for feat in dy_features:
    row = stats_df[stats_df["Feature"] == feat].iloc[0]
    print(f"  {feat}: CV = {row['CV']:.4f}")

print("\nBlob Row Features (Y position):")
for feat in blob_row_features:
    row = stats_df[stats_df["Feature"] == feat].iloc[0]
    print(f"  {feat}: CV = {row['CV']:.4f}")

print("\nBlob Col Features (X position):")
for feat in blob_col_features:
    row = stats_df[stats_df["Feature"] == feat].iloc[0]
    print(f"  {feat}: CV = {row['CV']:.4f}")

print("\nBlob Area Features:")
for feat in blob_area_features:
    row = stats_df[stats_df["Feature"] == feat].iloc[0]
    print(f"  {feat}: CV = {row['CV']:.4f}")


print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
