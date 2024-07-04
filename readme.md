# Case Seguidores GitHub
> Extrai dados de followers de um determinado usuário github

Utilizando a api rest publica do github, coleta os seguidores de um determinado usuário e, utilizando pyspark, coleta e trata informações sobre os usuários seguidores.
Os tratamentos adicionados são nos seguintes campos:
* Remove o digito `@` do começo do campo `company`, quando presente.
* Modifica o formato de retorno da data do campo `created_at` para uma str de modelo `dd/MM/yyyy`

## Installation
Para uma execução local, assumindo que o python esteja instalando na maquina é necessário apenas instalar as bibliotecas do `requirements.txt`
```sh
pip install -r requirements.txt
```

## Execução
Para a execução local são necessárias 3 `envvars`:
 * SOURCEUSER - Contendo o login do usuário a ser extraido.
 * APIKEY - Contendo sua chave de acesso a api.
 * CSVPATH - Contendo o caminho onde os arquivos .csv serão salvos.

Com as variáveis preenchidas a execução pode ser realizada através do arquivo `ifood_case`.
```sh
python ifood_case.py
```

Um script simples de execução contendo o espaço para as variáveis necessárias foi criado no caminho `run_scripts/localrun.sh`.

Para execução em outros ambientes foi adicionado um dockerfile, a imagem pode ter as variáveis de ambiente injetadas por um orquestrador para execuções recorrentes ou em diferentes usuários.
