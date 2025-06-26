# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# %%
imoveis_path = '../data/banco_de_dados.csv'
imoveis = pd.read_csv(imoveis_path)
imoveis
# %% tratando de dados NULOS, nesse caso o tratamento é dropar mesmo
imoveis_filtrado = imoveis.dropna(subset=['TIPO', 'PRICE', 'AREAS'])
imoveis_filtrado

# %% dropando os TIPOS de imoveis que nao vamos usar 
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['TIPO'].isin(['casas', 'apartamentos' ])]
imoveis_filtrado

# %% #* funcao para converter valores de preco, iptu e condominio de objeto para float

def converter_para_float(valor):
    try:
        valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
        return float(valor)
    except:
        return None

imoveis_filtrado['PRICE_CONVERTED'] = imoveis_filtrado['PRICE'].apply(converter_para_float)
imoveis_filtrado['IPTU_CONVERTED'] = imoveis_filtrado['IPTU'].apply(converter_para_float)
imoveis_filtrado['CONDOMÍNIO_CONVERTED'] = imoveis_filtrado['CONDOMÍNIO'].apply(converter_para_float)

imoveis_filtrado

# %% #* agora dropando os valores nulos de preco
imoveis_filtrado = imoveis_filtrado.dropna(subset=['PRICE','PRICE_CONVERTED'])
imoveis_filtrado

# %% #* para tratar os imoveis que estao dentro de uma faixa de area, convertemos as AREAS que estao numa faixa para sua media 

def converter_area_para_float(area):
    try:
        # Remove o "m²" e espaços
        area = str(area).replace('m²', '').replace(' ', '').strip()
        
        # Verifica se é um intervalo
        if '-' in area:
            partes = area.split('-')
            valores = [float(parte.replace(',', '.')) for parte in partes]
            return sum(valores) / len(valores)  # média
        else:
            return float(area.replace(',', '.'))
    except:
        return None

# %%
imoveis_filtrado['AREAS_CONVERTED'] = imoveis_filtrado['AREAS'].apply(converter_area_para_float)
imoveis_filtrado

#%%
imoveis_filtrado['PRICE_M2'] = imoveis_filtrado['PRICE_CONVERTED'] / imoveis_filtrado['AREAS_CONVERTED']
imoveis_filtrado

# %% #* filtrando primeiro por area, usando a fonte do diario de goias para o maior imovel a venda no estado que eh uma casa com 2600 m2 construidos.
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['AREAS_CONVERTED'] <= 2600]
imoveis_filtrado['AREAS_CONVERTED'].describe()

# %%
#* filtrando agora por PRECO/M2, usando a fonte do guia curta mais
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['PRICE_M2'] <= 20000]
imoveis_filtrado['PRICE_M2'].describe()

# %% agora dados descritivos depois de tratar os dados
imoveis_filtrado.groupby('TIPO')['PRICE_M2'].describe()


# %% #* IDEIA 3 - CLASSIFICANDO IMOVEIS POR FAIXA DE PRECO UTILIZANDO PERCENTIS

condicoes = [imoveis_filtrado['PRICE_M2'] <= 4500,
             (imoveis_filtrado['PRICE_M2'] > 4500) & (imoveis_filtrado['PRICE_M2'] <= 7000),
             (imoveis_filtrado['PRICE_M2'] > 7000) & (imoveis_filtrado['PRICE_M2'] <= 8000),
             imoveis_filtrado['PRICE_M2'] > 8000]

resultados = ['baixo_custo','medio_custo', 'alto_padrao', 'luxo']

imoveis_filtrado['faixa_preco'] = np.select(condicoes, resultados)
# %%
imoveis_filtrado

# %%
plt.figure(figsize=(10, 6))

sns.boxplot(
    data=imoveis_filtrado,
    x='faixa_preco',
    y='PRICE_M2',
    hue='faixa_preco',
    order=['baixo_custo', 'medio_custo', 'alto_padrao', 'luxo'],
    palette='viridis',
    )

plt.title('Distribuição de Imóveis por Faixa de Preço', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Faixa de Preço', fontsize=12, fontweight='bold')
plt.ylabel('Preco Médio do m²', fontsize=12, fontweight='bold')

plt.gca().yaxis.set_major_formatter('R${x:.0f}')

plt.tight_layout()
plt.show()

# %%
imoveis_filtrado['faixa_preco'].value_counts()

# %%
estatisticas_faixas = imoveis_filtrado.groupby('faixa_preco').agg({
    'faixa_preco' : ['count'],
    'PRICE_M2' : ['mean', 'median'],
    'AREAS_CONVERTED': ['mean', 'median'],
})

estatisticas_faixas.columns = [
    'total_imoveis',
    'media_preco_m2', 
    'mediana_preco_m2',
    'media_area',
    'mediana_area'
]
# %%
estatisticas_faixas
# %%
plt.figure(figsize=(12, 8))

barplot = sns.barplot(
    data=estatisticas_faixas,
    x='faixa_preco',
    y='total_imoveis',
    hue='faixa_preco',
    order=['baixo_custo', 'medio_custo', 'alto_padrao', 'luxo'],
    palette='viridis',
    width=0.5,
    edgecolor = 'black'
    )

for p in barplot.patches:
    barplot.annotate(f"{int(p.get_height())}", 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', 
                   xytext=(0, 10), 
                   textcoords='offset points',
                   fontsize=12,
                   fontweight='bold'
                   )

plt.title('Distribuição de Imóveis por Faixa de Preço', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Total de Imovéis', fontsize=12, fontweight='bold')
plt.xlabel('Faixa de Preço', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()
# %%
