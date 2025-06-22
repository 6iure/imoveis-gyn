
#? objetivo: verificar se existe uma diferença significativa no preço por metro quadrado entre casas e apartamentos na região analisada
#?   Medidas uteis: Média e mediana do preço por m² para casas e para apartamentos
#? - Desvio padrão para ver a dispersão
#? - Gráficos: boxplot comparando os dois grupos
# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %%
imoveis_path = "data/banco_de_dados.csv"
imoveis = pd.read_csv(imoveis_path)
imoveis
# %% 
imoveis.head()

# %% tratando de dados NULOS, nesse caso o tratamento é dropar mesmo
imoveis_filtrado = imoveis.dropna(subset=['TIPO', 'PRICE', 'AREAS'])
imoveis_filtrado

# %%
imoveis['TIPO'].unique()

# %% dropando os TIPOS de imoveis que nao vamos usar, #todo considerar os outros apartamentos pequenos futuramente 
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['TIPO'].isin(['casas', 'apartamentos'])]
imoveis_filtrado

# %% 
#* mostrando todos os imoveis que estao dentro de uma faixa de area
# todo como iremos tratar esses dados? 
imoveis_filtrado[imoveis_filtrado['AREAS'].str.contains('-', regex=False)]

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
# imoveis_filtrado = imoveis_filtrado.dropna(subset=['IPTU' ,'IPTU_CONVERTED'])
# imoveis_filtrado = imoveis_filtrado.dropna(subset=['CONDOMÍNIO' ,'CONDOMÍNIO_CONVERTED'])

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


# %% Media dos precos/m2 dos imoveis
imoveis_filtrado['PRICE_M2'].mean()
# %% Mediana dos precos/m2 dos imoveis
imoveis_filtrado['PRICE_M2'].median()

# %%
comparacao = imoveis_filtrado.groupby('TIPO')['PRICE_M2'].describe()
comparacao

# %% 
# Gráfico de barras com as médias
medias = imoveis_filtrado.groupby('TIPO')['PRICE_M2'].mean().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(x='TIPO', y='PRICE_M2', data=medias)
# plt.xticks(rotation=45, ha='right') 
plt.title('Preço Médio por m² por Tipo de Imóvel')
plt.xlabel('Tipo de Imóvel')
plt.ylabel('Preço por m² (R$)')
plt.tight_layout() 
plt.show()

# %% 
imoveis_filtrado['AREAS_CONVERTED'].describe()

# %% #* filtrando primeiro por area, usando a fonte do diario de goias para o maior imovel a venda no estado que eh uma casa com 2600 m2 construidos.
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['AREAS_CONVERTED'] <= 2600]
imoveis_filtrado['AREAS_CONVERTED'].describe()

# %%

imoveis_filtrado['PRICE_M2'].describe()
# %%
#* filtrando agora por PRECO, usando a fonte do guia curta mais
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['PRICE_M2'] <= 50000]
imoveis_filtrado['PRICE_M2'].describe()

# %%
# %% boxplot com as infos de comparacao 
plt.figure(figsize=(12, 8))
sns.boxplot(
    x='TIPO',
    y='PRICE_M2',
    data=imoveis_filtrado,
)

# plt.xticks(rotation=45, ha='right') 
plt.title('Distribuição de Preço por m² por Tipo de Imóvel')
plt.show()
# %%
imoveis_filtrado.groupby('TIPO')['PRICE_M2'].describe()
# %%
