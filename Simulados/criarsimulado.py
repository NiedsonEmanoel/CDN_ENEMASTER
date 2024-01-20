Disciplina = "MT" 

import numpy as np
import pandas as pd
import random
import time
from datetime import datetime
from urllib.parse import quote

urlItens = "https://github.com/NiedsonEmanoel/NiedsonEmanoel/raw/main/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/gerador/provasOrdernadasPorTri.csv"

dItens = pd.read_csv(urlItens, encoding='utf-8', decimal=',')

dItens = dItens[dItens['SG_AREA'] == Disciplina]
dItens = dItens[dItens['CO_HABILIDADE'].between(1, 30)]
dItens = dItens[dItens['IN_ITEM_ABAN'] == 0]

dItens.sort_values('theta_065', ascending=True, inplace=True)

if Disciplina == 'LC':
    dItens = dItens[~dItens['CO_HABILIDADE'].isin([5, 6, 7, 8])]

# Selecionar um item de cada habilidade de 1 a 30
habilidades_unicas = dItens.groupby('CO_HABILIDADE').sample(1)

# Selecionar os 12 itens restantes permitindo repetições, mas no máximo 3 repetições por habilidade
habilidades_repetidas = dItens.groupby('CO_HABILIDADE').apply(lambda x: x.sample(min(len(x), 3)))
habilidades_repetidas = habilidades_repetidas.sample(n=12, replace=True)

# Combinar os dataframes resultantes
resultado = pd.concat([habilidades_unicas, habilidades_repetidas])
resultado = resultado.drop_duplicates(subset='CO_ITEM')
# Obter as habilidades presentes no resultado atual
habilidades_presentes = resultado['CO_HABILIDADE'].unique()

# Verificar se todas as 30 habilidades estão presentes
if Disciplina != 'LC':
    if len(habilidades_presentes) < 30:
        # Calcular o número de habilidades faltantes
        habilidades_faltantes = np.setdiff1d(range(1, 31), habilidades_presentes)
        num_faltantes = 30 - len(habilidades_presentes)

        # Selecionar itens adicionais para as habilidades faltantes
        itens_faltantes = dItens[dItens['CO_HABILIDADE'].isin(habilidades_faltantes)].sample(n=num_faltantes, replace=True)

        # Combinar os itens faltantes com os resultados atuais
        resultado = pd.concat([resultado, itens_faltantes])

# Verificar o número de itens atual
num_itens = len(resultado)

# Remover itens extras se o número atual for maior que 45
if num_itens > 45:
    resultado = resultado.sample(n=45)

# Preencher com itens adicionais se o número atual for menor que 45
if num_itens < 45:
    num_adicionais = 45 - num_itens
    itens_adicionais = dItens.sample(n=num_adicionais, replace=True)
    itens_adicionais = itens_adicionais[~itens_adicionais['CO_ITEM'].isin(resultado['CO_ITEM'])]
    resultado = pd.concat([resultado, itens_adicionais])

# Exibir o resultado
print('Proficiência QMaisDificil: '+str(resultado.max()['theta_065']))
print('')
print('Proficiência QMaisFacil: '+str(resultado.min()['theta_065']))

def flashnamesa(SG):
    if SG == 'CN': return 'Natureza'
    elif SG == 'MT': return 'Matemática'
    elif SG == 'CH': return 'Humanas'
    else: return 'Linguagens'


def grn():
    # Obter o timestamp atual em segundos
    timestamp = int(time.time())

    # Definir o timestamp como semente para a função random
    random.seed(timestamp)

    # Gerar um número inteiro aleatório entre 0 e 100000
    return random.randint(0, 100000)


data_formatada = datetime.now().strftime("%d-%m-%Y")
name = f"{flashnamesa(Disciplina.upper())} - {grn()}{int(round((resultado.max()['theta_065']+resultado.min()['theta_065'])/2,0))} - {data_formatada}".upper()
# Formatar o nome para uso em um link
nome_formatado = quote(name)

# Criar o link
link = f"https://raw.githubusercontent.com/NiedsonEmanoel/CDN_ENEMASTER/main/Simulados/{nome_formatado}.csv"

print(name)
print(link)
resultado.to_csv(f"{name}.csv", encoding='utf-8', decimal=',')


