from io import BytesIO

import pandas as pd


def read_csv_safely(file_or_bytes):
    if isinstance(file_or_bytes, bytes):
        raw = file_or_bytes
    elif hasattr(file_or_bytes, "getvalue"):
        raw = file_or_bytes.getvalue()
    else:
        raw = file_or_bytes

    last_error = None
    for encoding in ("utf-8", "utf-8-sig", "latin1"):
        try:
            if isinstance(raw, bytes):
                df = pd.read_csv(BytesIO(raw), encoding=encoding)
            else:
                df = pd.read_csv(raw, encoding=encoding)
            return validate_dataframe(df)
        except Exception as exc:
            last_error = exc

    raise ValueError(f"Could not read CSV file: {last_error}")


def validate_dataframe(df):
    if df.empty and len(df.columns) == 0:
        raise ValueError("CSV file is empty or has no columns.")
    if len(df.columns) == 0:
        raise ValueError("CSV file has no columns.")
    return df
