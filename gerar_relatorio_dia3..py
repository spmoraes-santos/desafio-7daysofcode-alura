#%%
import pickle
import os
from jinja2 import Environment, FileSystemLoader
import pdfkit
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Cria diretório de saída
os.makedirs("output", exist_ok=True)

# Carrega os dados salvos pelo analysis_1.py
with open("temp_data/dados_relatorio.pkl", "rb") as f:
    dados = pickle.load(f)

emprestimos_por_ano = dados["emprestimos_por_ano"]
emprestimos_por_mes = dados["emprestimos_por_mes"]
emprestimos_por_hora = dados["emprestimos_por_hora"]
emprestimos_unicos = dados["emprestimos_unicos"]
total_exemplares = dados["total_exemplares"]

# --- Gráficos em base64 ---
def fig_to_base64(fig):
    import io
    import base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


# Configura estilo global
sns.set_style("whitegrid")

# Gráfico por ano (linha)
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.lineplot(x=emprestimos_por_ano.index, y=emprestimos_por_ano.values,
             marker='o', linewidth=2.5, color='royalblue', ax=ax1)
ax1.set_title('Total de exemplares emprestados por ano', fontsize=16, weight='bold')
ax1.set_xlabel('Ano', fontsize=12)
ax1.set_ylabel('Quantidade de exemplares', fontsize=12)
ax1.set_xticks(emprestimos_por_ano.index)
ax1.tick_params(axis='both', labelsize=10)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
fig1.tight_layout()
grafico_ano = fig_to_base64(fig1)
plt.close(fig1)


# Gráfico por mês (linha)
fig2, ax2 = plt.subplots(figsize=(10, 6))
emprestimos_por_mes = emprestimos_por_mes.reindex(range(1, 13), fill_value=0)
emprestimos_por_mes.plot(marker='o', linewidth=2, color='royalblue', ax=ax2)
ax2.set_title('Exemplares emprestados por mês', fontsize=16, fontweight='bold')
ax2.set_xlabel('Mês', fontsize=12)
ax2.set_ylabel('Quantidade de exemplares', fontsize=12)
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], rotation=0)
ax2.tick_params(axis='both', labelsize=10)
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
fig2.tight_layout()
grafico_mes_linha = fig_to_base64(fig2)
plt.close(fig2)


# Gráfico por mês (barra)
fig3, ax3 = plt.subplots(figsize=(10, 6))
emprestimos_por_mes.plot(kind='bar', color='skyblue', ax=ax3)
ax3.set_title('Exemplares emprestados por mês', fontsize=16, fontweight='bold')
ax3.set_xlabel('Mês', fontsize=12)
ax3.set_ylabel('Quantidade de exemplares', fontsize=12)
ax3.set_xticks(range(0, 12))
ax3.set_xticklabels(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], rotation=0)
ax3.tick_params(axis='both', labelsize=10)
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Adiciona os valores sobre as barras
for i, v in enumerate(emprestimos_por_mes):
    ax3.text(i, v + max(emprestimos_por_mes)*0.01, str(v), ha='center', fontsize=9)

fig3.tight_layout()
grafico_mes_barra = fig_to_base64(fig3)
plt.close(fig3)


# Gráfico por hora
fig4, ax4 = plt.subplots(figsize=(10, 6))
emprestimos_por_hora.plot(kind='bar', color='#FF69B4', edgecolor='black', linewidth=0.6, ax=ax4)
ax4.set_title('Distribuição Horária dos Empréstimos na Biblioteca\n(2010–2020)', fontsize=16, weight='bold', pad=15)
ax4.set_xlabel('Hora do Dia (0–23)', fontsize=12)
ax4.set_ylabel('Quantidade de Exemplares Emprestados', fontsize=12)
ax4.tick_params(axis='both', labelsize=10)
ax4.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
ax4.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
fig4.tight_layout()
grafico_hora = fig_to_base64(fig4)
plt.close(fig4)

# Renderiza o HTML
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("relatorio_dia3.html")

html_content = template.render(
    total_exemplares=total_exemplares,
    emprestimos_unicos=emprestimos_unicos,
    grafico_ano=grafico_ano,
    grafico_mes_linha=grafico_mes_linha,
    grafico_mes_barra=grafico_mes_barra,
    grafico_hora=grafico_hora,
    data_geracao=datetime.now().strftime("%d/%m/%Y %H:%M")
)

with open("output/relatorio_dia3.html", "w", encoding="utf-8") as f:
    f.write(html_content)

pdfkit.from_file("output/relatorio_dia3.html", "output/relatorio_dia3.pdf")

print("✅ Relatório em PDF gerado com sucesso em: output/relatorio_dia3.pdf")
