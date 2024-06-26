# pyGeoSampa_LiDAR
Python script to automatically download LiDAR data from GeoSampa, based on an area of interest (AOI) specified from a shape file (polygon).

[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/geografiadascoisas/pyGeoSampa_LiDAR/blob/main/README.pt-br.md)

## Requirements

- Python 3.x
- Python packages:
  - geopandas
  - requests

## Installation

You can install the script in two ways: by cloning the repository or by directly downloading the necessary files.

### Option 1: Clone the Repository

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/PyGeoSampa_LiDar.git
   cd PyGeoSampa_LiDar
   ```

2. Install the required packages:
   ```sh
   pip install geopandas requests
   ```

### Option 2: Download the Files

1. Download the necessary files:
   - `PyGeoSampa_LiDar.py`
   - `SIRGAS_SHP_quadriculamdt.zip`

2. Place the files in the same directory.

3. Install the required packages:
   ```sh
   pip install geopandas requests
   ```

## Usage

Run the script with the full path to the shapefile of the area of interest (AOI):

```sh
python PyGeoSampa_LiDar.py <path_to_shapefile>
```

### Example

```sh
python PyGeoSampa_LiDar.py .\limites.shp
```

## How It Works

1. The script loads the AOI shapefile and temporarily unzips the grid shapefile from GeoSampa (`SIRGAS_SHP_quadriculamdt.zip`).
2. Converts the shapefiles to the same coordinate reference system (CRS).
3. Checks if the AOI is a polygon. If it is not, the script issues an error and exits.
4. Checks if the AOI is within the grid boundaries. If it is outside, it issues a warning and exits the script.
5. Finds the grid cells that intersect the AOI.
6. Prompts the user to select the data type (DSM or DTM) and the data year (2017 or 2020) by typing numbers (1 or 2).
7. Constructs URLs to download the corresponding data files.
8. Informs the user that the download process may take a while, then downloads and extracts the data files to a specified directory.
9. If the user interrupts the process (Ctrl+C), the script displays a custom message "Process interrupted by user."

## Author

Abimael Cereda Junior - [https://about.me/ceredajunior](https://about.me/ceredajunior)
Geografia das Coisas - [https://geografiadascoisas.com.br](https://geografiadascoisas.com.br)

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.
