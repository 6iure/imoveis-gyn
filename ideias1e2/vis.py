
#? objetivo: verificar se existe uma diferença significativa no preço por metro quadrado entre casas e apartamentos na região analisada
#?   Medidas uteis: Média e mediana do preço por m² para casas e para apartamentos
#? - Desvio padrão para ver a dispersão
#? - Gráficos: boxplot comparando os dois grupos
# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %%
imoveis_path = "../data/banco_de_dados.csv"
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
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['TIPO'].isin(['casas', 'apartamentos' ])]
imoveis_filtrado

# %% 
#* mostrando todos os imoveis que estao dentro de uma faixa de area
# tratamento foi feito usando a media da faixa que esta na area 
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

# %% #* dados descritivos antes de tratar os dados
imoveis_filtrado.groupby('TIPO')['PRICE_M2'].describe()

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
#* filtrando agora por PRECO/M2, usando a fonte do guia curta mais
imoveis_filtrado = imoveis_filtrado[imoveis_filtrado['PRICE_M2'] <= 20000]
imoveis_filtrado['PRICE_M2'].describe()

# %% agora dados descritivos depois de tratar os dados
imoveis_filtrado.groupby('TIPO')['PRICE_M2'].describe()
# %% boxplot com as infos de comparacao 
plt.figure(figsize=(12, 8))
sns.boxplot(
    x='TIPO',
    y='PRICE_M2',
    data=imoveis_filtrado,
    palette='viridis',  # Cores mais modernas
    width=0.6,         # Largura das caixas
    linewidth=1.5,      # Espessura das bordas
    fliersize=3,       # Tamanho dos outliers
)

plt.title('Distribuição de Preço por m² por Tipo de Imóvel', fontsize=16, pad=20, fontweight='bold')
plt.xlabel('Tipo de Imóvel', fontsize=12, fontweight='bold')
plt.ylabel('Preço por m² (R$)', fontsize=12, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.4)    # Grid suave
plt.tight_layout()  # Ajusta o layout

plt.show()
# %% grafico de dispersao e boxplot

plt.figure(figsize=(14, 8))

# Boxplot principal
box = sns.boxplot(
    x='TIPO',
    y='PRICE_M2',
    data=imoveis_filtrado,
    width=0.5,
    showfliers=False,
    palette='viridis',
    linewidth=2,
    boxprops=dict(alpha=0.7),
    whiskerprops={'linewidth': 1.5},
)

# Stripplot sobreposto
strip = sns.stripplot(
    x='TIPO',
    y='PRICE_M2',
    data=imoveis_filtrado,
    jitter=0.25,
    alpha=0.5,
    size=5,
    palette='viridis',
    edgecolor='gray',
    linewidth=0.5
)

plt.title('Distribuição de Preços por m² por Tipo de Imóvel e sua Dispersao', 
          fontsize=16, pad=20, fontweight='bold')
plt.xlabel('Tipo de Imóvel',fontweight='bold', fontsize=13, labelpad=10)
plt.ylabel('Preço por m² (R$)', fontsize=13, labelpad=10, fontweight='bold')
plt.yticks(fontsize=11)

# Ajuste final
plt.tight_layout()
sns.despine(left=True)
plt.show()

# %% #*ideia 2 - identificacao dos bairros com melhor custo beneficio e bairros com mais imoveis
import re 
# %%
def extrair_bairro(address):
    # Converter para minúsculas e remover espaços extras
    address = str(address).lower().strip()
    
    # Padrões para remover
    padroes_inicio = [
        r'^rua\s+.+,\s*', 
        r'^av\s+.+,\s*',
        r'^avenida\s+.+,\s*',
        r'^r\.\s+.+,\s*',
        r'^alameda\s+.+,\s*',
        r'^quadra\s+.+,\s*',
        r'^q\d\s*.+,\s*',
        r',\s*apto\s+.+$',
        r',\s*apartamento\s+.+$',
        r',\s*bloco\s+.+$'
    ]

    # Padrões para remover (parte final)
    padroes_fim = [
        r',\s*goiânia\s*$',
        r',\s*goiania\s*$',
        r',\s*apto\s+.+$',
        r',\s*apartamento\s+.+$',
        r',\s*bloco\s+.+$',
        r',\s*go\s*$',
        r'-go\s*$',
        r'\s*-\s*goiânia\s*$',
        r'\s*-\s*goiania\s*$'
    ]
    
    # Aplicar cada padrão de limpeza
    for padrao in padroes_inicio:
        address = re.sub(padrao, '', address, flags=re.IGNORECASE)

    # Aplicar cada padrão de limpeza no final
    for padrao in padroes_fim:
        address = re.sub(padrao, '', address, flags=re.IGNORECASE)
    
    # Remover números e caracteres especiais no início/fim
    address = re.sub(r'^[\d\W]+|[\d\W]+$', '', address).strip()
    
    # Capitalizar a primeira letra de cada palavra
    address = ' '.join([word.capitalize() for word in address.split()])
    
    # Correções manuais para nomes conhecidos
    correcoes = {
        'St.': 'Setor',
        'S.': 'Setor',
        'Res.': 'Residencial',
        'Resid.': 'Residencial',
        'Goiania': '',
        'Goiânia': ''
    }
    
    for erro, correto in correcoes.items():
        address = address.replace(erro, correto)
    
    return address

# Aplicar a função à coluna ADDRESS
imoveis_filtrado['bairro_limpo'] = imoveis_filtrado['ADDRESS'].apply(extrair_bairro)

# %%
# Agrupar por bairro limpo e calcular métricas consolidadas
bairros_consolidados = imoveis_filtrado.groupby('bairro_limpo').agg({
    'ADDRESS': 'count',
    'PRICE_CONVERTED': ['mean', 'median'],
    'AREAS_CONVERTED': ['mean', 'median'],
    'PRICE_M2' : ['mean', 'mean'],
    'TIPO': lambda x: x.value_counts().to_dict()
}).reset_index()

# Renomear colunas
bairros_consolidados.columns = [
    'bairro', 
    'total_imoveis',
    'preco_medio', 
    'mediana_preco',
    'area_media', 
    'mediana_area',
    'preco_m2_medio',
    'mediana_preco_m2',
    'distribuicao_tipo'
]

# Filtrar bairros com pelo menos 10 imóveis
bairros_consolidados = bairros_consolidados[bairros_consolidados['total_imoveis'] >= 10]

# Ordenar por número de imóveis
bairros_consolidados = bairros_consolidados.sort_values('total_imoveis', ascending=False)
bairros_consolidados

# %% 
bairros_consolidados['total_imoveis'].sum()
# %%
top_consolidados = bairros_consolidados.sort_values('total_imoveis', ascending=True).tail(15)
top_consolidados
# %%
plt.figure(figsize=(12,8))

barplot = sns.barplot(
    data=top_consolidados,
    y='bairro',
    x='total_imoveis',
    palette='viridis',
    alpha=0.8,
)

plt.title('Os 20 Bairros com maior Número de Imóveis na Amostra\n (Depois da Apuracao)', fontsize=16, pad=20, fontweight='bold')
plt.xlabel('Número de Imóveis', fontsize=12, fontweight='bold')
plt.ylabel('Bairro', fontsize=12, fontweight='bold')

# %%
top_consolidados
# %% 

plt.figure(figsize=(12, 7))
scatter = sns.scatterplot(
    data=top_consolidados, 
    x='mediana_area', 
    y='mediana_preco_m2', 
    hue='bairro', 
    palette='Spectral', 
    s=150,             
    alpha=0.8,
    edgecolor='black',
    linewidth=0.5
)

plt.title('Relação entre Area e Preço por m² nos Bairros com Melhor Custo Benefício', 
          fontsize=14, pad=20, fontweight='bold')
plt.xlabel('Mediana da Area (m²)', fontsize=12, fontweight='bold')
plt.ylabel('Mediana do Preço por m² (R$)', fontsize=12, fontweight='bold')

plt.legend(

    title='Bairros',
)

# Adicionar grid para melhor leitura
plt.grid(True, linestyle='--', alpha=0.3)

# Ajustar limites dos eixos se necessário
buffer_x = top_consolidados['mediana_area'].max() * 0.1
buffer_y = top_consolidados['mediana_preco_m2'].max() * 0.1
plt.xlim(0, top_consolidados['mediana_area'].max() + buffer_x)
plt.ylim(0, top_consolidados['mediana_preco_m2'].max() + buffer_y)

plt.tight_layout()
plt.show()
 
# %%
