import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------
# STEP 1: LOAD THE REAL ECB DATA
# -------------------------------------------------------


germany  = pd.read_csv("Germany.csv",  skiprows=4, usecols=[0,2], names=['date','yield'])
france   = pd.read_csv("France.csv",   skiprows=4, usecols=[0,2], names=['date','yield'])
italy    = pd.read_csv("Italy.csv",    skiprows=4, usecols=[0,2], names=['date','yield'])
spain    = pd.read_csv("Spain.csv",    skiprows=4, usecols=[0,2], names=['date','yield'])
portugal = pd.read_csv("Portugal.csv", skiprows=4, usecols=[0,2], names=['date','yield'])


print("Germany data - first 5 rows:")
print(germany.head())
print("Total rows:", len(germany))
# STEP 2: CALCULATE MONTHLY YIELD CHANGES
# -------------------------------------------------------

germany['change']  = germany['yield'].diff()
france['change']   = france['yield'].diff()
italy['change']    = italy['yield'].diff()
spain['change']    = spain['yield'].diff()
portugal['change'] = portugal['yield'].diff()


all_changes = pd.concat([
    germany['change'].rename('Germany'),
    france['change'].rename('France'),
    italy['change'].rename('Italy'),
    spain['change'].rename('Spain'),
    portugal['change'].rename('Portugal')
], axis=1)


all_changes = all_changes.dropna()

print("Monthly yield changes - first 5 rows:")
print(all_changes.head())
print("Shape:", all_changes.shape)
var_99 = np.percentile(all_changes, 1, axis=0)


var_results = pd.DataFrame({
    'Country': ['Germany', 'France', 'Italy', 'Spain', 'Portugal'],
    'Historical_VaR_99': var_99
})

print("\n--- HISTORICAL VAR RESULTS (99% confidence) ---")
print(var_results)
print("\nInterpretation: On 99% of months, yield changes")
print("did NOT exceed these levels (in percentage points)")
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
fig.suptitle('Historical VaR Analysis — Eurozone Government Bonds\nSource: ECB Data Portal',
             fontsize=14, fontweight='bold')

countries = ['Germany', 'France', 'Italy', 'Spain', 'Portugal']
colors = ['#003399', '#002395', '#009246', '#c60b1e', '#006600']

for i, country in enumerate(countries):
    row = i // 3
    col = i % 3
    ax = axes[row][col]

    # Plot the histogram of yield changes
    ax.hist(all_changes[country], bins=40, color=colors[i],
            alpha=0.7, edgecolor='white')

    # Draw the VaR line in red
    var_line = var_results[var_results['Country'] == country]['Historical_VaR_99'].values[0]
    ax.axvline(x=var_line, color='red', linewidth=2, linestyle='--',
               label=f'99% VaR: {var_line:.2f}')

    ax.set_title(f'{country} 10Y Yields', fontweight='bold')
    ax.set_xlabel('Monthly yield change (pp)')
    ax.set_ylabel('Frequency')
    ax.legend(fontsize=9)

# Hide the 6th empty subplot
axes[1][2].set_visible(False)

plt.tight_layout()
plt.savefig('var_chart.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nChart saved as var_chart.png")
Z_SCORE_99 = -2.326  

para_var = []
for country in countries:
    mean = all_changes[country].mean()   # average monthly change
    std  = all_changes[country].std()    # standard deviation
    pvar = mean + (Z_SCORE_99 * std)     # parametric VaR formula
    para_var.append(pvar)

var_results['Parametric_VaR_99'] = para_var

print("\n--- COMPARISON: HISTORICAL vs PARAMETRIC VAR ---")
print(var_results.to_string(index=False))
print("\nNote: Difference between methods shows fat-tail risk")
print("Larger gap = more extreme events than normal dist assumes")

var_results.to_csv('var_results.csv', index=False)
print("\nResults exported to var_results.csv for PowerBI dashboard")