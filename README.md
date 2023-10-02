
## Como rodar:
Nessa versão da aplicação pecisamos primeiro colocar todos arquivos dentro de uma mesma pasta. 

E então abrir o arquivo index.html utilizando algum navegador(firefox, chrome). 

## Salvamento e Parser:
O grafo pode ser salvo em um formato gerado pelo Go.js que não é aceito pela HumanRobotics.

Por isso foi feito um "parser" que converte os dados JSON no formato da plataforma da HumanRobotics.

O parser atualmente é feito por um script em python e precisa ser rodado a parte.

Atualmente é preciso copiar e colar para dar load no JSON do Go.js

## Funcionamento do nó de script
Aqui vão alguns comando em relação a criação de scripts: 

Esses comandos devem ser iniciados no começo de qualquer script.

Gerar um link de um script para outro automaticamente chama uma função de "incluir script".

speak: =      -> Corresponde ao "Falar", gera uma fala do robô.

wait:;       -> Corresponde ao "Espera". 

listen:;     -> Corresponde ao "Escutar". 

;            -> Passa para o próximo bloco dentro do script.

Exemplo:

voice: Olá #{nome}, eu sou Robios!;

listen;

## Funcionamento do nó de Diálogo
Basta adicionar os textos em relação a inputs do lado esquerdo e outputs do direito.
Atualmente o parser entende somente uma entrada de output e action.

;            -> Passa para ou o próximo "input"
OBS: ; 
