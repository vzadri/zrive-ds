import requests
import pandas as pd
import jsonschema
import matplotlib.pyplot as plt

API_URL = "https://climate-api.open-meteo.com/v1/climate?"
VARIABLES = "temperature_2m_mean,precipitation_sum,soil_moisture_0_to_10cm_mean"
COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},
}
MODELS = (
    "CMCC_CM2_VHR4",
    "FGOALS_f3_H",
    "HiRAM_SIT_HR",
    "MRI_AGCM3_2_S",
    "EC_Earth3P_HR",
    "MPI_ESM1_2_XR",
    "NICAM16_8S",
)


def validate_json_schema(response):
    schema = {
        "$schema": "http://json-schema.org/schema#",
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"},
            "generationtime_ms": {"type": "number"},
            "utc_offset_seconds": {"type": "integer"},
            "timezone": {"type": "string"},
            "timezone_abbreviation": {"type": "string"},
            "elevation": {"type": "number"},
            "daily_units": {
                "type": "object",
                "properties": {
                    "time": {"type": "string"},
                    "temperature_2m_mean_CMCC_CM2_VHR4": {"type": "string"},
                    "precipitation_sum_CMCC_CM2_VHR4": {"type": "string"},
                    "soil_moisture_0_to_10cm_mean_CMCC_CM2_VHR4": {"type": "string"},
                    "temperature_2m_mean_FGOALS_f3_H": {"type": "string"},
                    "precipitation_sum_FGOALS_f3_H": {"type": "string"},
                    "soil_moisture_0_to_10cm_mean_FGOALS_f3_H": {"type": "string"},
                    "temperature_2m_mean_HiRAM_SIT_HR": {"type": "string"},
                    "precipitation_sum_HiRAM_SIT_HR": {"type": "string"},
                    "soil_moisture_0_to_10cm_mean_HiRAM_SIT_HR": {"type": "string"},
                    "temperature_2m_mean_MRI_AGCM3_2_S": {"type": "string"},
                    "precipitation_sum_MRI_AGCM3_2_S": {"type": "string"},
                    "soil_moisture_0_to_10cm_mean_MRI_AGCM3_2_S": {"type": "string"},
                    "temperature_2m_mean_EC_Earth3P_HR": {"type": "string"},
                    "precipitation_sum_EC_Earth3P_HR": {"type": "string"},
                    "soil_moisture_0_to_10cm_mean_EC_Earth3P_HR": {"type": "string"},
                    "temperature_2m_mean_MPI_ESM1_2_XR": {"type": "string"},
                    "precipitation_sum_MPI_ESM1_2_XR": {"type": "string"},
                    "soil_moisture_0_to_10cm_mean_MPI_ESM1_2_XR": {"type": "string"},
                    "temperature_2m_mean_NICAM16_8S": {"type": "string"},
                    "precipitation_sum_NICAM16_8S": {"type": "string"},
                    "soil_moisture_0_to_10cm_mean_NICAM16_8S": {"type": "string"},
                },
                "required": [
                    "precipitation_sum_CMCC_CM2_VHR4",
                    "precipitation_sum_EC_Earth3P_HR",
                    "precipitation_sum_FGOALS_f3_H",
                    "precipitation_sum_HiRAM_SIT_HR",
                    "precipitation_sum_MPI_ESM1_2_XR",
                    "precipitation_sum_MRI_AGCM3_2_S",
                    "precipitation_sum_NICAM16_8S",
                    "soil_moisture_0_to_10cm_mean_CMCC_CM2_VHR4",
                    "soil_moisture_0_to_10cm_mean_EC_Earth3P_HR",
                    "soil_moisture_0_to_10cm_mean_FGOALS_f3_H",
                    "soil_moisture_0_to_10cm_mean_HiRAM_SIT_HR",
                    "soil_moisture_0_to_10cm_mean_MPI_ESM1_2_XR",
                    "soil_moisture_0_to_10cm_mean_MRI_AGCM3_2_S",
                    "soil_moisture_0_to_10cm_mean_NICAM16_8S",
                    "temperature_2m_mean_CMCC_CM2_VHR4",
                    "temperature_2m_mean_EC_Earth3P_HR",
                    "temperature_2m_mean_FGOALS_f3_H",
                    "temperature_2m_mean_HiRAM_SIT_HR",
                    "temperature_2m_mean_MPI_ESM1_2_XR",
                    "temperature_2m_mean_MRI_AGCM3_2_S",
                    "temperature_2m_mean_NICAM16_8S",
                    "time",
                ],
            },
            "daily": {
                "type": "object",
                "properties": {
                    "time": {"type": "array", "items": {"type": "string"}},
                    "temperature_2m_mean_CMCC_CM2_VHR4": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "precipitation_sum_CMCC_CM2_VHR4": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "soil_moisture_0_to_10cm_mean_CMCC_CM2_VHR4": {
                        "type": "array",
                        "items": {"type": "null"},
                    },
                    "temperature_2m_mean_FGOALS_f3_H": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "precipitation_sum_FGOALS_f3_H": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "soil_moisture_0_to_10cm_mean_FGOALS_f3_H": {
                        "type": "array",
                        "items": {"type": "null"},
                    },
                    "temperature_2m_mean_HiRAM_SIT_HR": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "precipitation_sum_HiRAM_SIT_HR": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "soil_moisture_0_to_10cm_mean_HiRAM_SIT_HR": {
                        "type": "array",
                        "items": {"type": "null"},
                    },
                    "temperature_2m_mean_MRI_AGCM3_2_S": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "precipitation_sum_MRI_AGCM3_2_S": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "soil_moisture_0_to_10cm_mean_MRI_AGCM3_2_S": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "temperature_2m_mean_EC_Earth3P_HR": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "precipitation_sum_EC_Earth3P_HR": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "soil_moisture_0_to_10cm_mean_EC_Earth3P_HR": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "temperature_2m_mean_MPI_ESM1_2_XR": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "precipitation_sum_MPI_ESM1_2_XR": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "soil_moisture_0_to_10cm_mean_MPI_ESM1_2_XR": {
                        "type": "array",
                        "items": {"type": "null"},
                    },
                    "temperature_2m_mean_NICAM16_8S": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "precipitation_sum_NICAM16_8S": {
                        "type": "array",
                        "items": {"type": "number"},
                    },
                    "soil_moisture_0_to_10cm_mean_NICAM16_8S": {
                        "type": "array",
                        "items": {"type": "null"},
                    },
                },
                "required": [
                    "precipitation_sum_CMCC_CM2_VHR4",
                    "precipitation_sum_EC_Earth3P_HR",
                    "precipitation_sum_FGOALS_f3_H",
                    "precipitation_sum_HiRAM_SIT_HR",
                    "precipitation_sum_MPI_ESM1_2_XR",
                    "precipitation_sum_MRI_AGCM3_2_S",
                    "precipitation_sum_NICAM16_8S",
                    "soil_moisture_0_to_10cm_mean_CMCC_CM2_VHR4",
                    "soil_moisture_0_to_10cm_mean_EC_Earth3P_HR",
                    "soil_moisture_0_to_10cm_mean_FGOALS_f3_H",
                    "soil_moisture_0_to_10cm_mean_HiRAM_SIT_HR",
                    "soil_moisture_0_to_10cm_mean_MPI_ESM1_2_XR",
                    "soil_moisture_0_to_10cm_mean_MRI_AGCM3_2_S",
                    "soil_moisture_0_to_10cm_mean_NICAM16_8S",
                    "temperature_2m_mean_CMCC_CM2_VHR4",
                    "temperature_2m_mean_EC_Earth3P_HR",
                    "temperature_2m_mean_FGOALS_f3_H",
                    "temperature_2m_mean_HiRAM_SIT_HR",
                    "temperature_2m_mean_MPI_ESM1_2_XR",
                    "temperature_2m_mean_MRI_AGCM3_2_S",
                    "temperature_2m_mean_NICAM16_8S",
                    "time",
                ],
            },
        },
        "required": [
            "daily",
            "daily_units",
            "elevation",
            "generationtime_ms",
            "latitude",
            "longitude",
            "timezone",
            "timezone_abbreviation",
            "utc_offset_seconds",
        ],
    }
    try:
        jsonschema.validate(response, schema)
    except jsonschema.exceptions.ValidationError as error:
        print("Data does not match schema: ", error)
        return False
    return True


def call_api(
    url,
    params,
):
    response = requests.get(url, params=params)
    if not response.status_code == 200:
        error = response.json()
        print("error=", error)
    else:
        response = response.json()
        # if validate_json_schema(response):
        print("json schema correcto")
        return response["daily"]


def get_data_meteo_api(city):
    if city in COORDINATES:
        params = {
            "latitude": COORDINATES[city]["latitude"],
            "longitude": COORDINATES[city]["longitude"],
            "start_date": "1950-01-01",
            # "end_date": "2050-12-31",
            "end_date": "1996-12-31",
            "models": MODELS,
            "daily": VARIABLES,
        }
        data = call_api(API_URL, params)
        data = pd.DataFrame(data)
        return data


def process_dataframe_columns(df):
    df["time"] = pd.to_datetime(df["time"]).dt.year

    df_grouped = df.groupby("time")

    temp_cols = [
        col
        for col in df.columns
        if "temperature_2m_mean" in col and not df[col].isna().all()
    ]
    prec_cols = [
        col
        for col in df.columns
        if "precipitation_sum" in col and not df[col].isna().all()
    ]
    soil_cols = [
        col
        for col in df.columns
        if "soil_moisture_0_to_10cm_mean" in col and not df[col].isna().all()
    ]

    df_new = pd.DataFrame()
    df_new["temperature_mean"] = df_grouped[temp_cols].mean().mean(axis=1)
    df_new["temperature_std"] = df_grouped[temp_cols].std().mean(axis=1)
    df_new["precipitation_mean"] = df_grouped[prec_cols].mean().mean(axis=1)
    df_new["precipitation_std"] = df_grouped[prec_cols].std().mean(axis=1)
    df_new["soil_moisture_mean"] = df_grouped[soil_cols].mean().mean(axis=1)
    df_new["soil_moisture_std"] = df_grouped[soil_cols].std().mean(axis=1)

    return df_new


def plot_meteo_data(dict_city_df):
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    for city, df in dict_city_df.items():
        for i, variable in enumerate(["temperature", "precipitation", "soil_moisture"]):
            mean = df[f"{variable}_mean"]
            std = df[f"{variable}_std"]
            axs[i].plot(df.index, mean, label=f"{city} {variable}")
            axs[i].fill_between(df.index, mean - std, mean + std, alpha=0.2)
            axs[i].set_ylabel(variable)
            axs[i].legend()

    plt.tight_layout()
    plt.show()


def main():
    dict_city_df = {}
    for city in COORDINATES:
        dataAPI = get_data_meteo_api(city)
        dict_city_df[city] = process_dataframe_columns(dataAPI)

    plot_meteo_data(dict_city_df)


if __name__ == "__main__":
    main()
