## Defines function to thin training dataset 
# method: repeatedly pick a random remaining region, drop every other remaining region within `threshold_km` of it, and repeat until every region is kept or dropped

from dataclasses import dataclass
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd

@dataclass
class ThinConfig:
    name: str                          
    raw_dataset: str                   
    threshold_km: float = 50           # empirically chosen from correlogram analysis
    min_regions: int = 50              # countries with fewer regions than this are left untouched
    random_seed: int = 42              


# function to calculate haversine distance between one point and an array of points
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))

# function to thin regions within a single country
def thin_country(sub_df, threshold_km, rng):
    remaining = sub_df.copy()
    kept_rows = []

    while len(remaining) > 0:
        pick_idx = rng.choice(remaining.index.to_numpy())
        picked_row = remaining.loc[pick_idx]
        kept_rows.append(picked_row)

        dists = haversine_km(
            picked_row["lat"], picked_row["lon"],
            remaining["lat"].values, remaining["lon"].values
        )
        remaining = remaining.loc[dists >= threshold_km]

    return pd.DataFrame(kept_rows)

# function to thin the entire dataset, iterating over countries 
def thin_dataset(df, threshold_km, min_regions, rng):
    thinned_parts = []
    summary_rows = []

    for country, sub in df.groupby("country_ID"):
        n_before = len(sub)

        if n_before < min_regions:
            thinned_parts.append(sub)
            summary_rows.append({
                "country_ID": country, "n_before": n_before,
                "n_after": n_before, "n_dropped": 0, "thinned": False,
            })
            continue

        thinned_sub = thin_country(sub, threshold_km, rng)
        n_after = len(thinned_sub)

        thinned_parts.append(thinned_sub)
        summary_rows.append({
            "country_ID": country, "n_before": n_before,
            "n_after": n_after, "n_dropped": n_before - n_after, "thinned": True,
        })

    thinned_df = pd.concat(thinned_parts, ignore_index=True)
    summary_df = pd.DataFrame(summary_rows).sort_values("n_dropped", ascending=False)
    return thinned_df, summary_df


# function to prep dataset for thinning — assumes lat/lon are already present in raw_dataset,
# returns the thinned DataFrame in memory 
def prepare_thinned_dataset(
    config: ThinConfig,
    data_dir: Union[str, Path],
    verbose: bool = True,
) -> pd.DataFrame:

    data_dir = Path(data_dir)

    if verbose:
        print(f"\n── {config.name} ──────────────────────────────")

    df = pd.read_csv(data_dir / config.raw_dataset)
    n_before_total = len(df)

    missing_coords = df["lat"].isna().sum()
    if missing_coords > 0:
        if verbose:
            print(f"  warning: {missing_coords} rows missing lat/lon, dropping before thinning")
        df = df.dropna(subset=["lat", "lon"])

    rng = np.random.default_rng(config.random_seed)
    thinned_df, summary_df = thin_dataset(df, config.threshold_km, config.min_regions, rng)

    if verbose:
        print(summary_df.to_string(index=False))
        print(f"  total: {n_before_total:,} -> {len(thinned_df):,} rows "
              f"({n_before_total - len(thinned_df):,} dropped)")

    return thinned_df