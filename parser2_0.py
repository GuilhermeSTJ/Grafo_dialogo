import json
import string
import random
from tkinter import *
from tkinter import filedialog

#Guarda o nome dos scripts
nome_scripts= []

#Salva os dados referentes a links
linkos = [""]

def trataScript(tudo,linkos):
    conteudo = []
    nome = tudo['key']
    data  = tudo['text']
    data = data.split(";")
    links = ""

    #Laço que passa por todas linhas de script
    for d in data:
        value = []
        #Retira todos \n
        d = d.replace('\n', '')

        #aqui começamos com os casos
        if "speak:" in d:
            conteudo.append("\nspeak@"+ d.strip('speak:') +"@false@false")

        if "wait:" in d:
            conteudo.append("\nwait@" + d.strip('wait:'))

        if "listen:" in d:
            conteudo.append("\nvoice@command@trigger_asr")

    for l in linkos:
        if(l['from'] == nome):
            if l['to'] in nome_scripts:
                links = ("\nscript@add@"+l['to']+"@")

    if(links != ""):
        conteudo.append(links)

    #envia uma lista contendo todos scripts
    return conteudo

    
def trataEntrada(tudo):
    conteudo= []
    if 'input' in tudo:
        tudo = tudo['input']
        data = tudo.split(";")
        for d in data:
            d = d.replace('\n','')
            if(d != ""):
                conteudo.append('{"input":"' + d + '"}')
    return conteudo  

def trataSaida(tudo,linkos):
    conteudo = []
    out = ""
    action = '"actions":"script:'
    sai = []
    if 'output' in tudo:
        data = tudo['output']
        data = data.split(";")

        for d in data:
            d = d.replace('\n','')
            if(d !=""):
                out = '{"output":"' + d +'",'
        
            for l in linkos:
                if(l['from'] == tudo['key']):
                    sai.append(l['to'])
            for s in sai:
                action = action  + s + '"'
            out = out + action + ',"emotions":"","parameters":[]}'
            
    else:
        out = '{"output":"",'
        
        for l in linkos:
            if(l['from'] == tudo['key']):
                sai.append(l['to'])
        for s in sai:
            action = action  + s + '"'
        out = out + action + ',"emotions":"","parameters":[]}'
        
    return out


def trataEntities(linkos,tudo):
    conteudo = ""
    for l in linkos:
            if(l['to'] == tudo['key']):
                conteudo = ('{"name":"context:script:' + l['from'] + '"}')
    print(conteudo)

    return conteudo

def criaDialogo(dialog,linkos):
    n = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    print(n)
    uid = n + '-6bc0-45a7-a7ad-8672382be7aa'
    entrada = trataEntrada(dialog)
    saida = trataSaida(dialog,linkos)
    context = trataEntities(linkos,dialog)

    dialogo = '{"id":"'+ uid +'","mode":"-","inputs":'+ str(entrada).replace("'","") +',"outputs":['+ saida +'],"requires":[],"concepts":['+ context +'],"entities":['+ context+']}'
    f = open("Dialogos/" + uid + ".json", "w",encoding="utf-8")
    f.write(dialogo)
    f.close()

def criaScript(scri,linkos):

    uid = "52f2bc85-228e-477f-a2c4-c163aa1e8059"
    apid = "ae37d798-c643-495c-a9fc-7a42ced9f458"
    nome = scri['key'].strip('\n')
    conteudo = trataScript(scri,linkos)

    script = '{"uid":"' + uid + '","applicationUid":"'+ apid +'","name":"'+ nome +'","content":"' + "".join(conteudo) +'"}'

    f = open("Scripts/" + nome + ".json", "w",encoding="utf-8")
    f.write(script)
    f.close()


win=Tk()
win.geometry("450x200")

Label(win, text="Clique o botão e escolha o(s) arquivo(s) \n que deseja transformar!", font='Arial 16 bold').pack(pady=15)

def open_file():

    filepath = filedialog.askopenfilename(title="Pesquisar", filetypes=(("all files","*.*"), ("text    files","*.txt")))
    f = open(filepath,'r')
    k = 0
    data = json.load(f)

    #Salva os dados referentes a links
    linkos = data['linkDataArray']

    #remove todos links que encaixam em um 1 nó
    for l in linkos[:]:
       if len(l) == 1:
           linkos.remove(l)

    #Salva em uma lista o nome de todos scripts
    for i in data['nodeDataArray']:
        keys,values = zip(*i.items())
        if(values[0] == "Script"):
            nome_scripts.append(values[1])

    #Separa aqueles que são script e aqueles que são dialogo
    for j in data['nodeDataArray']:        
        keys,values = zip(*j.items())
        if(values[0] == "Script"):
            criaScript(j,linkos)
        if(values[0] == "Dialogo"):
            criaDialogo(j,linkos) 
    
    f.close()

#criaScript(nome,conteudo)
#criaDialogo(entrada,saida,context)
button = Button(win, text="Abra", command=open_file)
button.pack()

win.mainloop()

