import os
import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt
import did_analysis

# Replace with your actual FRED API key
FRED_API_KEY = 'FRED_KEY_HERE'


def generate_data_and_charts():
    # Folder structure
    data_dir = 'data'
    figures_dir = 'figures'
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # File paths
    data_file = os.path.join(data_dir, 'foodservice_employment.csv')
    figure_file = os.path.join(figures_dir, 'foodservice_employment_trends.png')

    # Load or fetch data
    if not os.path.exists(data_file):
        print("Fetching data from FRED...")
        fred = Fred(api_key=FRED_API_KEY)

        # used to be CAUR, NYUR, TXUR, and UNRATE for total unemployment
        # now for food sector unemployment, no US
        series_ids = {
            'California': 'SMU06000007072200001',
            'New York': 'SMU36000007072200001',
            'Texas': 'SMU48000007072200001'
        }

        data = {}
        for region, series_id in series_ids.items():
            data[region] = fred.get_series(series_id)

        df = pd.DataFrame(data)
        df.index = pd.to_datetime(df.index)

        df.to_csv(data_file)
        print(f"Data saved to {data_file}")
    else:
        print(f"Reading cached data from {data_file}")
        df = pd.read_csv(data_file, index_col=0, parse_dates=True)

    # Filter for recent years
    df = df[df.index >= '2020-01-01']

    # Plot Figure 1
    plt.figure(figsize=(10, 6))
    df.plot(ax=plt.gca())
    policy_ca = pd.to_datetime('2024-04-01')
    policy_ny = pd.to_datetime('2025-01-01')
    plt.axvline(policy_ca, color='red', linestyle='--', linewidth=1.5, label='CA $20/hr (Apr 2024)')
    plt.axvline(policy_ny, color='blue', linestyle='--', linewidth=1.5, label='NY +$0.50 (Jan 2025)')
    ylim = plt.ylim()
    plt.text(policy_ca, ylim[1]*0.97, 'CA $20/hr starts', color='red', fontsize=9, ha='left', va='top')
    plt.text(policy_ny, ylim[1]*0.90, 'NY +$0.50 starts', color='blue', fontsize=9, ha='left', va='top')
    plt.title('Food Service Employment (2020–2025)')
    plt.ylabel('Employment (Thousands)')
    plt.xlabel('Date')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(figure_file, dpi=300)
    plt.close()
    print(f"Chart with policy marker saved to {figure_file}")

    # Plot Figure 2 (smoothed and zoomed)
    df_smooth = df.rolling(window=3, center=True).mean()
    df_zoom = df_smooth[(df_smooth.index >= '2023-01-01') & (df_smooth.index <= '2025-06-01')]
    fig2_path = os.path.join(figures_dir, 'foodservice_employment_policy_window.png')
    plt.figure(figsize=(10, 6))
    df_zoom.plot(ax=plt.gca())
    plt.axvline(policy_ca, color='red', linestyle='--', linewidth=1.5, label='CA $20/hr (Apr 2024)')
    plt.axvline(policy_ny, color='blue', linestyle='--', linewidth=1.5, label='NY +$0.50 (Jan 2025)')
    plt.axvspan(policy_ca, pd.to_datetime('2024-12-31'), color='red', alpha=0.1)
    plt.axvspan(policy_ny, pd.to_datetime('2025-06-01'), color='blue', alpha=0.1)
    plt.title('Food Service Employment Trends Around Minimum Wage Hikes (2023–2025)')
    plt.ylabel('Employment (Thousands)')
    plt.xlabel('Date')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"Focused policy chart saved to: {fig2_path}")

# Entry point
if __name__ == "__main__":
    print("Select a choice:")
    print("1. Generate Initial Data")
    print("2. Difference-in-Differences analysis")
    choice = int(input("Enter 1 or 2: "))
    if choice == 1:
        generate_data_and_charts()
    elif choice == 2:
        did_analysis.run_did()