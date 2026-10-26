# Gridded Agricultural Capital and Labor

Code accompanying:

> Manitius, C., Zia, A., & Ricketts, T. *The social and economic footprint of agriculture: fine-scale data for assessing the cost of transformation.* [Preprint]

This repository produces global, gridded (5 arc-min, ~10 km at the equator) estimates of agricultural capital stock and labor for 2020. It uses a random forest model trained on sub-national statistics to predict how capital and labor intensities (value of capital or number of workers per tonne of production) vary within countries. The predictions are combined with gridded production data and calibrated to known sub-national and national totals. The repository also contains the 30x30 exposure analysis and the code to reproduce all results and figures in the paper.

## Data availability

| Item | Location |
|---|---|
| Gridded capital and labor datasets (final, calibrated) | [DOI] |
| Compiled predictor dataset and sub-national training data | [DOI] |

The `Data/`, `Results/` and `Figures/` folders are excluded from the repository. Download the datasets above and place the training and predictor files in a `Data/` folder. Outputs are written to `Results/` and `Figures/`.

## Workflow

Run the notebooks in this order. 

1. **`01_RF_model/01.1_train_RF.ipynb`**: trains two versions of the model: one with five folds used for spatial cross-validation and a second trained on the full dataset for downscaling
2. **`01_RF_model/01.2_evaluate_RF.ipynb`**: computes performance metrics against the country-average null model
3. **`02_downscaling_model/02.1_ML_downscaling_model.ipynb`**: predicts intensities at the grid-scale, multiplies by production, and rescales to sub-national and national totals (for central, 10th and 90th percentile estimates)
4. **`02_downscaling_model/02.2_country_avg_model.ipynb`**: builds the country-average comparison model
5. **`02_downscaling_model/02.3_calculate_final_intensities.ipynb`**: recalculates intensities from the calibrated capital and labor rasters
6. **`02_downscaling_model/02.4_AOA.ipynb`**: calculates the dissimilarity index and area of applicability
7. **`03_30x30_analysis/03.1` to `03.4b`**: defines the 30x30 scenario and calculates exposure globally, by country, and across deprivation percentiles
8. **`03_generate_figures/`**: reproduces figures and tables in the paper

## Inputs

Inputs are not stored in this repository. Besides the compiled datasets above, the notebooks expect the following public datasets in `Data/`:

- **30x30 scenario:** Jung et al. (2021) (https://doi.org/10.1038/s41559-021-01528-7)
- **Country boundaries:** GADM 4.1 (https://gadm.org/data.html); simplified boundaries from geoBoundaries (https://www.geoboundaries.org/simplifiedDownloads.html) for mapping
- **Relative deprivation:** Global Gridded Relative Deprivation Index (CIESIN, 2025) (https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-pmp-grdi-2010-2020-1.00)
- **Population:** Bondarenko et al. (2025) (https://hub.worldpop.org/geodata/listing?id=138)

Sub-national boundary shapefiles used for some SI figures are available on request from the corresponding author.

## Requirements

The code is written in Python. Version 3.9.6 is recommended. Main packages:

`numpy`, `pandas`, `scipy`, `scikit-learn`, `quantile-forest`, `geopandas`, `rasterio`, `xarray`, `rioxarray`, `matplotlib`, `pyarrow`, `jupyter`

## Citation
If you use this code or the datasets, please cite the paper above.

## License
See [LICENSE](LICENSE).

## Contact

Carina Manitius, University of Vermont: carina.manitius@uvm.edu
