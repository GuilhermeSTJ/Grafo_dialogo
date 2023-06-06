import json
import string
import random
from tkinter import *
from tkinter import filedialog

sUid = "258a67a1-c7ad-4988-a2da-19255d47ff9c"
sApp = "4141dd46-718d-46ef-ace1-ca647bf736b5"

def trataScript(data):
    conteudo = []
    data = data.split(";")
    text = ""

    #Laço que passa por todas linhas de script
    for d in data:
        value = []
        #Retira todos \n
        d = d.replace('\n', '')

        #aqui começamos com os casos
        if "speak" in d:
            value = d.split(":")
            if (len(value) > 1):
                text = "\nspeak@"+ value[1] +"@false@false"
                conteudo.append(text)

        if "wait" in d:
            value = d.split(":")
            if(len(value) > 1):
                text = "\nwait@" + value[1]
                conteudo.append(text)

        if "voice" in d:
            value = d.replace(':','')
            conteudo.append("\nvoice@command@trigger_asr")

    #envia uma lista contendo todos scripts
    return conteudo

def jsonScript(nome,cont):
    data_Script ={
        "uid":sUid,
        "applicationUid":sApp,
        "name":nome,
        "content":''.join(cont)
    }
    with open("C:/Users/Teo/Downloads/Script/"+ nome + '.json', 'w', encoding='utf-8') as f:
        json.dump( data_Script, f, ensure_ascii=False, indent=4)

def jsonDialogo():
    nome = ''

def procScript(data,elos,nomeScripts):
    nome = data['key']
    script = ""
    links = ""
    
    #Se o valor do texto não for nulo modificar
    if 'text' in data:
        script = data['text']

    #Transforma os textos no padrão aceito pela plataforma
    conteudo = trataScript(script)

    #Verifica se há um script que vai para outro script
    for l in elos:
        if(l['from'] == nome):
            if l['to'] in nomeScripts:
                links = ("\nscript@add@"+l['to']+"@")

    #Verifica se há links para serem salvos
    if(links != ""):
        conteudo.append(links)

    #Envia todo conteudo para ser transformado em json
    jsonScript(nome, conteudo)

def procDialogo(data,elos):
    entrada = ""
    saida = ""
    linkIn = []
    linkOut = []

    #Verifica se há input ou output nesse dialogo
    #Se tiver salva a variavel
    if 'input' in data:
        entrada = data['input']
    if 'output' in data:
        saida = data['output']

    #Verifica se há links vindo
    for i in elos:
        if(i['to'] == data['key']):
            linkIn.append(i)

    #Verifica se há links saindo
    for o in elos:
        if(o['from'] == data['key']):
            linkOut.append(o)

    jsonDialogo(entrada,saida,linkIn,linkOut)
def inicia(json):

    #Cria duas listas, uma contendos os links e a outra contendo os dados
    elos = json['linkDataArray']
    data = json['nodeDataArray']

    #Retira todos links que só encaixam em 1 nó
    for l in elos[:]:
       if len(l) == 1:
           elos.remove(l)

    #Cria uma lista contendo o nome de todos scripts
    #Vai ser usado para verificar se existe um script indo para outro script
    nomeScripts = []
    for d in data:
        if(d['category'] == 'Script'):
            nomeScripts.append(d['key'])
    
    #Seleciona Somente os nós que sejam de Dialogo e Script
    for j in data:
        if(j['category'] == 'Dialogo'):
            procDialogo(j,elos)
        if(j['category'] == 'Script'):
            procScript(j,elos,nomeScripts)


win=Tk()
win.geometry("450x200")

Label(win, text="Clique o botão e escolha o(s) arquivo(s) \n que deseja transformar!", font='Arial 16 bold').pack(pady=15)

def open_file():

    filepath = filedialog.askopenfilename(title="Pesquisar", filetypes=(("all files","*.*"), ("text    files","*.txt")))
    #filepath = "C:/Users/Teo/Downloads/Robo/saida.json"
    f = open(filepath,'r')
    data = json.load(f)

    inicia(data)
    f.close()

button = Button(win, text="Abra", command=open_file)
button.pack()

win.mainloop()



