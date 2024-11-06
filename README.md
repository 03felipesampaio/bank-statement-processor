# bank-statement-processor


## O que é?

Você entra com o arquivo PDF da sua fatura ou o arquivo OFX do seu extrato e nós devolvemos um arquivo no seu formato favorito com todas informacões extraídas.

Se você é cliente do Nubank ou Banco Inter, provavelmente já reparou que quando sua fatura do cartão de crédito fecha, seu banco envia um e-mail com um PDF anexado. O arquivo PDF descreve todas suas compras desde a abertura ao fechamento da fatura. Mas o formato do arquivo não é facil de manipular e extrair informacões. Esse app foi criado para facilitar a extracao de informacões desses documentos no formato de sua preferência.

![Arquitetura](/docs/imgs/parse-statement.svg "Desenho da arquitetura")

## Como usar?

### Pelo site

A forma mais fácil de usar é através do nosso site, disponível no link https://statement-reader-131357556933.southamerica-east1.run.app/

Para enviar seu arquivo siga esses passos:

1. Selecione o banco ao qual o arquivo pertence.
2. Defina se o arquivo é uma fatura ou um extrato no campo 'Tipo de arquivo'.
3. Selecione o tipo de arquivo que você deseja receber de volta.
4. Clique no botão de pesquisa e selecione o arquivo que deseja extrair as informacões.
5. Clique em enviar.  
6. Verifique se houve o download do arquivo de output

### Pela API

Consulte a aba /docs no site. Os endpoints e seus parâmetros estão descritos.

https://statement-reader-131357556933.southamerica-east1.run.app/docs   

### Instalando localmente

#### Docker

Para executar a aplicacão em um container, siga esses comandos:

```bash

docker build -t statement_reader . && docker run -dp 127.0.0.1:8000:8000 statement_reader
```

#### Python

Versão usada no desenvolvimento: python3.12

```bash
# Cria um ambiente virtual
python -m venv venv

# Linux - Ativa o ambiente virtual
source ./venv/bin/activate

python main.py

```

Depois disso o programa vai estar disponível no endereco http://127.0.0.1:8000 

## Como contactar o desenvolvedor?


## Como contribuir?