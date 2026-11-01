"""Hicks (1935) on modern data: do concentrated US manufacturing industries live a quiet life?

Hicks argued that a monopolist's profit barely changes near its maximum, so a firm
sheltered from competition can take part of its reward as a quiet life instead of the
last dollar of profit. If he was right, industries run by a few firms should tolerate
more inefficiency than competitive ones: a wider gap between their best and worst plants
(the test Syverson 2004 made standard) and slower productivity growth.

This script
  1. computes the "flat top" arithmetic behind Hicks's sentence (results/flat_top.csv),
  2. builds a panel of the 86 four-digit NAICS manufacturing industries with Census
     concentration ratios (2002-2022), Census/BLS within-industry productivity
     dispersion (DiSP) and BLS productivity indices (results/industry_panel.csv),
  3. runs the cross-industry test for 2017 and repeats it for 2002, 2007 and 2012,
  4. writes a table of named industries and one figure.

Run from the repository root (then run src/consolidation.py for the extension):
    python src/quiet_life.py              # uses the files in data/raw/
    python src/quiet_life.py --download   # re-fetches the raw files first
"""

import argparse
import io
import time
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
import requests
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"
USER_AGENT = "Brendyn Beasley research 83249437+brendynbeasley@users.noreply.github.com"

# Economic Census concentration tables, national, by NAICS (public flat files)
EC = "https://www2.census.gov/programs-surveys/economic-census/data/"
CENSUS_FILES = {
    2002: ("EC0231SR12.zip", EC + "2002/sector31/EC0231SR12.zip"),
    2007: ("EC0731SR12.zip", EC + "2007/sector31/EC0731SR12.zip"),
    2012: ("EC1231SR2.zip", EC + "2012/sector31/EC1231SR2.zip"),
    2017: ("EC1700SIZECONCEN.zip", EC + "2017/sector00/EC1700SIZECONCEN.zip"),
    2022: ("EC2200SIZECONCEN.zip", EC + "2022/sector00/EC2200SIZECONCEN.zip"),
}
BASIC_2022 = ("EC2231BASIC.zip", EC + "2022/sector31/EC2231BASIC.zip")
DISP_URL = "https://www2.census.gov/ces/disp/"
DISP_FILES = {"tfp": "total_factor_productivity.csv", "lp": "output_per_hour.csv"}
# BLS detailed-industry productivity indices, as republished on FRED (no key needed)
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
BLS_SERIES = {"tfp": "M000000000", "lp": "L000000000"}  # IPUEN{naics4}{suffix}

MAIN_YEAR = 2017
# Dispersion is averaged over the five years around each Census (DiSP ends in 2021,
# so 2022 is left out of the dispersion tests: its window would be the pandemic years)
DISP_WINDOWS = {2002: (2000, 2004), 2007: (2005, 2009), 2012: (2010, 2014), 2017: (2015, 2019)}
GROWTH_WINDOW = (2007, 2019)       # business-cycle peak to peak, before the pandemic
CR4_BINS = [0, 20, 40, 60, 100]    # concentration groups for the summary table
TOBACCO = "3122"                   # the one extreme outlier, dropped in a robustness row
FLAT_TOP_DEVIATIONS = [0.05, 0.10, 0.20, 0.30]
FLAT_TOP_EXAMPLE = "3311"          # iron and steel mills: concentrated, no excise taxes

# Census does not name firms. These are each industry's well-known leaders (my judgment).
LEADERS = {
    "3122": "Altria (Marlboro), Reynolds American (Camel, Newport)",
    "3364": "Boeing, Lockheed Martin, RTX, GE Aerospace",
    "3352": "Whirlpool, GE Appliances, Electrolux",
    "3361": "GM, Ford, Stellantis, Toyota, Tesla",
    "3311": "Nucor, Cleveland-Cliffs, Steel Dynamics, U.S. Steel",
    "3221": "International Paper, Domtar, Georgia-Pacific",
    "3121": "Coca-Cola, PepsiCo, Anheuser-Busch, Molson Coors",
    "3241": "Marathon, Valero, ExxonMobil, Phillips 66",
    "3254": "Pfizer, Merck, Eli Lilly, Johnson & Johnson",
    "3344": "Intel, Texas Instruments, Micron, GlobalFoundries",
    "3341": "Dell, HP, Hewlett Packard Enterprise",
    "3116": "Tyson, JBS, Cargill, National Beef",
    "3256": "Procter & Gamble, Colgate-Palmolive, Clorox",
    "3251": "Dow, LyondellBasell, ExxonMobil Chemical",
    "3327": "thousands of small machine shops",
    "3231": "RR Donnelley, Quad, thousands of local printers",
}


def get(url):
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=120)
    r.raise_for_status()
    return r.content


def download():
    """Fetch every raw file into data/raw/ (about 180 small requests, paced)."""
    for sub in ("census", "disp", "bls"):
        (RAW / sub).mkdir(parents=True, exist_ok=True)
    for name, url in list(CENSUS_FILES.values()) + [BASIC_2022]:
        (RAW / "census" / name).write_bytes(get(url))
        print(f"  downloaded {url}")
    for name in list(DISP_FILES.values()) + ["readme.txt"]:
        (RAW / "disp" / name).write_bytes(get(DISP_URL + name))
        print(f"  downloaded {DISP_URL + name}")
    codes = sorted(load_disp("tfp")[0].naics4.unique())
    frames = []
    for code in codes:
        for measure, suffix in BLS_SERIES.items():
            sid = f"IPUEN{code}{suffix}"
            s = pd.read_csv(io.BytesIO(get(FRED_URL + sid)))
            s.columns = ["date", "index"]
            s["year"] = s.date.str[:4].astype(int)
            s["naics4"], s["measure"], s["series"] = code, measure, sid
            frames.append(s[["naics4", "measure", "series", "year", "index"]])
            time.sleep(0.3)
    pd.concat(frames).to_csv(RAW / "bls" / "bls_productivity_fred.csv", index=False)
    print(f"  downloaded {len(frames)} BLS productivity series from FRED")


def read_census_zip(name):
    with zipfile.ZipFile(RAW / "census" / name) as z:
        member = [m for m in z.namelist() if m.endswith(".dat")][0]
        d = pd.read_csv(z.open(member), sep="|", dtype=str, encoding="latin-1")
    d.columns = [c.strip().lstrip("#") for c in d.columns]
    return d


def load_concentration():
    """CR4, CR8, HHI, firm count and shipments for four-digit manufacturing, 2002-2022."""
    rows = []
    for year, (name, _) in CENSUS_FILES.items():
        d = read_census_zip(name)
        code = f"NAICS{year}"
        title = code + ("_LABEL" if year == 2022 else "_TTL" if year >= 2012 else "_MEANING")
        if year >= 2017:   # new layout: one row per size class, TYPOP 00 = all establishments
            d = d[(d.GEOTYPE == "01") & (d.TYPOP == "00")]
            share, hhi, codes = "VAL_PCT", "HHI", {"all": "001", "cr4": "604", "cr8": "608", "hhi": "650"}
            firms = "FIRM"
        else:
            share, hhi, codes = "CCORCPPCT", "VSHERFI", {"all": "004", "cr4": "856", "cr8": "857", "hhi": "859"}
            firms = "COMPANY"
        d = d[d[code].str.fullmatch(r"3[1-3]\d\d")]
        by = {k: d[d.CONCENFI == v].set_index(code) for k, v in codes.items()}
        out = pd.DataFrame({
            "title": by["all"][title].str.strip(),
            "firms": pd.to_numeric(by["all"][firms]),
            "shipments_k": pd.to_numeric(by["all"]["RCPTOT"]),
            "cr4": pd.to_numeric(by["cr4"][share]),
            "cr8": pd.to_numeric(by["cr8"][share]),
            "hhi": pd.to_numeric(by["hhi"][hhi]).replace(0, np.nan),
        })
        if "ESTAB" in by["all"]:
            out["estabs"] = pd.to_numeric(by["all"]["ESTAB"])
            out["top4_shipments_k"] = pd.to_numeric(by["cr4"]["RCPTOT"])
        out["year"] = year
        rows.append(out.rename_axis("naics4").reset_index())
        print(f"Loaded {name}: {len(out)} four-digit manufacturing industries for {year}")
    return pd.concat(rows, ignore_index=True)


def load_basic_2022():
    d = read_census_zip(BASIC_2022[0])
    d = d[(d.GEOTYPE == "01") & d.NAICS2022.str.fullmatch(r"3[1-3]\d\d")].set_index("NAICS2022")
    cols = ["RCPTOT", "PAYANN", "BENEFIT", "CSTMTOT", "VALADD", "ESTAB"]
    out = d[cols].apply(pd.to_numeric)
    print(f"Loaded {BASIC_2022[0]}: {len(out)} four-digit manufacturing industries, national totals")
    return out


def load_disp(measure):
    """DiSP within-industry dispersion of log productivity, one row per industry-year."""
    d = pd.read_csv(RAW / "disp" / DISP_FILES[measure], dtype=str, encoding="latin-1")
    n0 = len(d)
    d = d[d.naics4.str.fullmatch(r"\d{4}", na=False)].copy()
    for c in d.columns[1:]:
        d[c] = pd.to_numeric(d[c], errors="coerce")   # 'S' = suppressed by Census
    d["year"] = d.year.astype(int)
    return d.rename(columns={"d9010*": "d9010w", "d7525*": "d7525w"}), n0 - len(d)


def load_bls():
    d = pd.read_csv(RAW / "bls" / "bls_productivity_fred.csv", dtype={"naics4": str})
    print(f"Loaded bls_productivity_fred.csv: {d.series.nunique()} series, {d.year.min()}-{d.year.max()}")
    return d.pivot_table(index=["naics4", "year"], columns="measure", values="index")


def growth(index, code, start, end):
    """Average annual log growth, percent."""
    try:
        return 100 * np.log(index.loc[(code, end)] / index.loc[(code, start)]) / (end - start)
    except KeyError:
        return np.nan


def flat_top(basic):
    """Hicks's flat top: with straight-line demand and constant marginal cost, producing a
    fraction d away from the profit-maximizing output costs d^2 of the maximum profit."""
    ex = basic.loc[FLAT_TOP_EXAMPLE]
    margin = ex.RCPTOT - ex.PAYANN - ex.BENEFIT - ex.CSTMTOT   # $1,000
    rows = [{"deviation_from_best_output_pct": 100 * dev,
             "share_of_max_profit_lost_pct": 100 * dev ** 2,
             "example_naics": FLAT_TOP_EXAMPLE,
             "example_shipments_bn": ex.RCPTOT / 1e6,
             "example_margin_bn": margin / 1e6,
             "example_margin_lost_mn": margin * dev ** 2 / 1e3} for dev in FLAT_TOP_DEVIATIONS]
    return pd.DataFrame(rows)


def worked_examples(conc, panel):
    """The numbers behind the README's worked examples for CR4 and the productivity spread."""
    c = conc[(conc.naics4 == FLAT_TOP_EXAMPLE) & (conc.year == 2022)].iloc[0]
    p = panel.loc[FLAT_TOP_EXAMPLE]
    return pd.DataFrame([
        {"item": "steel mills 2022, top-4 shipments ($bn)", "value": c.top4_shipments_k / 1e6},
        {"item": "steel mills 2022, industry shipments ($bn)", "value": c.shipments_k / 1e6},
        {"item": "steel mills 2022, CR4 computed (%)", "value": 100 * c.top4_shipments_k / c.shipments_k},
        {"item": "steel mills 2022, CR4 published (%)", "value": c.cr4},
        {"item": "steel mills 2015-19, log output-per-hour gap 90-10", "value": p.lp_d9010_2017},
        {"item": "steel mills 2015-19, output-per-hour spread 90/10", "value": np.exp(p.lp_d9010_2017)},
        {"item": "steel mills 2015-19, log TFP gap 90-10", "value": p.tfp_d9010_2017},
        {"item": "steel mills 2015-19, TFP spread 90/10", "value": np.exp(p.tfp_d9010_2017)},
    ])


def build_panel(conc, bls):
    wide = conc.pivot(index="naics4", columns="year", values=["cr4", "cr8", "hhi", "firms", "shipments_k"])
    wide.columns = [f"{a}_{b}" for a, b in wide.columns]
    panel = wide.join(conc[conc.year == MAIN_YEAR].set_index("naics4")[["title", "estabs"]])
    for measure in DISP_FILES:
        d, dropped = load_disp(measure)
        print(f"Loaded {DISP_FILES[measure]}: {d.naics4.nunique()} industries, {d.year.min()}-{d.year.max()}; "
              f"dropped {dropped} note rows; {int(d.d9010.isna().sum())} suppressed cells")
        for year, (a, b) in DISP_WINDOWS.items():
            w = d[d.year.between(a, b)].groupby("naics4")
            panel[f"{measure}_d9010_{year}"] = w.d9010.mean()
            panel[f"{measure}_d7525_{year}"] = w.d7525.mean()
            panel[f"{measure}_d9010w_{year}"] = w.d9010w.mean()
    for measure in BLS_SERIES:
        idx = bls[measure].dropna()
        for start, end in [GROWTH_WINDOW, (2002, 2019), (2002, 2023)]:
            panel[f"{measure}_growth_{start}_{end}"] = [growth(idx, c, start, end) for c in panel.index]
    panel["log_estabs"] = np.log(panel.estabs)
    panel["subsector"] = panel.index.str[:3]
    keep = panel.dropna(subset=[f"cr4_{MAIN_YEAR}", f"tfp_d9010_{MAIN_YEAR}", f"lp_d9010_{MAIN_YEAR}"])
    print(f"Panel: {len(panel)} industries; kept {len(keep)} with 2017 concentration and dispersion; "
          f"dropped {len(panel) - len(keep)}")
    return keep


def fit(formula, data, weights=None):
    data = data.dropna(subset=[t.strip() for t in formula.replace("~", "+").split("+") if "C(" not in t])
    if weights is not None:
        m = smf.wls(formula, data, weights=data[weights]).fit(cov_type="HC1")
    else:
        m = smf.ols(formula, data).fit(cov_type="HC1")
    return m, len(data)


def cross_section(panel):
    """Dispersion and growth on concentration, 2017, under several specifications."""
    y0 = MAIN_YEAR
    outcomes = {
        f"tfp_d9010_{y0}": "TFP gap, 90th vs 10th percentile plant (log points)",
        f"lp_d9010_{y0}": "Output-per-hour gap, 90th vs 10th percentile plant (log points)",
        f"tfp_growth_{GROWTH_WINDOW[0]}_{GROWTH_WINDOW[1]}": "TFP growth 2007-2019 (% a year)",
        f"lp_growth_{GROWTH_WINDOW[0]}_{GROWTH_WINDOW[1]}": "Labor productivity growth 2007-2019 (% a year)",
    }
    x = f"cr4_{y0}"
    no_tob = panel.drop(index=TOBACCO)
    panel = panel.assign(hhi_k=panel[f"hhi_{y0}"] / 1000, cr4_start=panel["cr4_2007"])
    specs = [
        ("CR4 alone", "{y} ~ {x}", panel, None, x),
        ("CR4 + log establishments", "{y} ~ {x} + log_estabs", panel, None, x),
        ("CR4 + log establishments + subsector effects", "{y} ~ {x} + log_estabs + C(subsector)", panel, None, x),
        ("CR4, weighted by shipments", "{y} ~ {x}", panel, f"shipments_k_{y0}", x),
        ("CR4, tobacco dropped", "{y} ~ {x}", no_tob, None, x),
        ("CR4 + log establishments, tobacco dropped", "{y} ~ {x} + log_estabs", no_tob, None, x),
        ("HHI (per 1,000) instead of CR4", "{y} ~ hhi_k", panel, None, "hhi_k"),
        ("CR4 in 2007 instead of 2017", "{y} ~ cr4_start", panel, None, "cr4_start"),
    ]
    rows = []
    for y, label in outcomes.items():
        for name, f, data, w, term in specs:
            m, n = fit(f.format(y=y, x=x), data, w)
            rows.append({"outcome": label, "spec": name, "coef_per_point": m.params[term],
                         "se": m.bse[term], "ci_low": m.conf_int().loc[term, 0],
                         "ci_high": m.conf_int().loc[term, 1], "p": m.pvalues[term], "n": n,
                         "gap_cr4_60_vs_20": 40 * m.params[term] if term != "hhi_k" else np.nan,
                         "log_estabs_coef": m.params.get("log_estabs", np.nan)})
    out = pd.DataFrame(rows)
    out["ratio_cr4_60_vs_20"] = np.where(out.outcome.str.contains("gap"), np.exp(out.gap_cr4_60_vs_20), np.nan)
    return out


def by_census_year(panel):
    rows = []
    for year in DISP_WINDOWS:
        for measure in DISP_FILES:
            y, x = f"{measure}_d9010_{year}", f"cr4_{year}"
            m, n = fit(f"{y} ~ {x}", panel)
            m2, _ = fit(f"{y} ~ {x}", panel.drop(index=TOBACCO))
            rows.append({"census_year": year, "dispersion_years": "%d-%d" % DISP_WINDOWS[year],
                         "measure": "TFP" if measure == "tfp" else "output per hour", "n": n,
                         "coef_per_point": m.params[x], "se": m.bse[x], "p": m.pvalues[x],
                         "coef_no_tobacco": m2.params[x], "p_no_tobacco": m2.pvalues[x],
                         "mean_gap_log": panel[y].mean()})
    return pd.DataFrame(rows)


def groups(panel):
    g = pd.cut(panel[f"cr4_{MAIN_YEAR}"], CR4_BINS, right=False,
               labels=["under 20%", "20-40%", "40-60%", "60% or more"])
    ty = f"tfp_growth_{GROWTH_WINDOW[0]}_{GROWTH_WINDOW[1]}"
    out = panel.groupby(g, observed=True).agg(
        industries=("title", "size"),
        median_estabs=("estabs", "median"),
        median_tfp_gap_log=(f"tfp_d9010_{MAIN_YEAR}", "median"),
        median_lp_gap_log=(f"lp_d9010_{MAIN_YEAR}", "median"),
        median_tfp_growth=(ty, "median"))
    out["tfp_ratio_90_10"] = np.exp(out.median_tfp_gap_log)
    out["lp_ratio_90_10"] = np.exp(out.median_lp_gap_log)
    return out.rename_axis("top4_share_2017").reset_index()


def named(panel):
    t = panel.loc[[c for c in LEADERS if c in panel.index]].copy()
    out = pd.DataFrame({
        "naics4": t.index, "industry": t.title, "leaders": [LEADERS[c] for c in t.index],
        "cr4_2017": t.cr4_2017, "establishments_2017": t.estabs,
        "lp_ratio_90_10": np.exp(t.lp_d9010_2017), "tfp_ratio_90_10": np.exp(t.tfp_d9010_2017),
        "tfp_growth_2007_2019": t.tfp_growth_2007_2019,
        "shipments_2017_bn": t.shipments_k_2017 / 1e6})
    return out.sort_values("cr4_2017", ascending=False)


def figure(panel):
    """Two panels: output-per-hour spread and TFP spread against concentration."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    x = panel.cr4_2017
    xs = np.linspace(x.min(), x.max(), 50)
    for ax, col, label in [(axes[0], "lp_d9010_2017", "Output per hour"),
                           (axes[1], "tfp_d9010_2017", "Total factor productivity")]:
        y = panel[col]
        ax.scatter(x, np.exp(y), s=np.sqrt(panel.shipments_k_2017) / 25, alpha=0.5,
                   color="#3b6ea5", edgecolor="white", lw=0.5)
        ax.plot(xs, np.exp(np.polyval(np.polyfit(x, y, 1), xs)), color="#b5523b", lw=1.5,
                label="fitted line, all 86 industries")
        ax.plot(xs, np.exp(np.polyval(np.polyfit(x.drop(TOBACCO), y.drop(TOBACCO), 1), xs)),
                color="#b5523b", lw=1.2, ls="--", label="without tobacco")
        for code, name in [("3122", "Tobacco"), ("3364", "Aerospace"), ("3361", "Motor vehicles"),
                           ("3341", "Computers"), ("3344", "Semiconductors"), ("3311", "Steel mills"),
                           ("3327", "Machine shops")]:
            ax.annotate(name, (x[code], np.exp(y[code])), xytext=(4, 3), textcoords="offset points", fontsize=8)
        ax.set_yscale("log")
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_yticks([1.5, 2, 3, 5, 10, 20, 50])
        ax.set_title(label, fontsize=11)
        ax.set_xlabel("Top-4 companies' share of shipments, 2017 (%)")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("90th-percentile plant ÷ 10th-percentile plant (log scale)")
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle("The spread between best and worst plants, 2015-2019 average", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT / "dispersion_vs_concentration.png", dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true", help="re-fetch the raw files first")
    args = ap.parse_args()
    if args.download or not (RAW / "bls" / "bls_productivity_fred.csv").exists():
        download()
    OUT.mkdir(exist_ok=True)

    conc = load_concentration()
    basic = load_basic_2022()
    bls = load_bls()
    panel = build_panel(conc, bls)

    ft = flat_top(basic)
    ft.to_csv(OUT / "flat_top.csv", index=False)
    we = worked_examples(conc, panel)
    we.to_csv(OUT / "worked_examples.csv", index=False)
    print("\nWorked examples:")
    print(we.round(3).to_string(index=False))
    print("\nFlat top (share of maximum profit lost by missing the best output):")
    print(ft.round(2).to_string(index=False))

    cs = cross_section(panel)
    cs.to_csv(OUT / "cross_section_tests.csv", index=False)
    print("\nCross-industry tests, 2017 concentration:")
    print(cs.round(4).to_string(index=False))

    yr = by_census_year(panel)
    yr.to_csv(OUT / "by_census_year.csv", index=False)
    print("\nDispersion on CR4, each Census year:")
    print(yr.round(4).to_string(index=False))

    gr = groups(panel)
    gr.to_csv(OUT / "concentration_groups.csv", index=False)
    print("\nBy concentration group, 2017:")
    print(gr.round(3).to_string(index=False))

    nm = named(panel)
    nm.to_csv(OUT / "named_industries.csv", index=False)
    print("\nNamed industries:")
    print(nm.drop(columns="leaders").round(2).to_string(index=False))

    tails = panel.assign(lp_ratio=np.exp(panel.lp_d9010_2017), tfp_ratio=np.exp(panel.tfp_d9010_2017))
    tails = tails.sort_values("lp_ratio")[["title", "cr4_2017", "estabs", "lp_ratio", "tfp_ratio"]]
    pd.concat([tails.head(3), tails.iloc[[len(tails) // 2]], tails.tail(3)]).to_csv(OUT / "dispersion_extremes.csv")
    print("\nLowest, median and highest output-per-hour spread:")
    print(pd.concat([tails.head(3), tails.iloc[[len(tails) // 2]], tails.tail(3)]).round(2).to_string())

    summary = pd.DataFrame([{"industries": len(panel), "establishments_2017": panel.estabs.sum(),
                             "shipments_2017_tn": panel.shipments_k_2017.sum() / 1e9,
                             "industries_cr4_40_plus": int((panel.cr4_2017 >= 40).sum()),
                             "median_tfp_growth_2007_2019": panel.tfp_growth_2007_2019.median(),
                             "slowest_tfp_growth_industry": panel.tfp_growth_2007_2019.idxmin()}])
    summary.to_csv(OUT / "sample_summary.csv", index=False)
    print("\nSample:")
    print(summary.round(3).to_string(index=False))
    panel.to_csv(OUT / "industry_panel.csv")
    figure(panel)
    print(f"\nWrote {len(list(OUT.glob('*.csv')))} CSV files and the figure to results/")


if __name__ == "__main__":
    main()
