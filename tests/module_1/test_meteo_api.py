import pandas as pd
import pytest
import requests_mock
from src.module_1.module_1_meteo_api import (
    get_data_meteo_api,
    process_dataframe_columns,
)


mock_data = {
    "daily": {
        "time": ["1950-01-01", "1951-01-01", "1952-01-01", "1953-01-01"],
        "temperature_2m_mean_CMCC_CM2_VHR4": [13.6, 13.6, 13.4, 4.7],
        "precipitation_sum_CMCC_CM2_VHR4": [1.2, 1.3, 1.5, 2.0],
        "soil_moisture_0_to_10cm_mean_CMCC_CM2_VHR4": [0.25, 0.25, 0.24, 0.34],
        "temperature_2m_mean_FGOALS_f3_H": [13.6, 13.6, 13.4, 4.7],
        "precipitation_sum_FGOALS_f3_H": [1.2, 1.3, 1.5, 2.0],
        "soil_moisture_0_to_10cm_mean_FGOALS_f3_H": [0.25, 0.25, 0.24, 0.34],
    },
}
API_URL = "https://climate-api.open-meteo.com/v1/climate?"


def test_get_data_meteo_api():
    with requests_mock.Mocker() as mock:
        mock.get(API_URL, json=mock_data)
        data = get_data_meteo_api("Madrid")

        assert isinstance(data, pd.DataFrame)

        assert not data.empty


def test_process_dataframe():
    with requests_mock.Mocker() as mock:
        mock.get(API_URL, json=mock_data)
        data = get_data_meteo_api("Madrid")
        processed_data = process_dataframe_columns(data)

        assert isinstance(processed_data, pd.DataFrame)

        assert not processed_data.empty

        expected_columns = [
            "temperature_mean",
            "temperature_std",
            "precipitation_mean",
            "precipitation_std",
            "soil_moisture_mean",
            "soil_moisture_std",
        ]
        assert all(column in processed_data.columns for column in expected_columns)

