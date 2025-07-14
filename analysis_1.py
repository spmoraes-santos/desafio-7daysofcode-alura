### Created by S P Moraes-Santos

## Day 1- Load & Merge Data
#%% Libraries needed
from scripts.read_files import load_csvs,load_excels,load_parquets,load_url_file
from scripts.prepare_dfs import prepare_dataframe
from scripts.atribute_cdu import mappying_class_cdu
import matplotlib.pyplot as plt  
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.ticker as ticker
import pandas as pd
#%% Paths 
#caminho_emprestimos = "Datasets\\Dia 1\\emprestimos-*.csv"
caminho_emprestimos = "Datasets/Dia 1/emprestimos-*.csv"
caminho_exemplares = "https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_1-Importando_dados/Datasets/dados_exemplares.parquet"

#%% Load data, clean and check from first analysis
emprestimos_biblioteca = load_csvs(caminho_emprestimos)
emprestimos_biblioteca = prepare_dataframe(emprestimos_biblioteca, 'data_emprestimo')
emprestimos_biblioteca = prepare_dataframe(emprestimos_biblioteca, 'data_renovacao')
emprestimos_biblioteca = prepare_dataframe(emprestimos_biblioteca, 'data_devolucao')
#%% Load more data and check
dados_exemplares = load_parquets(caminho_exemplares)
print(dados_exemplares.head())


#%% Merge datasets
emprestimos_completos = emprestimos_biblioteca.merge(dados_exemplares)

##### Day 2 - Cleanup and Attribute Context
#%% See the header
emprestimos_completos.head(5) 

# %%  Drop registro_sistema
emprestimos_completos.drop('registro_sistema', axis=1, inplace=True)
emprestimos_completos.head(5)
# %% Transform matricula_ou_siape type into string
emprestimos_completos["matricula_ou_siape"] = emprestimos_completos["matricula_ou_siape"].astype(str)

# %% Atribute CDU to localizacao

emprestimos_completos["cdu_classe"] = emprestimos_completos["localizacao"].apply(mappying_class_cdu)

#%% See if works  

print(emprestimos_completos.head(5))

##### Day 3 - Understanding the loan patterns of the items
#%% Couting loans 
emprestimos_completos['id_emprestimo'].value_counts()
#%% Since loans can have more than 1 item, drop duplicates
emprestimos_unicos = emprestimos_completos['id_emprestimo'].nunique()
print(f'Total de empréstimos realizados: {emprestimos_unicos}')

#%% Total of items
emprestimos_total = len(emprestimos_completos)
print(f'Total de exemplares emprestados: {emprestimos_total}')
#%% Grouping items per year
emprestimos_data = emprestimos_completos.copy()

emprestimos_data['ano'] = emprestimos_completos['data_emprestimo'].dt.year
emprestimos_por_ano = emprestimos_data.groupby('ano').size()
#%% Plotting items per year 
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.lineplot(x=emprestimos_por_ano.index, y=emprestimos_por_ano.values, marker='o', linewidth=2.5, color='royalblue')
plt.title('Total de exemplares emprestados por ano', fontsize=16, weight='bold')
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Quantidade de exemplares', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(emprestimos_por_ano.index, rotation=0)
plt.tight_layout()
plt.show()
#%% Grouping items per month and coutting
emprestimos_data['mes'] = emprestimos_completos['data_emprestimo'].dt.month
emprestimos_por_mes = emprestimos_data.groupby('mes').size()

#%% Plotting as lineplot ()
emprestimos_por_mes = emprestimos_por_mes.reindex(range(1, 13), fill_value=0)

fig, ax = plt.subplots(figsize=(10, 6))
emprestimos_por_mes.plot(
    kind='line',
    marker='o',
    linewidth=2,
    color='royalblue',
    ax=ax
)
ax.set_title('Exemplares emprestados por mês', fontsize=16, fontweight='bold')
ax.set_xlabel('Mês', fontsize=12)
ax.set_ylabel('Quantidade de exemplares', fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels([
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
], rotation=0)
ax.tick_params(axis='both', labelsize=10)
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()
plt.show()

# %% Plotting as a barplot
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))
emprestimos_por_mes.plot(
    kind='bar',
    color='skyblue',
    ax=ax
)
ax.set_title('Exemplares emprestados por mês', fontsize=16, fontweight='bold')
ax.set_xlabel('Mês', fontsize=12)
ax.set_ylabel('Quantidade de exemplares', fontsize=12)
ax.set_xticks(range(0, 12))
ax.set_xticklabels([
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
], rotation=0)
ax.tick_params(axis='both', labelsize=10)

for i, v in enumerate(emprestimos_por_mes):
    ax.text(i, v + max(emprestimos_por_mes)*0.01, str(v), ha='center', fontsize=9)

plt.tight_layout()
plt.show()


# %% Items by hour
emprestimos_data['hora'] = emprestimos_completos['data_emprestimo'].dt.hour

emprestimos_por_hora = emprestimos_data.groupby('hora').size()

#%% Plotting items by hour

sns.set_style("whitegrid")
sns.set_palette("pastel")
plt.figure(figsize=(12, 6))
plt.figure(figsize=(12, 6))

sns.barplot(
    x=emprestimos_por_hora.index,
    y=emprestimos_por_hora.values,
    color='#FF69B4',
    edgecolor='black',
    linewidth=0.6
)

plt.title('Distribuição Horária dos Empréstimos na Biblioteca\n(2010–2020)', fontsize=16, weight='bold', pad=15)
plt.suptitle('Dados agregados por hora do dia', fontsize=11, color='gray')
plt.xlabel('Hora do Dia (0–23)', fontsize=12)
plt.ylabel('Quantidade de Exemplares Emprestados', fontsize=12)
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
sns.despine()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
# %% Data to report
# %% Data to report
import pickle
import os

os.makedirs("temp_data", exist_ok=True)

with open("temp_data/dados_relatorio.pkl", "wb") as f:
    pickle.dump({
        "total_exemplares": emprestimos_total,  # <-- corrigido aqui
        "emprestimos_unicos": emprestimos_unicos,
        "emprestimos_por_ano": emprestimos_por_ano,
        "emprestimos_por_mes": emprestimos_por_mes,
        "emprestimos_por_hora": emprestimos_por_hora
    }, f)

print(" Dados salvos para o relatório em temp_data/dados_relatorio.pkl")

# %%
