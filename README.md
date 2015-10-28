# Controle financeiro para Banco Imobiliário

## Introdução

O projeto surgiu de uma brincadeira com minha filha, jogando o famoso Banco Imobiliário (tm) da Estrela.

Em meados da década de 80, para agilizar o jogo com minha turma de amigos, o banqueiro possuía uma planilha em Supercalc 2, rodando num MSX Hotbit. Era uma planilha de conta-corrente com entradas e saídas das transações que aconteciam no jogo.

Com o advento do Super Banco Imobiliário (tm), onde as cédulas foram substituídas por uma máquina de cartões, surgiu a idéia de escrever um commandline em python, usando click e sqlalchemy, para controle das finanças de cada jogador, não gastando tempo com inserções de cartões.

Naturalmente, as crianças vão achar muito mais interessante o trabalho de cartões. O jogo é lúdico e ensina aos pequenos como trabalhar com o dinheiro virtual que temos hoje, bem como introduz o mundo dos negócios de "real state" aos nossos filhos.

## Instalação
```
$ pip install -r requirements.txt
```


## Como rodar

Após a instalação, devemos entrar no diretório bcimob para rodar os comandos

### Iniciando um novo jogo

O comando abaixo iniciará um novo jogo com a quantidade de jogadores especificada no parâmetro [número de jogadores] mais o banqueiro, resetando os valores para os BI$ 25.000,00 regulares.
```
$ ./bcimob.py start_game [número de jogadores] 
```

