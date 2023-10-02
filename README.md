
## Como rodar:
Nessa versão da aplicação pecisamos primeiro colocar todos arquivos dentro de uma mesma pasta. 

E então abrir o arquivo index.html utilizando algum navegador(firefox, chrome). 

A ideia é utilizar o NW.js para rodar a aplicação, contudo, para fins de testes iniciais acredito que assim fique mais facil!

## Salvamento e Parser:
O parser atualmente é feito por um sript em python. Para utilizar o parser é necessario especificar 
os caminhos para as pastas que deseja salvar tanto o script quanto o dialogo

##Comandos dos nós
Esses comandos serão entendidos no momentos de passar os scripts para o formato JSON aceito pela plataforma.

Isso pode e vai ser modificado com o tempo. A legenda contendo as instruções está sendo feita!

## Funcionamento do nó de script
Aqui vão alguns comando em relação a criação de scripts: 

Esses comandos devem ser iniciados no começo de qualquer script.

@voice =      -> Corresponde ao "Falar" 

@wait;       -> Corresponde ao "Espera" 

@listen;     -> Corresponde ao "Escutar" 

;            -> Passa para o próximo bloco dentro do script
OBS: ; será mudado para "enter" / "\n"

Exemplo:

@voice: Olá #{nome}, eu sou Robios!;

@listen;

## Funcionamento do nó de Diálogo
Basta adicionar os textos em relação a inputs do lado esquerdo e outputs do direito

;            -> Passa para ou o próximo "input" ou "output"
OBS: ; será mudado para "enter" / "\n" 
