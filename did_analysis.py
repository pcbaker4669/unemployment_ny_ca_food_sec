import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import os

def run_did():
    # Paths
    data_file = "data/foodservice_employment.csv"
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    # ---------- CA vs TX ----------
    print("Running CA vs TX DiD...")

    results_file = os.path.join(results_dir, "did_summary.txt")

    # Load data
    df = pd.read_csv(data_file, parse_dates=True, index_col=0)
    df = df[["California", "Texas"]]  # Focus on CA (treatment) vs TX (control)

    # Filter date range
    df = df[df.index >= "2022-01-01"]
    df = df[df.index <= "2025-06-01"]

    # Reshape to long format
    df = df.reset_index().rename(columns={"index": "date"})
    long_df = df.melt(id_vars="date", var_name="state", value_name="employment")
    # Define treatment and post-policy indicators
    long_df["treated"] = (long_df["state"] == "California").astype(int)
    long_df["post_policy"] = (long_df["date"] >= "2024-04-01").astype(int)

    # DiD regression
    model = smf.ols("employment ~ treated + post_policy + treated:post_policy", data=long_df).fit()

    # Save results
    with open(results_file, "w") as f:
        f.write(model.summary().as_text())

    print(f"DiD regression complete. Summary saved to: {results_file}")

    # Optional: plot parallel trends
    pivot_df = long_df.pivot(index="date", columns="state", values="employment")
    plt.figure(figsize=(10, 6))
    pivot_df.plot(ax=plt.gca())
    plt.axvline(pd.to_datetime("2024-04-01"), color='red', linestyle='--', label='Policy Date')
    plt.title("Food Service Employment: CA vs TX (2022–2025)")
    plt.ylabel("Employment (Thousands)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/did_plot_ca_tx.png", dpi=300)
    plt.close()

    print("Parallel trends plot saved to: figures/did_plot_ca_tx.png")

    # ---------- NY vs TX ----------
    print("\nRunning NY vs TX DiD...")

    results_file_ny = os.path.join(results_dir, "did_summary_ny.txt")
    df_ny = pd.read_csv(data_file, parse_dates=True, index_col=0)
    df_ny = df_ny[["New York", "Texas"]]
    df_ny = df_ny[df_ny.index >= "2022-01-01"]
    df_ny = df_ny[df_ny.index <= "2025-06-01"]
    df_ny = df_ny.reset_index().rename(columns={"index": "date"})
    long_df_ny = df_ny.melt(id_vars="date", var_name="state", value_name="employment")
    long_df_ny["treated"] = (long_df_ny["state"] == "New York").astype(int)
    long_df_ny["post_policy"] = (long_df_ny["date"] >= "2025-01-01").astype(int)

    model_ny = smf.ols("employment ~ treated + post_policy + treated:post_policy", data=long_df_ny).fit()
    with open(results_file_ny, "w") as f:
        f.write(model_ny.summary().as_text())

    print(f"NY DiD regression complete. Summary saved to: {results_file_ny}")

    pivot_df_ny = long_df_ny.pivot(index="date", columns="state", values="employment")
    plt.figure(figsize=(10, 6))
    pivot_df_ny.plot(ax=plt.gca())
    plt.axvline(pd.to_datetime("2025-01-01"), color='red', linestyle='--', label='Policy Date')
    plt.title("Food Service Employment: NY vs TX (2022–2025)")
    plt.ylabel("Employment (Thousands)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/did_plot_ny_tx.png", dpi=300)
    plt.close()

    print("Parallel trends plot saved to: figures/did_plot_ny_tx.png")