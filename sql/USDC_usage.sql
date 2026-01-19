-- Dune Analytics SQL
-- Purpose: Create daily measures of USDC activity on Ethereum.
--
-- This query aggregates USDC ERC-20 transfer events to compute:
--  - daily transaction counts
--  - total daily transfer volume
--
-- Source: Dune Analytics (tokens.transfers table).
--
-- The output is used in Phase 2 to study how ETH price volatility
-- is associated with stablecoin usage. Results are descriptive.
-- Time window covers the past 3 years because I had to copy it mannually from the preview table since the Dune free plan doesn't allow .csv installation.


SELECT
    block_date AS day,
    SUM(amount) AS daily_usdc_volume,
    COUNT(*) AS daily_usdc_tx_count
FROM tokens.transfers
WHERE
    blockchain = 'ethereum'
    AND symbol = 'USDC'
    AND block_date >= DATE_ADD('year', -3, CURRENT_DATE)
GROUP BY block_date
ORDER BY block_date