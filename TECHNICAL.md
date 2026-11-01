# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the method, every test statistic and
how to reproduce the results. All tables are in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

J. R. Hicks, "Annual Survey of Economic Theory: The Theory of Monopoly," *Econometrica* 3(1), January 1935, pp. 1–20.
A survey of Zeuthen, Schneider, Chamberlin and Robinson. In section I.5 ("The 'private' factors," p. 8) Hicks argues
that profit varies little near its maximum, that monopolists may face sharply rising subjective costs of effort, and
that they will therefore not bother to get very close to maximum profit. The paragraph ends "The best of all
monopoly profits is a quiet life." The paper reports no data and no estimate. I read the full text in the scan of
*Econometrica* volume 3 held by the Internet Archive (item `sim_econometrica_1935_3`).

| | |
|---|---|
| Question | Does a firm sheltered from competition take part of its reward as slack instead of maximum profit? |
| Test (mine; Hicks has none) | Across industries, regress the 90–10 log productivity gap and productivity growth on CR4 |
| Hicks's answer | Probably yes, qualitatively; no number |

## Headline results

| Test | Estimate per point of CR4 | 95% CI | p | N |
|---|---|---|---|---|
| Output-per-hour gap (2015–19) on CR4 2017 | +0.0092 | [0.0030, 0.0154] | 0.004 | 86 |
| Same, tobacco dropped | +0.0070 | [0.0008, 0.0133] | 0.028 | 85 |
| TFP gap (2015–19) on CR4 2017 | +0.0042 | [−0.0023, 0.0107] | 0.21 | 86 |
| Same, tobacco dropped | +0.0008 | [−0.0033, 0.0049] | 0.71 | 85 |
| TFP growth 2007–19 on CR4 2017 | +0.0027 | [−0.0179, 0.0233] | 0.80 | 86 |
| Δ TFP gap on Δ CR4, 2002→2017 | −0.0085 | [−0.0175, 0.0006] | 0.067 | 86 |
| TFP growth 2002–23 on Δ CR4 2002→2022, shipment-weighted | −0.0194 | [−0.0345, −0.0042] | 0.012 | 86 |

Output-per-hour spreads are wider in concentrated industries in every Census year (slopes 0.0084, 0.0099, 0.0099 and
0.0092 for 2002, 2007, 2012 and 2017, all p < 0.01). TFP spreads are not, except in specifications that keep tobacco
and control for plant counts (with or without subsector effects) or use 2007 concentration. Productivity growth is unrelated to concentration in the
cross-section. Within industries, rising concentration came with narrowing TFP gaps.

## Data

All files are public and were downloaded on 1 November 2026. Everything under 10 MB is committed in `data/raw/`.

| File | Source | Contents |
|---|---|---|
| `census/EC0231SR12.zip`, `EC0731SR12.zip`, `EC1231SR2.zip` | www2.census.gov, Economic Census 2002, 2007, 2012, sector 31 | CR4, CR8, HHI (top 50), company counts, shipments |
| `census/EC1700SIZECONCEN.zip`, `EC2200SIZECONCEN.zip` | Economic Census 2017, 2022, sector 00 | The same, plus establishments and top-4 shipments |
| `census/EC2231BASIC.zip` | Economic Census 2022, sector 31 | Shipments, payroll, benefits, materials (for the flat-top example) |
| `disp/total_factor_productivity.csv`, `disp/output_per_hour.csv`, `disp/readme.txt` | www2.census.gov/ces/disp (September 2024 release) | Within-industry dispersion of log productivity, 86 four-digit industries, 1987–2021 |
| `bls/bls_productivity_fred.csv` | BLS detailed-industry productivity via FRED, series `IPUEN{naics}M000000000` (TFP) and `IPUEN{naics}L000000000` (labor productivity) | Indices, 1987–2023 (TFP) and 1987–2025 (labor) |

All 86 DiSP industries appear in all five Censuses under the same four-digit code. NAICS revisions between 2002 and
2022 moved some six-digit products across four-digit lines; I used each Census's four-digit figures as published and
did not reallocate those products.

## Method

Rules applied to every test. I report every specification I ran, including two added after the first results (the
tobacco-dropped plant-count version and the 2007-concentration version).

1. Unit of observation is the four-digit NAICS manufacturing industry (86).
2. Dispersion $`D_i`$ is the DiSP 90–10 log gap, unweighted, averaged over 2000–04, 2005–09, 2010–14 and 2015–19 for
   the 2002, 2007, 2012 and 2017 Censuses. The 2022 Census is not paired with dispersion because DiSP ends in 2021.
3. Growth is average annual log growth of the BLS index, in percent, 2007–2019 for the cross-section and 2002–2019
   (and 2002–2023) for the extension.
4. Specifications reported for every outcome: CR4 alone; plus log establishments; plus three-digit subsector fixed
   effects; shipment-weighted; tobacco (NAICS 3122) dropped; log establishments with tobacco dropped; HHI per 1,000
   instead of CR4; CR4 in 2007 instead of 2017.
5. Heteroskedasticity-robust (HC1) standard errors. One observation per industry, so no clustering.

The cross-sectional equation, for industry $`i`$ in subsector $`s(i)`$ with $`N_i`$ establishments:

```math
D_i = \alpha + \beta\,\text{CR4}_i + \gamma \ln N_i + \delta_{s(i)} + \varepsilon_i, \qquad H_0:\ \beta = 0
```

The growth version replaces $`D_i`$ with $`g_i = 100\,[\ln A_{i,t_1} - \ln A_{i,t_0}]/(t_1 - t_0)`$, where
$`A`$ is the BLS index. The extension uses long differences, with equal and shipment weights and a leave-one-out
check on the equal-weight slope:

```math
\Delta D_i = \alpha + \beta\,\Delta \text{CR4}_i + u_i, \qquad \Delta x_i \equiv x_{i,2017} - x_{i,2002}
```

The flat-top calculation assumes linear demand $`p = a - bx`$ and constant marginal cost $`c`$, which give

```math
\frac{\Pi^* - \Pi\big((1+d)x^*\big)}{\Pi^*} = d^2
```

The steel example uses 2022 shipments minus payroll, benefits and materials ($38.7 billion) as the stand-in for
variable profit.

## Full test statistics

Every coefficient, standard error, 95% interval, p-value and N is in
[results/cross_section_tests.csv](results/cross_section_tests.csv) (32 rows: four outcomes by eight specifications),
[results/by_census_year.csv](results/by_census_year.csv) and
[results/consolidation_tests.csv](results/consolidation_tests.csv). Points worth recording:

- With log establishments in the TFP equation, its coefficient is +0.080, so at a given CR4 more plants means a wider
  gap. Because CR4 and log plants are negatively correlated, adding the control raises the CR4 slope to 0.0082
  (p = 0.038). Without tobacco that becomes 0.0043 (p = 0.101).
- The output-per-hour slope with HHI is 0.48 per 1,000 points (p = 0.005); for TFP it is −0.06 (p = 0.61). Census
  does not publish an HHI for 7 of the 86 industries in 2017, so these rows have N = 79.
- Δ TFP gap on Δ CR4, leave-one-out range −0.0112 to −0.0064. Shipment-weighted −0.0038 (p = 0.39).
- Shipment-weighted TFP growth 2002–2019 on Δ CR4 2002–2017 is −0.0236 (p = 0.19); the significant weighted growth
  result appears only with the 2002–2023 window.
- Weighted TFP growth 2002–2023 on Δ CR4 2002–2022 stays negative without each single industry, from −0.0229
  (without motor vehicles, p = 0.105) to −0.0143 (without motor vehicle parts, p = 0.035); see
  [results/consolidation_weighted_influence.csv](results/consolidation_weighted_influence.csv).
- In the extension, equal-weight versions of the growth tests are never significant (p between 0.55 and 0.94).

## Reproducing the results

```bash
pip install -r requirements.txt
python src/quiet_life.py        # flat top, panel, cross-industry tests, figure 1
python src/consolidation.py     # 2002 -> 2017 changes, figure 2
```

`python src/quiet_life.py --download` re-fetches every raw file (about 180 requests, paced). Both scripts print what
they loaded, what they kept and what they dropped.

## Repository layout

| Path | What it is |
|---|---|
| [src/quiet_life.py](src/quiet_life.py) | Data loading, flat top, panel, cross-industry tests, named table, figure 1 |
| [src/consolidation.py](src/consolidation.py) | Within-industry changes 2002→2017, quartiles, named movers, figure 2 |
| `results/*.csv`, `results/*.png` | Every number and chart in the README |
| `data/raw/` | Census, DiSP and BLS files as downloaded |

## References

- Autor, D., Dorn, D., Katz, L., Patterson, C. & Van Reenen, J. (2020). The fall of the labor share and the rise of
  superstar firms. *Quarterly Journal of Economics* 135(2).
- Bertrand, M. & Mullainathan, S. (2003). Enjoying the quiet life? Corporate governance and managerial preferences.
  *Journal of Political Economy* 111(5), 1043–1075.
- Demsetz, H. (1973). Industry structure, market rivalry, and public policy. *Journal of Law and Economics* 16(1).
- Giroud, X. & Mueller, H. (2010). Does corporate governance matter in competitive industries? *Journal of Financial
  Economics* 95(3), 312–331.
- Hicks, J. R. (1935). Annual survey of economic theory: the theory of monopoly. *Econometrica* 3(1), 1–20.
- Leibenstein, H. (1966). Allocative efficiency vs. "X-efficiency." *American Economic Review* 56(3), 392–415.
- Perelman, M. (2011). Retrospectives: X-efficiency. *Journal of Economic Perspectives* 25(4), 211–222.
- Stigler, G. (1976). The Xistence of X-efficiency. *American Economic Review* 66(1), 213–216.
- Syverson, C. (2004). Market structure and productivity: a concrete example. *Journal of Political Economy* 112(6),
  1181–1222.
