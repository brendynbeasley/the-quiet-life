"""Extension: when an industry consolidates, do its laggard plants get a quieter life?

The cross-industry test compares tobacco with sawmills. This script compares each
industry with itself. Between the 2002 and 2017 Economic Censuses some industries
became much more concentrated and others much less. Hicks's account predicts that
consolidation widens the gap between the best and worst plants and slows productivity
growth. The rival "superstar" account (Demsetz 1973; Autor et al. 2020) predicts that
consolidation comes from the best firms winning, with productivity growth that is the
same or faster.

Reads results/industry_panel.csv written by src/quiet_life.py, so run that first:
    python src/quiet_life.py
    python src/consolidation.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"

START, END = 2002, 2017       # Census years; dispersion windows 2000-04 and 2015-19
WEIGHT = "shipments_k_2017"   # size weight for the weighted versions
QUARTILE_LABELS = ["fell most", "fell a little", "rose a little", "rose most"]
# Well-known leaders for the industries that appear in the named table (my judgment)
LEADERS = {
    "3361": "GM, Ford, Stellantis, Toyota, Honda, Tesla",
    "3365": "Wabtec, Greenbrier, Trinity",
    "3363": "Lear, BorgWarner, Magna",
    "3313": "Alcoa, Century Aluminum, Novelis",
    "3362": "Thor Industries, Forest River, Wabash",
    "3379": "Tempur Sealy, Serta Simmons, Sleep Number (mattresses)",
}


def fit(y, x, data, weights=None):
    d = data.dropna(subset=[y, x])
    if weights:
        m = smf.wls(f"{y} ~ {x}", d, weights=d[weights]).fit(cov_type="HC1")
    else:
        m = smf.ols(f"{y} ~ {x}", d).fit(cov_type="HC1")
    return m, d


def leave_one_out(y, x, data):
    coefs = []
    for code in data.index:
        m, _ = fit(y, x, data.drop(index=code))
        coefs.append(m.params[x])
    return min(coefs), max(coefs)


def main():
    p = pd.read_csv(OUT / "industry_panel.csv", dtype={"naics4": str}).set_index("naics4")
    print(f"Loaded industry_panel.csv: {len(p)} industries")
    p["d_cr4"] = p[f"cr4_{END}"] - p[f"cr4_{START}"]
    p["d_cr4_2022"] = p["cr4_2022"] - p[f"cr4_{START}"]
    for m in ("tfp", "lp"):
        p[f"d_{m}_gap"] = p[f"{m}_d9010_{END}"] - p[f"{m}_d9010_{START}"]
    keep = p.dropna(subset=["d_cr4", "d_tfp_gap", "d_lp_gap", "tfp_growth_2002_2019"])
    print(f"Kept {len(keep)} industries with concentration and dispersion in both years; "
          f"dropped {len(p) - len(keep)}")

    tests = [
        ("d_tfp_gap", "d_cr4", "Change in TFP gap, 2000-04 to 2015-19 (log points)"),
        ("d_lp_gap", "d_cr4", "Change in output-per-hour gap, 2000-04 to 2015-19 (log points)"),
        ("tfp_growth_2002_2019", "d_cr4", "TFP growth 2002-2019 (% a year)"),
        ("lp_growth_2002_2019", "d_cr4", "Labor productivity growth 2002-2019 (% a year)"),
        ("tfp_growth_2002_2023", "d_cr4_2022", "TFP growth 2002-2023, CR4 change 2002-2022 (% a year)"),
        ("lp_growth_2002_2023", "d_cr4_2022", "Labor productivity growth 2002-2023, CR4 change 2002-2022"),
    ]
    rows = []
    for y, x, label in tests:
        for wname, w in [("equal weights", None), ("weighted by 2017 shipments", WEIGHT)]:
            m, d = fit(y, x, keep, w)
            lo, hi = leave_one_out(y, x, keep) if w is None else (np.nan, np.nan)
            rows.append({"outcome": label, "weights": wname, "coef_per_point": m.params[x],
                         "se": m.bse[x], "ci_low": m.conf_int().loc[x, 0], "ci_high": m.conf_int().loc[x, 1],
                         "p": m.pvalues[x], "n": len(d),
                         "leave_one_out_min": lo, "leave_one_out_max": hi,
                         "effect_of_10_point_rise": 10 * m.params[x]})
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "consolidation_tests.csv", index=False)
    print("\nWithin-industry changes, 2002 -> 2017:")
    print(res.round(4).to_string(index=False))

    # Which single industries move the weighted growth result
    m_all, _ = fit("tfp_growth_2002_2023", "d_cr4_2022", keep, WEIGHT)
    infl = []
    for code in keep.index:
        m, _ = fit("tfp_growth_2002_2023", "d_cr4_2022", keep.drop(index=code), WEIGHT)
        infl.append({"naics4": code, "industry": keep.title[code], "coef_without": m.params["d_cr4_2022"],
                     "p_without": m.pvalues["d_cr4_2022"]})
    infl = pd.DataFrame(infl).sort_values("coef_without")
    infl["coef_with_all"] = m_all.params["d_cr4_2022"]
    infl.to_csv(OUT / "consolidation_weighted_influence.csv", index=False)
    print("\nWeighted 2002-2023 TFP result without each industry (extremes):")
    print(pd.concat([infl.head(3), infl.tail(3)]).round(4).to_string(index=False))

    q = pd.qcut(keep.d_cr4, 4, labels=QUARTILE_LABELS)
    quart = keep.groupby(q, observed=True).agg(
        industries=("title", "size"), mean_change_cr4=("d_cr4", "mean"),
        mean_change_tfp_gap=("d_tfp_gap", "mean"), mean_change_lp_gap=("d_lp_gap", "mean"),
        median_tfp_growth=("tfp_growth_2002_2019", "median"),
        median_lp_growth=("lp_growth_2002_2019", "median"))
    quart = quart.rename_axis("top4_share_2002_to_2017").reset_index()
    quart.to_csv(OUT / "consolidation_quartiles.csv", index=False)
    print("\nBy quartile of the change in CR4, 2002 -> 2017:")
    print(quart.round(3).to_string(index=False))

    movers = keep.sort_values("d_cr4")
    movers = pd.concat([movers.head(6), movers.tail(6)])
    named = pd.DataFrame({
        "naics4": movers.index, "industry": movers.title,
        "leaders": [LEADERS.get(c, "") for c in movers.index],
        "cr4_2002": movers.cr4_2002, "cr4_2017": movers.cr4_2017, "change_cr4": movers.d_cr4,
        "firms_2002": movers.firms_2002, "firms_2017": movers.firms_2017,
        "tfp_ratio_2000_04": np.exp(movers.tfp_d9010_2002), "tfp_ratio_2015_19": np.exp(movers.tfp_d9010_2017),
        "tfp_growth_2002_2019": movers.tfp_growth_2002_2019})
    named.to_csv(OUT / "consolidation_named.csv", index=False)
    print("\nBiggest falls and rises in concentration:")
    print(named.drop(columns="leaders").round(2).to_string(index=False))

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axvline(0, color="#999999", lw=0.8)
    ax.scatter(keep.d_cr4, keep.d_tfp_gap, s=np.sqrt(keep[WEIGHT]) / 25, alpha=0.55,
               color="#3b6ea5", edgecolor="white")
    b = np.polyfit(keep.d_cr4, keep.d_tfp_gap, 1)
    xs = np.linspace(keep.d_cr4.min(), keep.d_cr4.max(), 50)
    ax.plot(xs, np.polyval(b, xs), color="#b5523b", lw=1.5, label="fitted line")
    for code, name in [("3361", "Motor vehicles"), ("3379", "Mattresses and blinds"), ("3161", "Leather tanning"),
                       ("3365", "Railcars"), ("3313", "Aluminum"), ("3362", "RVs and truck bodies"),
                       ("3311", "Steel mills"), ("3122", "Tobacco")]:
        if code in keep.index:
            ax.annotate(name, (keep.d_cr4[code], keep.d_tfp_gap[code]), xytext=(4, 3),
                        textcoords="offset points", fontsize=8)
    ax.set_xlabel("Change in the 4 largest companies' share, 2002 to 2017 (points)")
    ax.set_ylabel("Change in TFP gap, 90th vs 10th plant (log points)")
    ax.set_title("Industries that consolidated did not let their laggards fall further behind")
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "consolidation_scatter.png", dpi=150)
    plt.close(fig)
    print("\nWrote consolidation tables and figure to results/")


if __name__ == "__main__":
    main()
