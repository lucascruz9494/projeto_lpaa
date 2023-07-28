import pandas as pd
import numpy as np
from copy import deepcopy
from google.colab import files
import matplotlib.pyplot as plt
from google.colab import drive
import seaborn as sns
from matplotlib.animation import FuncAnimation
drive.mount('/content/drive',force_remount=True)
#substituir diretorio do dataset
df = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/CAERS_ASCII_2004_2017Q2.csv').dropna()
df=df.drop(["PRI_FDA Industry Name","RA_CAERS Created Date", 'PRI_Product Role'],axis=1).copy()
df= df.rename(columns={
    'RA_Report #':'ID_REGISTRO',
    'AEC_Event Start Date':'DATA_OCORRENCIA',
    'PRI_Reported Brand/Product Name':'MARCA_PRODUTO',
    'PRI_FDA Industry Code':'CODIGO_EMPRESA',
    'CI_Age at Adverse Event':'IDADE_VITIMA',
    'CI_Gender':'GENERO_VITIMA',
    'CI_Age Unit':'UNIDADE_IDADE',
    'AEC_One Row Outcomes':'CONSEQUENCIA_VITIMA',
    'SYM_One Row Coded Symptoms':'SINTOMAS'


})
df

df=df.loc[~df.duplicated(subset=['ID_REGISTRO'])].copy()

df = df[df['GENERO_VITIMA'] != 'Not Available']
df = df[df['GENERO_VITIMA'] != 'Not Reported']
df = df[df['GENERO_VITIMA'] != 'Unknown']
df

df['IDADE_VITIMA'] = np.where(df['UNIDADE_IDADE'] == "Year(s)", df['IDADE_VITIMA'], df['IDADE_VITIMA']/12)
def handle_idade(value):
  return value
df["IDADE_VITIMA"]=df['IDADE_VITIMA'].apply(handle_idade)
df

consquencias=df["CONSEQUENCIA_VITIMA"].value_counts().head(10)
consquencias

empresa=df["CODIGO_EMPRESA"].value_counts().head(10)
empresa

produto=df["MARCA_PRODUTO"].value_counts().head(10)
produto

sintomas=df["SINTOMAS"].value_counts().head(10)
sintomas

def handle_sintomas(value):
  if value in sintomas:
    return value
  else:
    return None
dfSintomas=df.copy()
dfSintomas["SINTOMAS"]=dfSintomas['SINTOMAS'].apply(handle_sintomas)
dfSintomas['SINTOMAS'].value_counts()
dfSintomas=dfSintomas.dropna()
dfSintomas

plt.figure(figsize=(10, 6))
dfSintomas['SINTOMAS'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Frequência dos 10 Sintomas mais recorrentes')
plt.xlabel('Sintomas')
plt.ylabel('Contagem')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

def handle_consequencias(value):
  if value in consquencias:
    return value
  else:
    return None
dfConsequencias=df.copy()
dfConsequencias["CONSEQUENCIA_VITIMA"]=dfConsequencias['CONSEQUENCIA_VITIMA'].apply(handle_consequencias)
dfConsequencias['CONSEQUENCIA_VITIMA'].value_counts()
dfConsequencias=dfConsequencias.dropna()
dfConsequencias

plt.figure(figsize=(10, 6))
dfConsequencias['CONSEQUENCIA_VITIMA'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Frequência das 10 consequencias mais recorrentes')
plt.xlabel('Consequencias')
plt.ylabel('Contagem')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

def handle_produto(value):
  if value in produto:
    return value
  else:
    return None
dfProduto=df.copy()
dfProduto["MARCA_PRODUTO"]=dfProduto['MARCA_PRODUTO'].apply(handle_produto)
dfProduto['MARCA_PRODUTO'].value_counts()
dfProduto=dfProduto.dropna()
dfProduto

plt.figure(figsize=(10, 6))
dfProduto['MARCA_PRODUTO'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Frequência dos 10 produtos que mais tiveram ocorrencias')
plt.xlabel('Produtos')
plt.ylabel('Contagem')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()





top_10_sintomas = df['SINTOMAS'].value_counts().nlargest(10).index
top_10_consequencia = df['CONSEQUENCIA_VITIMA'].value_counts().nlargest(10).index
top_10_marca_produto = df['MARCA_PRODUTO'].value_counts().nlargest(10).index
top_10_codigo_empresa = df['CODIGO_EMPRESA'].value_counts().nlargest(10).index
dataframe_filtered = df[
    (df['SINTOMAS'].isin(top_10_sintomas)) &
    (df['CONSEQUENCIA_VITIMA'].isin(top_10_consequencia)) &
    (df['MARCA_PRODUTO'].isin(top_10_marca_produto)) &
    (df['CODIGO_EMPRESA'].isin(top_10_codigo_empresa))
]
plt.figure(figsize=(10, 6))
dataframe_filtered.groupby(['SINTOMAS', 'CONSEQUENCIA_VITIMA']).size().unstack().plot(kind='bar', stacked=True)
plt.title('Relação entre Sintomas e Consequência na Vítima (Top 10)')
plt.xlabel('Sintomas')
plt.ylabel('Contagem')
plt.xticks(rotation=90)
plt.legend(fontsize='small', bbox_to_anchor=(1.02, 1), loc='upper left')

plt.show()



top_10_sintomas = df['SINTOMAS'].value_counts().nlargest(10).index
top_10_consequencia = df['CONSEQUENCIA_VITIMA'].value_counts().nlargest(10).index


dataframe_filtered = df[
    (df['SINTOMAS'].isin(top_10_sintomas)) &
    (df['CONSEQUENCIA_VITIMA'].isin(top_10_consequencia))
]


dataframe_filtered['DATA_OCORRENCIA'] = pd.to_datetime(dataframe_filtered['DATA_OCORRENCIA']).dt.year

fig, axes = plt.subplots(nrows=len(dataframe_filtered['DATA_OCORRENCIA'].unique()), ncols=1, figsize=(10, 6*len(dataframe_filtered['DATA_OCORRENCIA'].unique())))
plt.subplots_adjust(hspace=0.5)

for i, year in enumerate(dataframe_filtered['DATA_OCORRENCIA'].unique()):
    ax = axes[i]
    df_year = dataframe_filtered[dataframe_filtered['DATA_OCORRENCIA'] == year]
    grouped_data = df_year.groupby(['SINTOMAS', 'CONSEQUENCIA_VITIMA']).size().unstack(fill_value=0)
    grouped_data.plot(kind='bar', stacked=True, ax=ax, colormap='tab20', edgecolor='black', width=0.8)

    ax.set_title(f'Top 10 Sintomas e Consequências - Ano {year}')
    ax.set_xlabel('Sintomas')
    ax.set_ylabel('Contagem')
    ax.legend(title='Consequência na Vítima', fontsize='small')
    ax.set_xticklabels(grouped_data.index, rotation=90, ha='center')

plt.tight_layout()
plt.show()

top_10_sintomas = df['SINTOMAS'].value_counts().nlargest(10).index
top_10_consequencia = df['CONSEQUENCIA_VITIMA'].value_counts().nlargest(10).index
top_10_marca_produto = df['MARCA_PRODUTO'].value_counts().nlargest(10).index


df['SINTOMAS'] = df['SINTOMAS'].astype('category')
df['CONSEQUENCIA_VITIMA'] = df['CONSEQUENCIA_VITIMA'].astype('category')
df['MARCA_PRODUTO'] = df['MARCA_PRODUTO'].astype('category')



dataframe_filtered = df[(df['SINTOMAS'].isin(top_10_sintomas))
    & (df['CONSEQUENCIA_VITIMA'].isin(top_10_consequencia)) &
    (df['MARCA_PRODUTO'].isin(top_10_marca_produto))
]


plt.figure(figsize=(12, 8))


colors = plt.cm.rainbow_r(dataframe_filtered['SINTOMAS'].cat.codes / len(top_10_sintomas))


plt.scatter(dataframe_filtered['CONSEQUENCIA_VITIMA'], dataframe_filtered['MARCA_PRODUTO'], s=100, c=colors, alpha=0.7)

plt.title('Relação entre Sintomas, Consequências e Marca do Produto (Top 10 Sintomas, Consequências e Marcas)')
plt.xlabel('Consequência na Vítima')
plt.ylabel('Marca do Produto')
plt.xticks(rotation=90)
plt.legend(top_10_sintomas, title='Sintomas')
plt.colorbar(label='Sintomas')

plt.show()

plt.figure(figsize=(10, 6))
df['CODIGO_EMPRESA'].value_counts().nlargest(10).plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Contagem de Ocorrências por Empresa (Top 10)')
plt.xlabel('Empresa (Código)')
plt.ylabel('Contagem')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

plt.figure(figsize=(16, 16))
top_10_genero = df['GENERO_VITIMA'].value_counts().nlargest(10)
df_top_10_genero = df[df['GENERO_VITIMA'].isin(top_10_genero.index)]

df_top_10_genero['GENERO_VITIMA'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightcoral', 'lightblue'], startangle=90)
plt.title('Distribuição dos 10 Gêneros mais Frequentes da Vítima')
plt.axis('equal')

plt.show()

plt.figure(figsize=(50, 100))
plt.scatter(df['IDADE_VITIMA'], df['CONSEQUENCIA_VITIMA'], alpha=0.5, color='tomato')
plt.title('Relação entre Idade da Vítima e Consequência')
plt.xlabel('Idade da Vítima')
plt.ylabel('Consequência')
plt.xticks(range(0, 101, 10))
plt.show()

plt.figure(figsize=(12, 6))
df['DATA_OCORRENCIA'] = pd.to_datetime(df['DATA_OCORRENCIA'])
df['DATA_OCORRENCIA'].value_counts().resample('Y').sum().plot(color='mediumseagreen', marker='o')
plt.title('Tendência de Ocorrências ao Longo do Ano')
plt.xlabel('Ano')
plt.ylabel('Contagem')
plt.tight_layout()
plt.show()
