### Created by S P Moraes-Santos

## Day 1- Load & Merge Data
#%% Libraries needed
from scripts.read_files import load_csvs,load_excels,load_parquets,load_url_file
from scripts.prepare_dfs import prepare_dataframe
from scripts.atribute_cdu import mappying_class_cdu
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

##### Day 2 - Cleanup and Attribute Context
#%% See the header
empretimos_completos.head(5) 

# %%  Drop registro_sistema
empretimos_completos.drop('registro_sistema', axis=1, inplace=True)
empretimos_completos.head(5)
# %% Transform matricula_ou_siape type into string
empretimos_completos["matricula_ou_siape"] = empretimos_completos["matricula_ou_siape"].astype(str)

# %% Atribute CDU to localizacao

empretimos_completos["cdu_classe"] = empretimos_completos["localizacao"].apply(mappying_class_cdu)

#%% See if works  

print(empretimos_completos.head(5))
