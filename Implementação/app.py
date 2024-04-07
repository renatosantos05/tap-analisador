from functools import reduce
import re
import os
import json


def AcessarDiretorio():
    print("Digite o caminho para o diretório que Contem as Legendas:")
    diretorio = input()
    try:
        os.chdir(diretorio)
        print(f"Diretório alterado para: {diretorio}")
    except OSError as e:
        print(f"Erro ao tentar acessar o diretório: {diretorio}")
        AcessarDiretorio()

AcessarDiretorio()

temporada = []

for i in list(filter(lambda x : x.endswith(".srt"),os.listdir())):
    with open(i,"r",encoding = "utf-8") as arquivo:
        padrao = re.compile('[a-zA-Z]')
        padraoRemocao = re.compile('<i>|♪|!|\n|</i>|;|\.|\,|:|\?|\-|@"')

        strings = list(map(lambda x: re.sub(padraoRemocao, '', x).lower(),
                        filter(lambda x: re.search(padrao, x), arquivo.readlines())))
        strings = list(filter(lambda x: re.search(padrao,x),
                        reduce(lambda acumulador , x: acumulador + x.split(" "),strings , [])))
        temporada.extend(strings)

        contador = dict(sorted(reduce(lambda dicionario, x: {**dicionario, x: strings.count(x)}, set(strings),{})
                        .items(), key=lambda x: x[1],reverse=True))
        
        os.mkdir("Resultados") if not os.path.exists("Resultados") else None
        with  open(f"Resultados/{arquivo.name}.json", "w") as arquivo_resultado:
            MontarJson = lambda dicionario:arquivo_resultado.write(json.dumps([{"palavra": chave, "frequencia": valor} 
                        for chave,valor in dicionario.items()],indent=4))
            MontarJson(contador)
contadorTemporada = dict(sorted(reduce(lambda dicionario, x: {**dicionario, x: temporada.count(x)}, set(temporada),{})
                        .items(), key=lambda x: x[1],reverse=True))
        
os.mkdir("Resultados") if not os.path.exists("Resultados") else None
with  open(f"Resultados/{os.path.basename(os.getcwd())}.json", "w") as arquivo_resultado:
    MontarJson = lambda dicionario:arquivo_resultado.write(json.dumps([{"palavra": chave, "frequencia": valor} 
                        for chave,valor in dicionario.items()],indent=4))
    MontarJson(contadorTemporada)           












