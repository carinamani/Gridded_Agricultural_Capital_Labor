# Gridded Agricultural Capital and Labor

Code accompanying:

> Manitius, C., Zia, A., & Ricketts, T. *The social and economic footprint of agriculture: fine-scale data for assessing the cost of transformation.* [Preprint]

This repository produces global, gridded (5 arc-min, ~10 km at the equator) estimates of agricultural capital stock and agricultural labor for 2020. It uses a random forest model trained on sub-national statistics to predict how capital and labor intensities (value of capital or number of workers per tonne of production) vary within countries. The predictions are combined with gridded production data and calibrated to known sub-national and national totals. The repository also contains the 30x30 exposure analysis and the code for every figure and SI table in the paper.

## Data availability

| Item | Location |
|---|---|
| Gridded capital and labor datasets (final, calibrated) | [DOI] |
| Compiled predictor dataset and sub-national training data | [DOI] |

The `Data/`, `Results/` and `Figures/` folders are excluded from the repository (see `.gitignore`). Download the datasets above and place the training and predictor files in a `Data/` folder at the repository root. Outputs are written to `Results/` and `Figures/`, which are created as needed.

## Repository structure

```
.
├── helpers/                      # Shared functions imported by the notebooks
│   ├── step_a_config.py          # Run configuration (RunConfig) and hyperparameter search space
│   ├── step_b_spatial_CV.py      # Country-blocked spatial cross-validation folds
│   ├── step_c_train.py           # Model training, sample weighting, hyperparameter search
│   ├── step_d_feature_importance.py  # Impurity and permutation importance
│   ├── step_thin_sample.py       # Spatial thinning of the training data
│   └── reproject_raster.py       # Reprojection to the common 10 km Mollweide grid
├── 01_RF_model/
│   ├── 01.1_train_RF.ipynb       # Spatial CV (diagnostic) runs and final RF / QRF models
│   └── 01.2_evaluate_RF.ipynb    # Performance metrics (relative, absolute, country-average null model)
├── 02_downscaling_model/
│   ├── 02.1_ML_downscaling_model.ipynb            # Predict pixel intensities, convert to capital/labor, calibrate
│   ├── 02.2_country_avg_model.ipynb               # Country-average null model
│   ├── 02.3_calculate_final_intensities.ipynb     # Final intensity rasters from calibrated values
│   └── 02.4_AOA.ipynb                             # Area of applicability
├── 03_30x30_analysis/
│   ├── 03.1_prep_scenario.ipynb         # Reclassify the Jung et al. (2021) scenario
│   ├── 03.2_global_scale.ipynb          # Global exposure
│   ├── 03.3_country_exposure.ipynb      # Exposure by country
│   ├── 03.4a_prep_deprivation_index.ipynb  # Population-weighted deprivation percentiles
│   └── 03.4b_distribution_analysis.ipynb   # Exposure across deprivation percentiles
└── 03_generate_figures/              # One notebook per main figure / SI figure / SI table
```

## Workflow

Run the notebooks in this order. Each step reads outputs saved by the previous one.

1. **`01_RF_model/01.1_train_RF.ipynb`**: thins the training data, runs five-fold spatial cross-validation for the RF and quantile regression forest (QRF) models, then trains the final models on all data.
2. **`01_RF_model/01.2_evaluate_RF.ipynb`**: computes performance metrics against the country-average null model.
3. **`02_downscaling_model/02.1_ML_downscaling_model.ipynb`**: applies the final models to the gridded predictors, multiplies intensities by production, and rescales to sub-national and national totals (central, 10th and 90th percentile estimates).
4. **`02_downscaling_model/02.2_country_avg_model.ipynb`**: builds the country-average comparison model.
5. **`02_downscaling_model/02.3_calculate_final_intensities.ipynb`**: recalculates intensities from the calibrated capital and labor rasters.
6. **`02_downscaling_model/02.4_AOA.ipynb`**: calculates the dissimilarity index and area of applicability.
7. **`03_30x30_analysis/03.1` to `03.4b`**: reclassifies the 30x30 scenario and calculates exposure globally, by country, and across deprivation percentiles.
8. **`03_generate_figures/`**: reproduces the paper's figures and SI tables from the saved results.

## Inputs

Inputs are not stored in this repository. Besides the compiled datasets above, the notebooks expect the following public datasets in `Data/`:

- **30x30 scenario:** Jung et al. (2021), `minshort_speciestargets_biome.id_withPA_esh10km_repruns10_ranked.tif`
- **Country boundaries:** GADM 4.1 (https://gadm.org/data.html); simplified boundaries from geoBoundaries (https://www.geoboundaries.org/simplifiedDownloads.html) for mapping
- **Relative deprivation:** Global Gridded Relative Deprivation Index (CIESIN, 2025)
- **Population:** Bondarenko et al. (2025), gridded population by gender and age
- **Predictors, production and national statistics:** see Table 1 and the Methods of the paper, and the compiled predictor dataset above

Sub-national boundary shapefiles used for some SI figures are available on request from the corresponding author.

## Requirements

The code is written in Python. Version 3.9.6 is recommended. Main packages:

`numpy`, `pandas`, `scipy`, `scikit-learn`, `quantile-forest`, `geopandas`, `rasterio`, `xarray`, `rioxarray`, `matplotlib`, `pyarrow` (for parquet files), `jupyter`

## Citation
If you use this code or the datasets, please cite the paper above and the data DOIs.

## License
See [LICENSE](LICENSE).

## Contact

Carina Manitius, University of Vermont: [email]
