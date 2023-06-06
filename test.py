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

#Caso em que os outputs são maiores ou iguais as actions
def geraOutputCasoA(outp,linkOut):
    #{"output":"teste","actions":"script:script1","emotions":"","parameters":[]}
    outputCompleto = []    
    if len(linkOut) == 0:
        for o in outp:
            outputCompleto.append('{"output":' + o + ',"actions":"script:"'+ '""' + ',"emotions":"","parameters:[]}')
    else:
        valor = 1
        for o in outp:
            if len(linkOut) >= valor:
                outputCompleto.append('{"output":' + o + ',"actions":"script:"'+ linkOut[valor - 1] + ',"emotions":"","parameters:[]}')
            else:
                outputCompleto.append('{"output":' + o + ',"actions":"script:"'+ linkOut[0] + ',"emotions":"","parameters:[]}')
            valor = valor + 1
    return outputCompleto
    

def geraOutputCasoB(outp,linkOut):
    #{"output":"teste","actions":"script:script1","emotions":"","parameters":[]}
    outputCompleto = []
    if len(outp) == 0:
        for l in linkOut:
            outputCompleto.append('{"output":' + '""' + ',"actions":"script:"'+ l + ',"emotions":"","parameters:[]}')
    else:
        valor = 1
        for l in linkOut:
            if len(outp) >= valor:
                outputCompleto.append('{"output":' + outp[valor -1] + ',"actions":"script:"'+ l + ',"emotions":"","parameters:[]}')
            else:
                outputCompleto.append('{"output":' + '""' + ',"actions":"script:"'+ l + ',"emotions":"","parameters:[]}')
            valor = valor + 1
    return outputCompleto


dId = "1c232c57-7f59-407c-ae16-08bafaabc1d6"

inpu = []
linkOut = []
outp = []

outp.append("Uma lalartixa dançarovisk")
linkOut.append("Lalartixa")
linkOut.append("Lalartixa1")

linkIn = ""

inpu.append("Teste de texto")
inpu.append("Teste de texto2")

inputCompleto = geraInput(inpu)

if(len(outp) >= len(linkOut) ):
    if(len(outp) == 0):
        outputCompleto = ""
    else:
        outputCompleto = geraOutputCasoA(outp,linkOut)
else:
    outputCompleto = geraOutputCasoB(outp,linkOut)


data_Dialog = {
    'id' : dId ,
    'mode' :"-",
    'inputs' : inputCompleto,
    'outputs': outputCompleto,
    'requires':[],
    'concepts':[{
        'name' :"context:script:" + str(linkIn)
    }],
    'entities' :[{
        'name' :"context:script:" + str(linkIn)
    }]
}

data_Dialog2 = '{"id":' + dId + '", "mode": "-", "inputs":' + str(inputCompleto) + '"outputs:" ' + str(outputCompleto) + ',"requires": [], "concepts": [{"name": "context:' + str(linkIn) + '"}], "entities":[{"name": "context:' + str(linkIn) + '"}]}' 

y = json.dumps(data_Dialog2).replace("\\", "")
print(y)