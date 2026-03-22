# Eurozone Government Bond VaR Model

## Overview
A Historical and Parametric Value at Risk (VaR) model built in Python using 
real sovereign bond yield data sourced directly from the ECB Data Portal.

## Countries Covered
Germany, France, Italy, Spain, Portugal — the five core eurozone sovereigns 
monitored by the European Stability Mechanism (ESM).

## Methodology
- **Historical VaR (99%):** 388 months of ECB yield data sorted by loss magnitude; 
  VaR estimated at the 1st percentile
- **Parametric VaR (99%):** Calculated using mean + (z-score × standard deviation), 
  z = -2.326 at 99% confidence
- **Fat-tail analysis:** Comparison of both methods reveals the peripheral sovereign 
  bonds (Italy, Portugal) exhibit significant fat-tail risk beyond normal distribution assumptions

## Key Results
| Country  | Historical VaR | Parametric VaR |
|----------|---------------|----------------|
| Germany  | -0.37 pp      | -0.40 pp       |
| France   | -0.45 pp      | -0.48 pp       |
| Italy    | -0.94 pp      | -0.70 pp       |
| Spain    | -0.67 pp      | -0.59 pp       |
| Portugal | -1.03 pp      | -0.76 pp       |

## Tools Used
Python, pandas, NumPy, matplotlib | Data: ECB Data Portal
