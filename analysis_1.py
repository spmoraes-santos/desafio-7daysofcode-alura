
#%% Libraries needed
from scripts.read_files import load_csvs,load_excels,load_parquets,load_url_file
from scripts.prepare_dfs import prepare_dataframe
import matplotlib.pyplot as plt  

#%% Paths 
#caminho_emprestimos = "Datasets\\Dia 1\\emprestimos-*.csv"
caminho_emprestimos = "Datasets/Dia 1/emprestimos-*.csv"
caminho_exemplares = "https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_1-Importando_dados/Datasets/dados_exemplares.parquet"

#%% Load data, clean and check from first analysis
emprestimos_biblioteca = load_csvs(caminho_emprestimos)
emprestimos_biblioteca = prepare_dataframe(emprestimos_biblioteca, 'data_emprestimo')

#%% Load more data and check
dados_exemplares = load_parquets(caminho_exemplares)
print(dados_exemplares.head())


#%% Merge datasets
empretimos_completos = emprestimos_biblioteca.merge(dados_exemplares)