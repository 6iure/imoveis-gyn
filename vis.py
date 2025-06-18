
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

# %%
# %% mostrando as areas que o imovel contem mais de um tamanho
# todo como iremos tratar esses dados? fazendo a media OU dropando esses dados, pois sao 62linhas e nao fariam diferenca em um banco de dados de 20000 linhas, alem de que muitas ainda tem problemas em preco ou outras colunas
imoveis_temp = imoveis.dropna(subset=['AREAS'])
imoveis_temp[imoveis_temp['AREAS'].str.contains('-', regex=False)]

# %% tratando de dados NULOS, nesse caso o tratamento é dropar mesmo
imoveis = imoveis.dropna(subset=['TIPO', 'PRICE', 'AREAS'])
imoveis

# %% 
imoveis.info()

# %%

def converter_para_float(valor):
    try:
        valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
        return float(valor)
    except:
        return None

imoveis['PRICE_CONVERTED'] = imoveis['PRICE'].apply(converter_para_float)
imoveis['IPTU_CONVERTED'] = imoveis['IPTU'].apply(converter_para_float)
imoveis['CONDOMÍNIO_CONVERTED'] = imoveis['CONDOMÍNIO'].apply(converter_para_float)
# imoveis = imoveis.dropna(subset=['PRICE_CONVERTED'])


imoveis

# %% 

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

imoveis

# %%
imoveis['AREAS_CONVERTED'] = imoveis['AREAS'].apply(converter_area_para_float)
imoveis

#%%
imoveis['PRICE_M2'] = imoveis['PRICE_CONVERTED'] / imoveis['AREAS_CONVERTED']
imoveis


# %% Media dos precos/m2 dos imoveis
imoveis['PRICE_M2'].mean()
# %% Mediana dos precos/m2 dos imoveis3

imoveis['PRICE_M2'].median()

# %%
comparacao = imoveis.groupby('TIPO')['PRICE_M2'].describe()
comparacao

# %% 
# Gráfico de barras com as médias
medias = imoveis.groupby('TIPO')['PRICE_M2'].mean().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(x='TIPO', y='PRICE_M2', data=medias)
plt.xticks(rotation=45, ha='right') 
plt.title('Preço Médio por m² por Tipo de Imóvel')
plt.xlabel('Tipo de Imóvel')
plt.ylabel('Preço por m² (R$)')
plt.tight_layout() 
plt.show()

# %% boxplot com as infos de comparacao 
plt.figure(figsize=(12, 8))
sns.boxplot(
    x='TIPO',
    y='PRICE_M2',
    data=imoveis,
)

plt.xticks(rotation=45, ha='right') 
plt.title('Distribuição de Preço por m² por Tipo de Imóvel')
plt.show()



# %%
