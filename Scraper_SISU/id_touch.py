import requests
import re
import sys
import datetime
import pandas as pd

n_from = 1
n_to = 6000

user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
base_url = 'https://sisu-api.sisu.mec.gov.br/api/v1'

def makeCodeID_Curse(base_url, n_from, n_to, user_agent):
    codeID = []
    for i in range(n_from, n_to+1, 1):
        try:
            r=requests.get(f'{base_url}/oferta/curso/{i}', headers = user_agent)
            data = r.json()
            nome_curso = data['search_rule']

            curse_object = {'nome_curso': nome_curso, 'id': i}
            codeID.append(curse_object)
        except:
            continue
    
    return codeID

listaID = makeCodeID_Curse(base_url, n_from, n_to, user_agent)
df = pd.DataFrame(listaID, columns=['nome_curso', 'id'])

df.to_excel(f'{n_from}_{n_to}.xlsx', index=False)