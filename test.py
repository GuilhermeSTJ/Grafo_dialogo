import json

def geraInput(inpu):
    inputCompleto = ""
    if len(inpu) == 1:
        inputCompleto = ('[{"input":' + inpu + '}]')
    else:
        inputCompleto = []
        for i in inpu:
            inputCompleto.append('{"input":' + i + '}')
    return inputCompleto

def geraOutput(out):
    outputCompleto = ""
    if len(out) == 1:
        outputCompleto = ('{"output"}')

dId = "1c232c57-7f59-407c-ae16-08bafaabc1d6"

inpu = []
out = ""
linkOut = ""
linkIn = ""
linkOut = ""
inpu.append("Teste de texto")
inpu.append("Teste de texto2")

inputCompleto =  geraInput(inpu)

data_Dialog = {
    'id' : dId ,
    'mode' :"-",
    'inputs' : inputCompleto,
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

y = json.dumps(data_Dialog)
print(y)