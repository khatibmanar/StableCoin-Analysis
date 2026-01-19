# Stablecoin On-Chain Analysis: USDC and Market Volatility

This repository contains a research-oriented analysis of on-chain USDC activity on Ethereum, developed as a resume-ready project to demonstrate blockchain data analysis and applied econometric skills. The project is structured in two phases that progressively move from raw blockchain data collection to more structured empirical analysis.

---

## Project Overview

The goal of this project is to explore how stablecoin usage responds to conditions in cryptocurrency markets, with a focus on Ethereum-based USDC transactions. Specifically, the analysis examines whether periods of higher ETH price volatility are associated with changes in USDC transaction activity, measured by both transaction counts and transaction volumes.

The project is designed as a research notebook rather than a production pipeline, with an emphasis on transparency, documentation of data limitations, and clear interpretation of results.

---

## Phase 1: Raw On-Chain Data Collection (Etherscan API)

**Objective:**  
Demonstrate basic blockchain data collection, data cleaning, and awareness of API constraints using raw Ethereum transaction data.

**Data Source:**

- Etherscan ERC-20 transfer API (USDC contract)

**Key Steps:**

- Pulled raw USDC transfer data using the Etherscan API
- Documented the API’s 10,000-transaction-per-query limitation
- Implemented a block-by-day looping strategy to extend coverage across multiple days
- Explicitly acknowledged truncation on high-activity days as a data limitation rather than a bug

**Outcome:**  
Phase 1 establishes familiarity with:

- ERC-20 transfer mechanics
- Ethereum block structure
- Practical limitations of public blockchain APIs
- Transparent documentation of incomplete or biased samples

This phase is intentionally exploratory and serves as motivation for moving to indexed blockchain data in Phase 2.

---

## Phase 2: Indexed Data and Empirical Analysis (Dune Analytics)

**Objective:**  
Use indexed blockchain data to conduct a more systematic analysis of the relationship between market volatility and stablecoin usage.

**Data Sources:**

- Dune Analytics (Ethereum USDC transfer data)
- ETH price data (used to construct realized volatility)

**Measures of Stablecoin Activity:**

- Daily USDC transaction counts (extensive margin)
- Daily USDC transaction volume (intensive margin)

**Methodology:**

- Constructed daily ETH realized volatility using rolling windows
- Estimated OLS regressions with heteroskedasticity-robust (HC1) standard errors
- Ran baseline regressions and robustness checks including:
  - Lagged volatility
  - Day-of-week fixed effects
- Complemented regression results with a time-series visualization

**Key Findings:**

- Higher ETH volatility is associated with increased USDC transaction counts
- The relationship between volatility and transaction volume is weaker and less precisely timed
- Results are descriptive and exploratory rather than causal

---

## Implementation Notes

- All analysis is contained in Jupyter notebooks
- API keys and raw CSV outputs are excluded
- Notebooks are structured as research narratives with markdown explanations

---

## How to Reproduce Results

All analysis in this repository is contained in Jupyter notebooks and can be reproduced by running the notebooks sequentially.

To reproduce the analysis:

1. Clone the repository and create a Python environment with standard data analysis packages (e.g., pandas, numpy, matplotlib, statsmodels).
2. Open the notebooks in the `notebooks/` directory.
3. Run the Phase 1 notebook to review raw on-chain data collection.
4. Run the Phase 2 notebook to reproduce the indexed data analysis, regressions, and figures.

The Phase 2 analysis relies on data queried from Dune Analytics and public ETH price data. API keys and raw query outputs are not included in the repository and must be obtained separately if re-running the data extraction steps.

---

## Notes on Scope and Limitations

- The analysis focuses exclusively on on-chain Ethereum activity and does not capture off-chain or cross-chain USDC usage
- Results should be interpreted as descriptive associations
- The project prioritizes clarity, reproducibility, and research judgment over model complexity

---

## Motivation

This project was developed to build hands-on experience with blockchain data and applied empirical analysis in the context of stablecoins and financial markets. It is intended as a learning and demonstration tool rather than a finished academic paper.
