from argparse import ArgumentError
from ast import If
import os
import shutil

def validaPath(path):
    if not os.path.isdir(path):
        raise ArgumentError(None,'Caminho informado inválido' )

def validaArgumento(args):
    if len(args) == 0:
        raise ArgumentError(None, 'Nenhum argumento informado, favor fornecer o caminho e a data do arquivo como argumento.')
    if len(args) < 2:
        raise ArgumentError(None, 'Quantidade de argumentos insuficientes, favor fornecer o caminho e a data do arquivo como argumento.')
    if len(args) > 2:
        raise ArgumentError(None, 'Quantidade de argumentos fornecidade maior que o necessário')
        
def validaArquivos(arquivos, data):
    arquivosProcessar = []
    for arquivo in arquivos:
        if '.TXT' in arquivo and data in arquivo:
            arquivosProcessar.append(arquivo)
    
    if len(arquivosProcessar) == 0:    
        raise FileNotFoundError('Nenhum arquivo correspondente a data {} e a extenção de arquivo .TXT encontrado.'.format(data)) from None

    return arquivosProcessar

def abreArquivo(caminho, arquivo):
    arquivoAberto = open(caminho +'/'+ arquivo, 'r')
    return arquivoAberto
                
def processaArquivos(path, data):
    validaPath(path)
    contador = 1
    lista = []
    for pasta, subpastas, arquivos in os.walk(path):
        if contador == 1:
            print('Arquivos: ', arquivos)
            print('Subpastas: ', subpastas)
            print('Pasta atual: ', pasta)
            lista = validaArquivos(arquivos, data)
        contador += 1
    return lista

def splitaPontoVirgula(linha):
    return linha.split(';')

def splitaPipe(value):
    indexPipe = value.rfind('|')
    if indexPipe == -1:
        indexPipe = len(value)
        
    v = value[0:indexPipe]
    return v.split('|')   

def expandeDados(linha, escreveArquivo):
    
    linhas = []
    
    valoresSplitadosPontoVirgula = splitaPontoVirgula(linha.strip())
    planos = splitaPipe(valoresSplitadosPontoVirgula[2])
    valoresPlanos = splitaPipe(valoresSplitadosPontoVirgula[3])
    
    for i in range(len(planos)):
        linhas = [valoresSplitadosPontoVirgula[0], valoresSplitadosPontoVirgula[1], planos[i], valoresPlanos[i]]
        escreveArquivo.write(';'.join(linhas)+'\n')
                
def excluiArquivoTratado(arquivosSaida, caminho):
    for arquivo in arquivosSaida:
        if os.path.exists(caminho + '/' + arquivo):
            os.remove(caminho + '/' + arquivo)

def iteraLinhasArquivo(arquivoAberto):
    nomeArquivo = arquivoAberto.name
    escreveArquivo = open(nomeArquivo.replace('.BAK', '.txt'), 'w')
    try:
        while(True):
            linha = arquivoAberto.readline()
            
            if len(linha.strip()) == 0:
                print('Saindo do loop')
                break
            
            expandeDados(linha, escreveArquivo)            
            
    finally:
        arquivoAberto.close()
        escreveArquivo.close()
        
def montaArquivoSaida(arquivos):
    arquivosSaida = []
    for arquivo in arquivos:
            arquivosSaida.append(arquivo.replace('.BAK', '.txt'))
    return arquivosSaida

def renomeiaArquivos(arquivos, caminho):
    arquivosRenomeados = []
    for arquivo in arquivos:
        arquivoRenomeado = arquivo.upper().replace('.TXT', '.BAK')
        os.rename(caminho +'/'+ arquivo, caminho +'/'+ arquivoRenomeado)
        arquivosRenomeados.append(arquivoRenomeado)
    return arquivosRenomeados

def moveArquivoOriginal(arquivos, caminho):
    
    backup = caminho + '/BACKUP'
    
    if not os.path.exists(backup):
        os.mkdir(backup)
    
    for arquivo in arquivos:
        shutil.move(caminho +'/'+ arquivo, backup)
        
def main():
    arquivosSaida = []
    caminho = ''
    try:
        '''argumentos = sys.argv
        argumentos.pop(0)'''
        argumentos = ['C:/Arquivo', '03_2022']
        validaArgumento(argumentos)
        caminho = argumentos[0]
        dataArquivo = argumentos[1]
        
        arquivos = processaArquivos(caminho, dataArquivo)
        
        arquivos = renomeiaArquivos(arquivos, caminho)
        
        arquivosSaida = montaArquivoSaida(arquivos)
        
        for arquivo in arquivos:
            iteraLinhasArquivo(abreArquivo(caminho, arquivo))
            
        moveArquivoOriginal(arquivos, caminho)
    
    except ArgumentError as e:
        print('Erro ao tratar arquivo: ', e.message)
        excluiArquivoTratado(arquivosSaida, caminho)
    except Exception as e:
        print('Erro ao realizar transformação do arquivo:', e)
        excluiArquivoTratado(arquivosSaida, caminho)
            
main()