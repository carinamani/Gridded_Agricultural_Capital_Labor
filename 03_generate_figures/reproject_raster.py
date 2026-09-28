##### reproject_raster.py
# Reprojects any raster to match a fixed reference grid in memory 

import numpy as np
import rasterio
from rasterio.transform import Affine
from rasterio.crs import CRS
from rasterio.warp import reproject
from rasterio.enums import Resampling
import xarray as xr
import rioxarray  


# --- hardcoded reference grid specs, from conservation_scenario.tif ---
REF_TRANSFORM = Affine(10000.0, 0.0, -18039506.49,
                        0.0, -10000.0, 8871247.85)

REF_CRS = CRS.from_wkt(
    'PROJCS["unknown",GEOGCS["unknown",DATUM["D_Unknown_based_on_WGS84_ellipsoid",'
    'SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]]],'
    'PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],'
    'PROJECTION["Mollweide"],PARAMETER["central_meridian",0],'
    'PARAMETER["false_easting",0],PARAMETER["false_northing",0],'
    'UNIT["metre",1,AUTHORITY["EPSG","9001"]],'
    'AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
)

REF_WIDTH  = 3607
REF_HEIGHT = 1768
REF_NODATA = -9999.0  


def reproject_raster(in_path, resampling="sum"):
    resampling_map = {
        "sum":  Resampling.sum,
        "mean": Resampling.average,
    }
    if resampling not in resampling_map:
        raise ValueError(f"resampling must be one of {list(resampling_map)}, got {resampling!r}")

    dst_array = np.full((REF_HEIGHT, REF_WIDTH), np.nan, dtype=np.float32)

    with rasterio.open(in_path) as src_in:
        total_before = np.nansum(src_in.read(1))

        reproject(
            source=rasterio.band(src_in, 1),
            destination=dst_array,
            src_transform=src_in.transform,
            src_crs=src_in.crs,
            src_nodata=src_in.nodata,
            dst_transform=REF_TRANSFORM,
            dst_crs=REF_CRS,
            dst_nodata=np.nan,
            resampling=resampling_map[resampling],
        )

    total_after = np.nansum(dst_array)
    ratio = total_after / total_before if total_before else float("nan")

    return dst_array

def array_to_raster(array, transform=REF_TRANSFORM, crs=REF_CRS, nodata=np.nan):
    height, width = array.shape

    # pixel-center coordinates, derived from the affine transform
    xs = transform.c + transform.a * (np.arange(width) + 0.5)
    ys = transform.f + transform.e * (np.arange(height) + 0.5)

    da = xr.DataArray(
        array,
        dims=("y", "x"),
        coords={"y": ys, "x": xs},
        name="band_data",
    )
    da = da.rio.write_crs(crs, inplace=True)
    da = da.rio.write_transform(transform, inplace=True)
    da = da.rio.write_nodata(nodata, inplace=True)
    return da