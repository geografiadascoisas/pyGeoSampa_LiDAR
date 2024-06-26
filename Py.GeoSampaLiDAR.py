import geopandas as gpd
import requests
import os
import zipfile
from io import BytesIO
import sys
import tempfile

# ------------------------------------------------------------------------------
# PyGeoSampa_LiDar
# Version: 1.0.0
# Author: Abimael Cereda Junior - https://about.me/ceredajunior
# Geografia das Coisas - https://geografiadascoisas.com.br
# License: Apache License 2.0
# ------------------------------------------------------------------------------

def main():
    try:
        # Check for command line arguments
        if len(sys.argv) != 2:
            print("Usage: python PyGeoSampa_LiDar.py <aoi_path>")
            sys.exit(1)

        # Path to your area of interest shapefile
        aoi_path = sys.argv[1]
        grid_zip_path = "SIRGAS_SHP_quadriculamdt.zip"

        # Temporary directory for extracting grid shapefiles
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(grid_zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the grid shapefile within the temporary directory
            grid_path = None
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(".shp") and "SIRGAS_SHP_quadriculamdt" in file:
                        grid_path = os.path.join(root, file)
                        break

            if grid_path is None:
                print("Error: SIRGAS_SHP_quadriculamdt.shp not found in the zip file.")
                sys.exit(1)

            print(f"Grid shapefile found at: {grid_path}")

            # Load both shapefiles
            try:
                aoi_gdf = gpd.read_file(aoi_path)
                print(f"AOI shapefile loaded successfully with CRS: {aoi_gdf.crs}")
            except Exception as e:
                print(f"Error loading AOI shapefile: {e}")
                sys.exit(1)

            # Check if AOI is a polygon
            if not all(aoi_gdf.geometry.type == 'Polygon'):
                print("Error: The AOI shapefile must contain polygons. Please provide a valid AOI shapefile.")
                sys.exit(1)

            try:
                grid_gdf = gpd.read_file(grid_path)
                print(f"Grid shapefile loaded successfully with CRS: {grid_gdf.crs}")
                # Define the CRS explicitly if not set
                if grid_gdf.crs is None:
                    grid_gdf.set_crs("EPSG:31983", inplace=True)
                    print(f"Grid shapefile CRS set to: {grid_gdf.crs}")
            except Exception as e:
                print(f"Error loading grid shapefile: {e}")
                sys.exit(1)

            # Check and set CRS
            target_crs = "EPSG:31983"
            if aoi_gdf.crs != target_crs:
                try:
                    aoi_gdf = aoi_gdf.to_crs(target_crs)
                    print(f"AOI shapefile converted to CRS: {aoi_gdf.crs}")
                except Exception as e:
                    print(f"Error converting AOI shapefile to CRS {target_crs}: {e}")
                    sys.exit(1)

            if grid_gdf.crs != target_crs:
                try:
                    grid_gdf = grid_gdf.to_crs(target_crs)
                    print(f"Grid shapefile converted to CRS: {grid_gdf.crs}")
                except Exception as e:
                    print(f"Error converting grid shapefile to CRS {target_crs}: {e}")
                    sys.exit(1)

            # Check if AOI is within the grid boundaries
            aoi_within_grid = grid_gdf.unary_union.contains(aoi_gdf.unary_union)
            if not aoi_within_grid:
                print("Warning: The area of interest is outside the boundaries of the São Paulo municipality.")
                sys.exit(1)

            # Find intersecting cells
            intersecting_cells = gpd.overlay(grid_gdf, aoi_gdf, how='intersection')
            print(f"Found {len(intersecting_cells)} intersecting cells.")

            # Prompt user for the data type
            print("Select data type:")
            print("1. DSM")
            print("2. DTM")
            data_type_choice = input("Enter the number corresponding to your choice: ")
            if data_type_choice == "1":
                data_type = "MDS"
            elif data_type_choice == "2":
                data_type = "MDT"
            else:
                print("Invalid choice. Please choose either 1 (DSM) or 2 (DTM).")
                sys.exit(1)

            # Prompt user for the data year
            print(f"Select data year for {data_type}:")
            print("1. 2017")
            print("2. 2020")
            data_year_choice = input("Enter the number corresponding to your choice: ")
            if data_year_choice == "1":
                data_year = f"{data_type}_2017"
            elif data_year_choice == "2":
                data_year = f"{data_type}_2020"
            else:
                print(f"Invalid choice. Please choose either 1 ({data_type}_2017) or 2 ({data_type}_2020).")
                sys.exit(1)

            # Base URL for the data
            base_url = "https://geosampa.prefeitura.sp.gov.br/PaginasPublicas/downloadArquivo.aspx?orig=DownloadMapaArticulacao"

            # Construct download URLs
            urls = [
                f"{base_url}&arq={data_year}%5C{cell['qmdt_cod']}.zip&arqTipo=MAPA_ARTICULACAO"
                for idx, cell in intersecting_cells.iterrows()
            ]

            # Create directory for downloaded files
            download_dir = f"downloaded_{data_year}_files"
            os.makedirs(download_dir, exist_ok=True)

            # Inform the user that the download process can take some time
            print("Starting download of data files. Please wait, this may take a while...")

            # Download and extract each file
            for url in urls:
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    z = zipfile.ZipFile(BytesIO(response.content))
                    z.extractall(path=download_dir)
                    print(f"Extracted {url}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to download {url}: {e}")
                except zipfile.BadZipFile:
                    print(f"Failed to extract {url}: Bad zip file")

        print("Download and extraction completed!")
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
