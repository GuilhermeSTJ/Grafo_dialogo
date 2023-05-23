import json
import string
import random
from tkinter import *
from tkinter import filedialog

class script():
    nome_script = ""
    conteudo = ""
    link_script = ""

    def __init__(self,n,c):
        self.nome_script = n
        self.conteudo = c
    
    def printa(self):
        print("SCRIPT ")
        print("nome:" + self.nome_script + "  link para:" + self.link_script)
        print(" O conteudo é: \n" + self.conteudo)
        
    def link(self,l):
        self.link_script = l
        
class dialogo():
    nome_dialog = ""
    inputs = ""
    outputs = ""
    link_in = ""
    link_out = ""
    
    def __init__(self,n):
        self.nome_dialog = n
    
    def setInput(self,inp):
        self.inputs = inp
        
    def setOutput(self,out):
        self.outputs = out        
        
    def printa(self):
        print("DIALOGO ")
        print("nome:" + self.nome_dialog + "  link in:" + self.link_in + "  link out:" + self.link_out)
        print("o(s) input(s): \n" + self.inputs )
        print("o(s) outuput(s): \n" + self.outputs)
    
    def linkIn(self, l):
        self.link_in = l
        
    def linkOut(self, o):
        self.link_out = o  

#Função para criação do json do dialogo
def jsonDialogo(inputs,outputs,linkIn,linkOut):
    dId = "1c232c57-7f59-407c-ae16-08bafaabc1d6"

    #Aqui vamos estruturar os inputs de forma a ficar no padrao da empresa
    inputSeparado = inputs.split(";")
    inputCompleto = ('[{"input":' + inputs + '}]')
    if(len(inputSeparado) != 1):
        inputCompleto = []
        for i in inputSeparado:
            inputCompleto.append('{"input":' + i + '}')

    outputSeparado = outputs.split(";")
    outputCompleto = ('[{"output":' + outputs + '}]')
    if(len(outputSeparado) != 1):
        outputCompleto = []
        for o in outputSeparado:
            outputCompleto.append('{"output":' + o + '}')

    out = str(outputCompleto).replace("'","")
    inp = str(inputCompleto).replace("'","")
    data_Dialog = {
        'id' : dId ,
        'mode' :"-",
        'inputs' : inp,
        'outputs': [{
            'output' :out,
            'actions' :"script:" + linkOut,
            'emotions' :"",
            'parameters' :[]
        }],
        'requires':[],
        'concepts':[{
            'name' :"context:script:" + str(linkIn)
        }],
        'entities' :[{
            'name' :"context:script:" + str(linkIn)
        }]
    }

    letters = string.ascii_lowercase
    digitos = string.digits
    nome = ( ''.join(random.choice(letters + digitos) for i in range(10)) )
    with open("/home/teo/codigo_Antigo/Grafo_gojs/nwjs-v0.74.0-linux-x64/www/JSON/dialogs/"+ nome + '.json', 'w', encoding='utf-8') as f:
        json.dump( data_Dialog, f, ensure_ascii=False, indent=4)
    
#Função para criação do json de script
def jsonScript(nome, conteudo):
    
    sUid = "258a67a1-c7ad-4988-a2da-19255d47ff9c"
    sApp = "4141dd46-718d-46ef-ace1-ca647bf736b5"

    data_Script ={
        'uid' : sUid,
        'applicationUid' : sApp,
        'name' : nome,
        'content': conteudo
    }
    
    with open("/home/teo/codigo_Antigo/Grafo_gojs/nwjs-v0.74.0-linux-x64/www/JSON/scripts/"+ str(nome) + '.json', 'w', encoding='utf-8') as f:
        json.dump(data_Script  , f, ensure_ascii=False, indent=4)

#Função responsavel por alocar os valores do script no construtor
def procScript(list,links,lista_nomes):
    
    #Coloca os valores no nó (nome,conteudo, link)
    keys,values = zip(*list.items())
    obj = script(values[1],values[3])    
    #por enquanto o link tera valor vazio
    obj.link("")
    
    #Laço responsavel por verificar se há uma chamada a um script
    for l in links:
        k,v = zip(*l.items())
        #Se não houver "to" e "from" é um link colocado errado, portanto ignoramos
        if(len(l) != 2):
            break
        if(v[0] == values[1]):
            if(v[1] in lista_nomes):
                obj.link(v[1])
    
    jsonScript(values[1],values[3])
    
#Função responsavel por alocar os valors dos dialogos no construtor
def procDialogo(list,links):
    
    keys,values = zip(*list.items())
    obj = dialogo(values[1])
    
    #Laço que verifica se há ou não inputs e outputs
    #Se houver aloca os valores deles no construtor
    c = 0
    inputs = ""
    outputs = ""
    linkIn = ""
    linkOut = ""
    
    for k in keys:
        if (k == "input"):
            obj.setInput(values[c])
            inputs = values[c]
        if (k == "output"):
            obj.setOutput(values[c])
            outputs = values[c]
        c = c + 1

    for l in links:
        k,v = zip(*l.items())
        if(values[1] == v[0]):
            obj.linkOut(v[1])
            linkIn = v[1]
        if(values[1] == v[1]):
            obj.linkIn(v[1])
            linkOut = v[1]
            
    jsonDialogo(inputs,outputs,linkIn,linkOut)

win=Tk()
win.geometry("450x200")

Label(win, text="Clique o botão e escolha o(s) arquivo(s)", font='Arial 16 bold').pack(pady=15)

def open_file():
    filepath = filedialog.askopenfilename(title="Pesquisar", filetypes=(("all files","*.*"), ("text    files","*.txt")))
    f = open(filepath,'r')
    k = 0
    data = json.load(f)

    #Guarda o nome dos scripts
    nome_scripts= []

    #Salva os dados referentes a links
    links = data['linkDataArray']

    #Salva em uma lista o nome de todos scripts
    for i in data['nodeDataArray']:
        keys,values = zip(*i.items())
        if(values[0] == "Script"):
            nome_scripts.append(values[1])

    #Separa aqueles que são script e aqueles que são dialogo
    for j in data['nodeDataArray']:        
        keys,values = zip(*j.items())
        if(values[0] == "Script"):
            procScript(j,links,nome_scripts)
        if(values[0] == "Dialogo"):
            procDialogo(j,links)
    f.close()

button = Button(win, text="Open", command=open_file)
button.pack()

win.mainloop()

