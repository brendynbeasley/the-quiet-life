# Hicks (1935) on modern data: findings

## In plain English

In 1935 John Hicks suggested that a company with no serious competition takes part of its reward as a quiet life,
running less efficiently than it could. If so, industries dominated by a few companies should keep more weak plants
alive and improve more slowly. This study checks that across all 86 four-digit US manufacturing industries.

- **Concentrated industries have a wider gap in output per worker hour.** In tobacco (Altria, Reynolds American) a
  plant at the 90th percentile produces about 21 times as much per hour as one at the 10th, and in motor vehicles
  (GM, Ford, Stellantis, Toyota) about 12 times, against about 3 times among machine shops. The pattern holds in every Census since 2002.
- **Counting machinery and materials, most of that gap goes away.** Measured by total factor productivity, which
  counts equipment and materials as well as labor, the gap is not reliably wider in concentrated industries. Motor vehicles drop to a spread of 2.0.
  Only tobacco, whose productivity fell faster than any other industry's from 2007 to 2019, looks like Hicks's
  picture.
- **Concentrated industries did not improve more slowly.** From 2007 to 2019 productivity growth was unrelated to
  concentration.
- **Industries that consolidated did not let their laggards fall further behind.** Between 2002 and 2017 the gap
  between best and worst plants widened least where concentration rose most (leather tanning narrowed; motor
  vehicles, which fragmented, widened), though the slope is not significant at 5% (p = 0.067). Weighted by size,
  consolidating industries grew a little more slowly through 2023, a result that leans on a few very large industries
  and is not significant through 2019.

The essay version is in the [README](../README.md). Methods and reproduction are in
[TECHNICAL.md](../TECHNICAL.md).

## Key to the labels

*CR4* = share of industry shipments made by the 4 largest companies (%). *HHI* = Herfindahl-Hirschman index of the
50 largest companies. *Gap* or *d9010* = log productivity of the 90th-percentile plant minus the 10th (DiSP).
*Spread* or *ratio_90_10* = exp(gap), the 90th plant's productivity divided by the 10th's. *lp* = output per hour.
*tfp* = total factor productivity. *Growth* = average annual log growth of the BLS index, percent. *coef_per_point*
= change in the outcome per percentage point of CR4 (or per 1,000 HHI points). *ratio_cr4_60_vs_20* = predicted
spread at CR4 = 60 divided by predicted spread at CR4 = 20. Standard errors are HC1. *Fell most ... rose most* =
quartiles of the change in CR4 from 2002 to 2017. *leaders* = today's best-known producers in the industry, chosen
by judgment; Census does not name firms.

## Summary of the tests

| Test | Estimate | p | Reading |
|---|---|---|---|
| Output-per-hour gap on CR4, 2017 | +0.0092 per point | 0.004 | Wider in concentrated industries |
| TFP gap on CR4, 2017 | +0.0042 per point | 0.21 | No reliable difference |
| TFP gap on CR4, tobacco dropped | +0.0008 per point | 0.71 | No difference |
| TFP growth 2007–19 on CR4 | +0.0027 per point | 0.80 | No difference |
| Change in TFP gap on change in CR4, 2002→2017 | −0.0085 per point | 0.067 | Gap narrowed where concentration rose |
| TFP growth 2002–23 on change in CR4, shipment-weighted | −0.0194 per point | 0.012 | Slower growth where concentration rose; equal-weight p = 0.56 |

## Every table

The figures are [dispersion_vs_concentration.png](dispersion_vs_concentration.png) and
[consolidation_scatter.png](consolidation_scatter.png). The full industry panel, with every variable for all 86
industries, is [industry_panel.csv](industry_panel.csv).

### `flat_top.csv`

| deviation_from_best_output_pct | share_of_max_profit_lost_pct | example_naics | example_shipments_bn | example_margin_bn | example_margin_lost_mn |
|---|---|---|---|---|---|
| 5 | 0.25 | 3311 | 129.8 | 38.7 | 97 |
| 10 | 1.00 | 3311 | 129.8 | 38.7 | 387 |
| 20 | 4.00 | 3311 | 129.8 | 38.7 | 1,548 |
| 30 | 9.00 | 3311 | 129.8 | 38.7 | 3,482 |

### `worked_examples.csv`

| item | value |
|---|---|
| steel mills 2022, top-4 shipments ($bn) | 77.268 |
| steel mills 2022, industry shipments ($bn) | 129.832 |
| steel mills 2022, CR4 computed (%) | 59.514 |
| steel mills 2022, CR4 published (%) | 59.500 |
| steel mills 2015-19, log output-per-hour gap 90-10 | 2.089 |
| steel mills 2015-19, output-per-hour spread 90/10 | 8.074 |
| steel mills 2015-19, log TFP gap 90-10 | 0.968 |
| steel mills 2015-19, TFP spread 90/10 | 2.633 |

### `sample_summary.csv`

| industries | establishments_2017 | shipments_2017_tn | industries_cr4_40_plus | median_tfp_growth_2007_2019 | slowest_tfp_growth_industry |
|---|---|---|---|---|---|
| 86 | 291,586 | 5.549 | 19 | -0.364 | 3122 |

### `cross_section_tests.csv`

| outcome | spec | coef_per_point | se | ci_low | ci_high | p | n | log_estabs_coef | ratio_cr4_60_vs_20 |
|---|---|---|---|---|---|---|---|---|---|
| TFP gap, 90th vs 10th percentile plant (log points) | CR4 alone | 0.0042 | 0.0033 | -0.0023 | 0.0107 | 0.209 | 86 |  | 1.18 |
| TFP gap, 90th vs 10th percentile plant (log points) | CR4 + log establishments | 0.0082 | 0.0040 | 0.0005 | 0.0160 | 0.038 | 86 | 0.080 | 1.39 |
| TFP gap, 90th vs 10th percentile plant (log points) | CR4 + log establishments + subsector effects | 0.0079 | 0.0035 | 0.0010 | 0.0147 | 0.024 | 86 | 0.094 | 1.37 |
| TFP gap, 90th vs 10th percentile plant (log points) | CR4, weighted by shipments | -0.0000 | 0.0041 | -0.0080 | 0.0079 | 0.991 | 86 |  | 1.00 |
| TFP gap, 90th vs 10th percentile plant (log points) | CR4, tobacco dropped | 0.0008 | 0.0021 | -0.0033 | 0.0049 | 0.712 | 85 |  | 1.03 |
| TFP gap, 90th vs 10th percentile plant (log points) | CR4 + log establishments, tobacco dropped | 0.0043 | 0.0026 | -0.0008 | 0.0095 | 0.101 | 85 | 0.066 | 1.19 |
| TFP gap, 90th vs 10th percentile plant (log points) | HHI (per 1,000) instead of CR4 | -0.0622 | 0.1223 | -0.3018 | 0.1774 | 0.611 | 79 |  |  |
| TFP gap, 90th vs 10th percentile plant (log points) | CR4 in 2007 instead of 2017 | 0.0069 | 0.0031 | 0.0009 | 0.0129 | 0.023 | 86 |  | 1.32 |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | CR4 alone | 0.0092 | 0.0032 | 0.0030 | 0.0154 | 0.004 | 86 |  | 1.45 |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | CR4 + log establishments | 0.0114 | 0.0042 | 0.0031 | 0.0197 | 0.007 | 86 | 0.044 | 1.58 |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | CR4 + log establishments + subsector effects | 0.0099 | 0.0042 | 0.0017 | 0.0182 | 0.018 | 86 | 0.088 | 1.49 |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | CR4, weighted by shipments | 0.0106 | 0.0038 | 0.0031 | 0.0181 | 0.005 | 86 |  | 1.53 |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | CR4, tobacco dropped | 0.0070 | 0.0032 | 0.0008 | 0.0133 | 0.028 | 85 |  | 1.33 |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | CR4 + log establishments, tobacco dropped | 0.0089 | 0.0042 | 0.0006 | 0.0172 | 0.035 | 85 | 0.035 | 1.43 |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | HHI (per 1,000) instead of CR4 | 0.4800 | 0.1707 | 0.1454 | 0.8146 | 0.005 | 79 |  |  |
| Output-per-hour gap, 90th vs 10th percentile plant (log points) | CR4 in 2007 instead of 2017 | 0.0140 | 0.0034 | 0.0073 | 0.0207 | 0.000 | 86 |  | 1.75 |
| TFP growth 2007-2019 (% a year) | CR4 alone | 0.0027 | 0.0105 | -0.0179 | 0.0233 | 0.798 | 86 |  |  |
| TFP growth 2007-2019 (% a year) | CR4 + log establishments | -0.0109 | 0.0113 | -0.0330 | 0.0113 | 0.336 | 86 | -0.268 |  |
| TFP growth 2007-2019 (% a year) | CR4 + log establishments + subsector effects | -0.0045 | 0.0109 | -0.0258 | 0.0167 | 0.676 | 86 | -0.099 |  |
| TFP growth 2007-2019 (% a year) | CR4, weighted by shipments | -0.0049 | 0.0053 | -0.0154 | 0.0055 | 0.354 | 86 |  |  |
| TFP growth 2007-2019 (% a year) | CR4, tobacco dropped | 0.0118 | 0.0091 | -0.0060 | 0.0295 | 0.194 | 85 |  |  |
| TFP growth 2007-2019 (% a year) | CR4 + log establishments, tobacco dropped | -0.0007 | 0.0093 | -0.0189 | 0.0176 | 0.942 | 85 | -0.233 |  |
| TFP growth 2007-2019 (% a year) | HHI (per 1,000) instead of CR4 | 0.5935 | 0.6298 | -0.6409 | 1.8279 | 0.346 | 79 |  |  |
| TFP growth 2007-2019 (% a year) | CR4 in 2007 instead of 2017 | 0.0029 | 0.0090 | -0.0147 | 0.0206 | 0.745 | 86 |  |  |
| Labor productivity growth 2007-2019 (% a year) | CR4 alone | 0.0158 | 0.0136 | -0.0108 | 0.0425 | 0.244 | 86 |  |  |
| Labor productivity growth 2007-2019 (% a year) | CR4 + log establishments | 0.0204 | 0.0171 | -0.0131 | 0.0540 | 0.232 | 86 | 0.091 |  |
| Labor productivity growth 2007-2019 (% a year) | CR4 + log establishments + subsector effects | 0.0105 | 0.0194 | -0.0275 | 0.0486 | 0.587 | 86 | -0.049 |  |
| Labor productivity growth 2007-2019 (% a year) | CR4, weighted by shipments | 0.0085 | 0.0099 | -0.0109 | 0.0278 | 0.392 | 86 |  |  |
| Labor productivity growth 2007-2019 (% a year) | CR4, tobacco dropped | 0.0026 | 0.0107 | -0.0184 | 0.0236 | 0.809 | 85 |  |  |
| Labor productivity growth 2007-2019 (% a year) | CR4 + log establishments, tobacco dropped | 0.0045 | 0.0129 | -0.0208 | 0.0298 | 0.729 | 85 | 0.035 |  |
| Labor productivity growth 2007-2019 (% a year) | HHI (per 1,000) instead of CR4 | 0.0208 | 0.7321 | -1.4140 | 1.4557 | 0.977 | 79 |  |  |
| Labor productivity growth 2007-2019 (% a year) | CR4 in 2007 instead of 2017 | 0.0046 | 0.0132 | -0.0214 | 0.0305 | 0.729 | 86 |  |  |

### `by_census_year.csv`

| census_year | dispersion_years | measure | n | coef_per_point | se | p | coef_no_tobacco | p_no_tobacco | mean_gap_log |
|---|---|---|---|---|---|---|---|---|---|
| 2002 | 2000-2004 | TFP | 86 | 0.0037 | 0.0030 | 0.2180 | 0.0010 | 0.602 | 1.032 |
| 2002 | 2000-2004 | output per hour | 86 | 0.0084 | 0.0024 | 0.0004 | 0.0073 | 0.004 | 1.724 |
| 2007 | 2005-2009 | TFP | 86 | 0.0054 | 0.0026 | 0.0385 | 0.0039 | 0.150 | 1.159 |
| 2007 | 2005-2009 | output per hour | 86 | 0.0099 | 0.0033 | 0.0025 | 0.0103 | 0.010 | 1.750 |
| 2012 | 2010-2014 | TFP | 86 | 0.0011 | 0.0026 | 0.6668 | -0.0010 | 0.628 | 1.134 |
| 2012 | 2010-2014 | output per hour | 86 | 0.0099 | 0.0030 | 0.0008 | 0.0081 | 0.007 | 1.848 |
| 2017 | 2015-2019 | TFP | 86 | 0.0042 | 0.0033 | 0.2087 | 0.0008 | 0.712 | 1.137 |
| 2017 | 2015-2019 | output per hour | 86 | 0.0092 | 0.0032 | 0.0035 | 0.0070 | 0.028 | 1.868 |

### `concentration_groups.csv`

| top4_share_2017 | industries | median_estabs | median_tfp_gap_log | median_lp_gap_log | median_tfp_growth | tfp_ratio_90_10 | lp_ratio_90_10 |
|---|---|---|---|---|---|---|---|
| under 20% | 27 | 4,991 | 1.055 | 1.652 | -0.362 | 2.871 | 5.215 |
| 20-40% | 40 | 1,668 | 1.020 | 1.807 | -0.547 | 2.774 | 6.095 |
| 40-60% | 14 | 810 | 1.095 | 1.767 | -0.136 | 2.988 | 5.851 |
| 60% or more | 5 | 305 | 1.157 | 2.256 | -0.393 | 3.181 | 9.547 |

### `named_industries.csv`

| naics4 | industry | leaders | cr4_2017 | establishments_2017 | lp_ratio_90_10 | tfp_ratio_90_10 | tfp_growth_2007_2019 | shipments_2017_bn |
|---|---|---|---|---|---|---|---|---|
| 3122 | Tobacco manufacturing | Altria (Marlboro), Reynolds American (Camel, Newport) | 91.1 | 166 | 20.7 | 10.2 | -2.52 | 47.5 |
| 3364 | Aerospace product and parts manufacturing | Boeing, Lockheed Martin, RTX, GE Aerospace | 65.4 | 1,773 | 6.0 | 3.2 | -0.39 | 249.8 |
| 3352 | Household appliance manufacturing | Whirlpool, GE Appliances, Electrolux | 62.9 | 305 | 5.4 | 4.2 | 0.40 | 22.7 |
| 3361 | Motor vehicle manufacturing | GM, Ford, Stellantis, Toyota, Tesla | 61.5 | 313 | 12.0 | 2.0 | -0.71 | 323.4 |
| 3311 | Iron and steel mills and ferroalloy manufacturing | Nucor, Cleveland-Cliffs, Steel Dynamics, U.S. Steel | 50.1 | 292 | 8.1 | 2.6 | 0.97 | 87.6 |
| 3221 | Pulp, paper, and paperboard mills | International Paper, Domtar, Georgia-Pacific | 45.2 | 367 | 3.6 | 2.3 | 0.29 | 77.4 |
| 3116 | Animal slaughtering and processing | Tyson, JBS, Cargill, National Beef | 42.5 | 3,509 | 7.7 | 4.2 | -0.37 | 215.7 |
| 3241 | Petroleum and coal products manufacturing | Marathon, Valero, ExxonMobil, Phillips 66 | 42.0 | 2,116 | 11.3 | 2.2 | -0.32 | 543.5 |
| 3256 | Soap, cleaning compound, and toilet preparation manufacturing | Procter & Gamble, Colgate-Palmolive, Clorox | 41.1 | 2,258 | 10.9 | 4.9 | -1.26 | 82.5 |
| 3341 | Computer and peripheral equipment manufacturing | Dell, HP, Hewlett Packard Enterprise | 39.5 | 948 | 51.0 | 8.6 | 2.35 | 20.3 |
| 3254 | Pharmaceutical and medicine manufacturing | Pfizer, Merck, Eli Lilly, Johnson & Johnson | 35.7 | 2,384 | 6.2 | 5.0 | -0.78 | 211.2 |
| 3121 | Beverage manufacturing | Coca-Cola, PepsiCo, Anheuser-Busch, Molson Coors | 33.2 | 9,011 | 10.4 | 4.8 | -0.56 | 107.5 |
| 3344 | Semiconductor and other electronic component manufacturing | Intel, Texas Instruments, Micron, GlobalFoundries | 25.2 | 3,922 | 30.3 | 27.2 | 1.12 | 95.3 |
| 3251 | Basic chemical manufacturing | Dow, LyondellBasell, ExxonMobil Chemical | 24.7 | 2,459 | 15.7 | 9.4 | -0.61 | 218.0 |
| 3231 | Printing and related support activities | RR Donnelley, Quad, thousands of local printers | 13.8 | 25,262 | 3.5 | 2.4 | 0.21 | 82.8 |
| 3327 | Machine shops; turned product; and screw, nut, and bolt manufacturing | thousands of small machine shops | 4.3 | 22,804 | 3.2 | 2.6 | -0.62 | 66.6 |

### `dispersion_extremes.csv`

| naics4 | title | cr4_2017 | estabs | lp_ratio | tfp_ratio |
|---|---|---|---|---|---|
| 3162 | Footwear manufacturing | 42.1 | 221 | 3.01 | 1.82 |
| 3151 | Apparel knitting mills | 29.4 | 226 | 3.16 | 2.19 |
| 3327 | Machine shops; turned product; and screw, nut, and bolt manufacturing | 4.3 | 22,804 | 3.18 | 2.59 |
| 3211 | Sawmills and wood preservation | 18.2 | 3,306 | 5.64 | 4.01 |
| 3122 | Tobacco manufacturing | 91.1 | 166 | 20.65 | 10.20 |
| 3344 | Semiconductor and other electronic component manufacturing | 25.2 | 3,922 | 30.34 | 27.22 |
| 3341 | Computer and peripheral equipment manufacturing | 39.5 | 948 | 51.02 | 8.64 |

### `consolidation_tests.csv`

| outcome | weights | coef_per_point | se | ci_low | ci_high | p | n | leave_one_out_min | leave_one_out_max | effect_of_10_point_rise |
|---|---|---|---|---|---|---|---|---|---|---|
| Change in TFP gap, 2000-04 to 2015-19 (log points) | equal weights | -0.0085 | 0.0046 | -0.0175 | 0.0006 | 0.067 | 86 | -0.0112 | -0.0064 | -0.085 |
| Change in TFP gap, 2000-04 to 2015-19 (log points) | weighted by 2017 shipments | -0.0038 | 0.0045 | -0.0126 | 0.0049 | 0.394 | 86 |  |  | -0.038 |
| Change in output-per-hour gap, 2000-04 to 2015-19 (log points) | equal weights | -0.0073 | 0.0045 | -0.0161 | 0.0015 | 0.103 | 86 | -0.0086 | -0.0051 | -0.073 |
| Change in output-per-hour gap, 2000-04 to 2015-19 (log points) | weighted by 2017 shipments | -0.0013 | 0.0045 | -0.0101 | 0.0074 | 0.765 | 86 |  |  | -0.013 |
| TFP growth 2002-2019 (% a year) | equal weights | -0.0112 | 0.0190 | -0.0484 | 0.0260 | 0.554 | 86 | -0.0174 | 0.0020 | -0.112 |
| TFP growth 2002-2019 (% a year) | weighted by 2017 shipments | -0.0236 | 0.0180 | -0.0589 | 0.0116 | 0.189 | 86 |  |  | -0.236 |
| Labor productivity growth 2002-2019 (% a year) | equal weights | 0.0086 | 0.0279 | -0.0461 | 0.0633 | 0.758 | 86 | -0.0003 | 0.0223 | 0.086 |
| Labor productivity growth 2002-2019 (% a year) | weighted by 2017 shipments | -0.0349 | 0.0192 | -0.0725 | 0.0027 | 0.069 | 86 |  |  | -0.349 |
| TFP growth 2002-2023, CR4 change 2002-2022 (% a year) | equal weights | -0.0071 | 0.0122 | -0.0311 | 0.0169 | 0.559 | 86 | -0.0129 | -0.0011 | -0.071 |
| TFP growth 2002-2023, CR4 change 2002-2022 (% a year) | weighted by 2017 shipments | -0.0194 | 0.0077 | -0.0345 | -0.0042 | 0.012 | 86 |  |  | -0.194 |
| Labor productivity growth 2002-2023, CR4 change 2002-2022 | equal weights | 0.0012 | 0.0166 | -0.0314 | 0.0339 | 0.941 | 86 | -0.0047 | 0.0088 | 0.012 |
| Labor productivity growth 2002-2023, CR4 change 2002-2022 | weighted by 2017 shipments | -0.0106 | 0.0196 | -0.0490 | 0.0278 | 0.588 | 86 |  |  | -0.106 |

### `consolidation_quartiles.csv`

| top4_share_2002_to_2017 | industries | mean_change_cr4 | mean_change_tfp_gap | mean_change_lp_gap | median_tfp_growth | median_lp_growth |
|---|---|---|---|---|---|---|
| fell most | 22 | -9.891 | 0.202 | 0.191 | 0.245 | 0.604 |
| fell a little | 21 | -2.052 | 0.110 | 0.165 | 0.089 | 0.418 |
| rose a little | 21 | 2.243 | 0.067 | 0.137 | 0.365 | 0.459 |
| rose most | 22 | 7.873 | 0.036 | 0.084 | 0.374 | 0.881 |

### `consolidation_named.csv`

| naics4 | industry | leaders | cr4_2002 | cr4_2017 | change_cr4 | firms_2002 | firms_2017 | tfp_ratio_2000_04 | tfp_ratio_2015_19 | tfp_growth_2002_2019 |
|---|---|---|---|---|---|---|---|---|---|---|
| 3361 | Motor vehicle manufacturing | GM, Ford, Stellantis, Toyota, Honda, Tesla | 81.2 | 61.5 | -19.7 | 308 | 264 | 1.74 | 1.99 | 0.16 |
| 3259 | Other chemical product and preparation manufacturing |  | 30.4 | 11.1 | -19.3 | 2,304 | 1,824 | 3.06 | 3.91 | -0.14 |
| 3365 | Railroad rolling stock manufacturing | Wabtec, Greenbrier, Trinity | 55.0 | 40.0 | -15.0 | 147 | 153 | 1.90 | 3.00 | -0.57 |
| 3363 | Motor vehicle parts manufacturing | Lear, BorgWarner, Magna | 28.6 | 15.3 | -13.3 | 4,565 | 4,035 | 2.64 | 2.28 | 1.04 |
| 3313 | Alumina and aluminum production and processing | Alcoa, Century Aluminum, Novelis | 50.9 | 38.4 | -12.5 | 435 | 323 | 2.90 | 3.28 | 1.90 |
| 3343 | Audio and video equipment manufacturing |  | 43.2 | 30.8 | -12.4 | 544 | 464 | 3.05 | 3.31 | 1.87 |
| 3325 | Hardware manufacturing |  | 19.3 | 29.2 | 9.9 | 807 | 573 | 2.14 | 2.16 | -0.33 |
| 3162 | Footwear manufacturing |  | 32.0 | 42.1 | 10.1 | 320 | 203 | 2.75 | 1.82 | 0.24 |
| 3362 | Motor vehicle body and trailer manufacturing | Thor Industries, Forest River, Wabash | 20.1 | 32.3 | 12.2 | 1,915 | 1,649 | 1.82 | 1.80 | -0.20 |
| 3159 | Apparel accessories and other apparel manufacturing |  | 15.0 | 28.0 | 13.0 | 1,362 | 568 | 3.09 | 2.52 | -1.01 |
| 3161 | Leather and hide tanning and finishing |  | 45.8 | 60.0 | 14.2 | 246 | 169 | 2.57 | 2.29 | 2.07 |
| 3379 | Other furniture related product manufacturing | Tempur Sealy, Serta Simmons, Sleep Number (mattresses) | 32.2 | 52.6 | 20.4 | 974 | 638 | 1.88 | 2.98 | 0.32 |

### `consolidation_weighted_influence.csv` (the three lowest and three highest slopes)

| naics4 | industry | coef_without | p_without | coef_with_all |
|---|---|---|---|---|
| 3361 | Motor vehicle manufacturing | -0.0229 | 0.105 | -0.0194 |
| 3254 | Pharmaceutical and medicine manufacturing | -0.0212 | 0.009 | -0.0194 |
| 3121 | Beverage manufacturing | -0.0210 | 0.008 | -0.0194 |
| 3344 | Semiconductor and other electronic component manufacturing | -0.0169 | 0.019 | -0.0194 |
| 3241 | Petroleum and coal products manufacturing | -0.0145 | 0.047 | -0.0194 |
| 3363 | Motor vehicle parts manufacturing | -0.0143 | 0.035 | -0.0194 |

