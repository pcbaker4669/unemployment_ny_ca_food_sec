import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

def run_did():
    # Paths
    data_file = "data/foodservice_employment.csv"
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    # ---------- CA vs TX DiD ----------
    print("Running CA vs TX DiD...")
    results_file_ca = os.path.join(results_dir, "did_summary_ca.txt")

    # Load & filter data
    df = pd.read_csv(data_file, parse_dates=True, index_col=0)
    df = df[['California', 'Texas']]
    df = df.loc['2022-01-01':'2025-07-31']

    # Reshape and create indicators
    ca = df.reset_index().rename(columns={'index': 'date'})
    long_ca = ca.melt(id_vars='date', var_name='state', value_name='employment')
    long_ca['treated'] = (long_ca['state'] == 'California').astype(int)
    long_ca['post_policy'] = (long_ca['date'] >= pd.to_datetime('2024-04-01')).astype(int)

    # Run DiD with robust SE
    model_ca = smf.ols('employment ~ treated + post_policy + treated:post_policy', data=long_ca).fit(cov_type='HC1')
    with open(results_file_ca, 'w') as f:
        f.write(model_ca.summary().as_text())
    print(f"CA DiD summary saved to {results_file_ca}")

    # Plot parallel trends
    pivot_ca = long_ca.pivot(index='date', columns='state', values='employment')
    plt.figure(figsize=(8,5))
    pivot_ca.plot(ax=plt.gca())
    plt.axvline(pd.to_datetime('2024-04-01'), color='r', linestyle='--', label='Policy Date')
    plt.title('CA vs TX Employment Trends')
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/ca_tx_trends.png')
    plt.close()

    # ---------- CA Event Study ----------
    print("Running CA event study...")
    policy_date_ca = pd.to_datetime('2024-04-01')
    long_ca['rel_month'] = (long_ca['date'].dt.to_period('M') - policy_date_ca.to_period('M')).apply(lambda x: x.n)
    for m in range(-12, 13):
        if m != 0:
            long_ca[f'rel_{m}'] = ((long_ca['rel_month'] == m) & (long_ca['treated'] == 1)).astype(int)

    # Only include dummy indicators, exclude helper column
    rel_cols_ca = [c for c in long_ca.columns if c.startswith('rel_') and c != 'rel_month']
    rel_cols_ca = sorted(rel_cols_ca, key=lambda x: int(x.split('_')[1]))

    # Build design matrix
    X_ca = long_ca[rel_cols_ca + ['treated']]
    X_ca = sm.add_constant(X_ca)
    y_ca = long_ca['employment']
    evt_ca = sm.OLS(y_ca, X_ca).fit(cov_type='HC1')

    coefs_ca = evt_ca.params[rel_cols_ca]
    cis_ca = evt_ca.conf_int().loc[rel_cols_ca]
    months_ca = [int(c.split('_')[1]) for c in rel_cols_ca]

    plt.figure(figsize=(8,5))
    plt.errorbar(months_ca, coefs_ca, yerr=[coefs_ca - cis_ca[0], cis_ca[1] - coefs_ca], fmt='o')
    plt.axhline(0, color='k', ls='--')
    plt.axvline(0, color='r', ls='--', label='Policy Implementation')
    plt.title('CA Event Study')
    plt.xlabel('Months Relative to Policy')
    plt.ylabel('Employment Effect')
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/event_study_ca.png')
    plt.close()
    print("CA event study plot saved.")

    # ---------- NY vs TX DiD ----------
    print("Running NY vs TX DiD...")
    results_file_ny = os.path.join(results_dir, "did_summary_ny.txt")
    df_ny = pd.read_csv(data_file, parse_dates=True, index_col=0)
    df_ny = df_ny[['New York', 'Texas']]
    df_ny = df_ny.loc['2022-01-01':'2025-07-31']

    ny = df_ny.reset_index().rename(columns={'index': 'date'})
    long_ny = ny.melt(id_vars='date', var_name='state', value_name='employment')
    long_ny['treated'] = (long_ny['state'] == 'New York').astype(int)
    long_ny['post_policy'] = (long_ny['date'] >= pd.to_datetime('2025-01-01')).astype(int)

    model_ny = smf.ols('employment ~ treated + post_policy + treated:post_policy', data=long_ny).fit(cov_type='HC1')
    with open(results_file_ny, 'w') as f:
        f.write(model_ny.summary().as_text())
    print(f"NY DiD summary saved to {results_file_ny}")

    pivot_ny = long_ny.pivot(index='date', columns='state', values='employment')
    plt.figure(figsize=(8,5))
    pivot_ny.plot(ax=plt.gca())
    plt.axvline(pd.to_datetime('2025-01-01'), color='r', linestyle='--', label='Policy Date')
    plt.title('NY vs TX Employment Trends')
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/ny_tx_trends.png')
    plt.close()

    # ---------- NY Event Study ----------
    print("Running NY event study...")
    policy_date_ny = pd.to_datetime('2025-01-01')
    long_ny['rel_month'] = (long_ny['date'].dt.to_period('M') - policy_date_ny.to_period('M')).apply(lambda x: x.n)
    for m in range(-12, 13):
        if m != 0:
            long_ny[f'rel_{m}'] = ((long_ny['rel_month'] == m) & (long_ny['treated'] == 1)).astype(int)

    rel_cols_ny = [c for c in long_ny.columns if c.startswith('rel_') and c != 'rel_month']
    rel_cols_ny = sorted(rel_cols_ny, key=lambda x: int(x.split('_')[1]))

    X_ny = long_ny[rel_cols_ny + ['treated']]
    X_ny = sm.add_constant(X_ny)
    y_ny = long_ny['employment']
    evt_ny = sm.OLS(y_ny, X_ny).fit(cov_type='HC1')

    coefs_ny = evt_ny.params[rel_cols_ny]
    cis_ny = evt_ny.conf_int().loc[rel_cols_ny]
    months_ny = [int(c.split('_')[1]) for c in rel_cols_ny]

    plt.figure(figsize=(8,5))
    plt.errorbar(months_ny, coefs_ny, yerr=[coefs_ny - cis_ny[0], cis_ny[1] - coefs_ny], fmt='o')
    plt.axhline(0, color='k', ls='--')
    plt.axvline(0, color='r', ls='--', label='Policy Implementation')
    plt.title('NY Event Study')
    plt.xlabel('Months Relative to Policy')
    plt.ylabel('Employment Effect')
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/event_study_ny.png')
    plt.close()
    print("NY event study plot saved.")
