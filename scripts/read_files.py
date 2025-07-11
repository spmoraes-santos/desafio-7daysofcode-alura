#### Created by S.P. Moraes-Santos

import pandas as pd
import glob
import os

def load_csvs(path_pattern):
    """
    Load one or multiple CSV files matching a glob pattern.

    Parameters:
        path_pattern (str): Glob pattern, e.g., 'data/*.csv'

    Returns:
        pd.DataFrame: Concatenated DataFrame with all CSV data,
                      or an empty DataFrame if no files found.
    """
    files = glob.glob(path_pattern)
    if not files:
        return pd.DataFrame()
    elif len(files) == 1:
        return pd.read_csv(files[0])
    else:
        return pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

def load_excels(path_pattern, sheet_name=0, skiprows=None, usecols=None, engine=None, verbose=True):
    """
    Load one or multiple Excel files matching a glob pattern into a single DataFrame.

    Parameters:
        path_pattern (str): Glob pattern, e.g., 'data/*.xlsx'
        sheet_name (str|int|list|None): Sheet to read (default is 0). Use None to read all sheets.
        skiprows (int|list, optional): Rows to skip at the beginning.
        usecols (str|list, optional): Columns to read.
        engine (str, optional): Engine to use ('openpyxl', 'xlrd', etc.)
        verbose (bool): If True, prints which files are being loaded.

    Returns:
        pd.DataFrame: Concatenated DataFrame with all Excel data,
                      or an empty DataFrame if no files found or all fail to load.
    """
    files = glob.glob(path_pattern)

    if not files:
        if verbose:
            print(f"Not found any file: {path_pattern}")
        return pd.DataFrame()

    dataframes = []
    for file in files:
        try:
            if verbose:
                print(f"Lendo: {os.path.basename(file)}")
            df = pd.read_excel(file, sheet_name=sheet_name, skiprows=skiprows,
                               usecols=usecols, engine=engine)
            dataframes.append(df)
        except Exception as e:
            print(f"Reading error {file}: {e}")

    if not dataframes:
        return pd.DataFrame()

    return pd.concat(dataframes, ignore_index=True)


def load_parquets(path_pattern):
    """
    Load one or multiple Parquet files from local path (with glob) or directly from URL.

    Parameters:
        path_pattern (str): Glob pattern or URL

    Returns:
        pd.DataFrame: Concatenated DataFrame with all Parquet data,
                      or an empty DataFrame if no files found.
    """
    if path_pattern.startswith("http"):
        # Se for URL, lê direto
        return pd.read_parquet(path_pattern)

    # Caso contrário, trata como caminho local
    files = glob.glob(path_pattern)
    if not files:
        return pd.DataFrame()
    elif len(files) == 1:
        return pd.read_parquet(files[0])
    else:
        return pd.concat([pd.read_parquet(file) for file in files], ignore_index=True)

def load_jsons(path_pattern, lines=False):
    """
    Load one or multiple JSON files matching a glob pattern.

    Parameters:
        path_pattern (str): Glob pattern, e.g., 'data/*.json'
        lines (bool): True if files are in JSON Lines format.

    Returns:
        pd.DataFrame: Concatenated DataFrame with all JSON data,
                      or an empty DataFrame if no files found.
    """
    files = glob.glob(path_pattern)
    if not files:
        return pd.DataFrame()
    elif len(files) == 1:
        return pd.read_json(files[0], lines=lines)
    else:
        return pd.concat([pd.read_json(file, lines=lines) for file in files], ignore_index=True)

def load_files_auto(path_pattern, json_lines=False):
    """
    Automatically load multiple files of different formats (CSV, Excel, Parquet, JSON)
    by detecting the file extension.

    Parameters:
        path_pattern (str): Glob pattern for file paths.
        json_lines (bool): True if JSON files are JSON Lines.

    Returns:
        pd.DataFrame: Concatenated DataFrame with all loaded data,
                      or an empty DataFrame if no files found.
    """
    files = glob.glob(path_pattern)
    if not files:
        return pd.DataFrame()

    dfs = []

    for file in files:
        ext = os.path.splitext(file)[1].lower()

        if ext == '.csv':
            df = pd.read_csv(file)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file)
        elif ext == '.parquet':
            df = pd.read_parquet(file)
        elif ext == '.json':
            df = pd.read_json(file, lines=json_lines)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        dfs.append(df)

    if len(dfs) == 1:
        return dfs[0]
    else:
        return pd.concat(dfs, ignore_index=True)

def load_url_file(url, file_type=None, **kwargs):
    """
    Load a file directly from a URL based on the specified or inferred file type.

    Parameters:
        url (str): URL to the file.
        file_type (str, optional): Type of file to load ('csv', 'excel', 'json', 'parquet', 'table').
                                   If not provided, will infer from the URL extension.
        **kwargs: Additional keyword arguments passed to the pandas read function.

    Returns:
        pd.DataFrame: Loaded DataFrame, or empty DataFrame if reading fails.
    """

    # Infer type from extension if not given
    if not file_type:
        ext = os.path.splitext(url)[-1].lower()
        if ext == '.csv':
            file_type = 'csv'
        elif ext in ['.xls', '.xlsx']:
            file_type = 'excel'
        elif ext == '.json':
            file_type = 'json'
        elif ext == '.parquet':
            file_type = 'parquet'
        else:
            file_type = 'table'  # default fallback

    try:
        if file_type == 'csv':
            return pd.read_csv(url, **kwargs)
        elif file_type == 'excel':
            return pd.read_excel(url, **kwargs)
        elif file_type == 'json':
            return pd.read_json(url, **kwargs)
        elif file_type == 'parquet':
            return pd.read_parquet(url, **kwargs)
        elif file_type == 'table':
            return pd.read_table(url, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        print(f"Erro ao ler o arquivo da URL: {url}")
        print(f"Tipo: {file_type} | Detalhes do erro: {e}")
        return pd.DataFrame()
