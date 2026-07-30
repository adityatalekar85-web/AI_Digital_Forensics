import pandas as pd
import numpy as np


def load_data(file):

    df = pd.read_csv(file)

    return df


def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    removed = before - after

    return df, removed


def missing_values(df):

    return df.isnull().sum()


def fill_missing_values(df):

    for column in df.columns:

        if df[column].dtype == "object":

            df[column] = df[column].fillna("Unknown")

        else:

            df[column] = df[column].fillna(df[column].mean())

    return df


def dataset_information(df):

    info = {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Missing Values": int(df.isnull().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum())

    }

    return info