# 📊 Minimum Wage Hikes and Food Service Employment: A DiD Analysis

This repository contains the Python code, data pipeline, and output used in the analysis for the paper:  
**“Minimum Wage Hikes and Sectoral Employment: Evidence from California and New York”**

The study uses a difference-in-differences (DiD) framework to estimate the short-term employment effects of recent minimum wage increases in California and New York, using Texas as a control state. Event study models are also included to assess dynamic effects and validate the parallel trends assumption.

---

## 🗂 Project Structure

```
minwage-did/
│
├── data/
│   └── foodservice_employment.csv       # Monthly FRED employment data (NAICS 722)
│
├── figures/
│   ├── ca_tx_trends.png                 # CA vs TX trend plot
│   ├── ny_tx_trends.png                 # NY vs TX trend plot
│   ├── event_study_ca.png               # CA event study plot
│   └── event_study_ny.png               # NY event study plot
│
├── results/
│   ├── did_summary_ca.txt               # CA vs TX regression summary
│   └── did_summary_ny.txt               # NY vs TX regression summary
│
├── main.py                              # Entry point: prompts and calls DiD script
├── did_analysis.py                      # Core logic: DiD regressions and plots
├── requirements.txt                     # Dependencies
└── README.md                            # Project overview and usage
```

---

## 📈 Data Source

- **Source**: [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org)
- **Sector**: NAICS 722 – Food Services and Drinking Places  
- **States**: California, New York, Texas  
- **Period**: January 2020 – July 2025  
- **Frequency**: Monthly, seasonally adjusted

---

## 🧪 Methodology Summary

- **Difference-in-Differences (DiD)**:
  - CA vs TX (Policy date: April 2024, $20 fast food wage)
  - NY vs TX (Policy date: January 2025, $0.50 statewide increase)
- **Event Studies**:
  - Month-by-month effects before and after policy dates
  - Includes 95% confidence intervals to assess statistical significance

---

## ✅ How to Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/minwage-did.git
   cd minwage-did
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis (interactive prompt)**  
   ```bash
   python main.py
   ```

   Choose which policy to analyze:
   ```
   Enter 1 to run CA vs TX analysis
   Enter 2 to run both CA and NY analyses
   ```

4. **Output**  
   - Regression results are saved to the `results/` folder
   - Visualizations are saved to the `figures/` folder

---

## 📄 Paper Citation

If you reference this project or build on the analysis, please cite:

> Baker, P. (2025). *Minimum Wage Hikes and Sectoral Employment: Evidence from California and New York*. George Mason University, Department of Computational Social Science.

---

## 📬 Contact

**Peter Baker**  
PhD Student, Computational Social Science  
Email: pcbaker1969@gmail.com  
GitHub: [@pcbaker4669](https://github.com/pcbaker4669)
