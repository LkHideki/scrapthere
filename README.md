# Scrap there!

Conjunto de módulos que permitem scrap e exposição das informações em api.

Contém dois módulos:
- *drive.py*: tem a classe Driver que faz o handle do navegador.
- *router.py*: tem as rotas (a partir) de /api/*.

O main.py usa a `uvicorn` que é um servidor para rodar a api.

Ative o seu *ambiente virtual* e rode `pip install -r requirements.txt` para instalar tudo o que precisa.

## Módulo Driver
Contém a classe `Driver` que é usada para interagir com páginas da web usando o Selenium WebDriver.

### Dependências

Este módulo depende das seguintes bibliotecas:

- `time`
- `typing`
- `selenium`

### Uso

Para usar este módulo, você precisa instanciar a classe `Driver` (sugiro que use o gerenciador de contexto do python `with` para não esquecer de sair do objeto webdriver).

A classe `Driver` tem uma constante `KEYS` que representa as teclas do teclado.

```python
from drive import Driver

with Driver(...) as driver:
  ...
```

## Módulo Router

É onde ficam as lógicas das rotas e onde se pode usar o Driver.

### Dependência

- `fastapi`

### Uso

Declare as rotas e suas lógicas de funcionamento.


### Exemplo

Você só precisa implementar rotas no módulo *router.py*.

Um exemplo pode ser

```python
@router.get("/")
def hello_world():
    res = []
    with Driver("chrome", "https://www.selenium.dev/documentation/") as driver:
        driver.wait_for("p")
        driver.cook_a_soup()
        res = driver.select_from_soup("ul.ul-1 a span")

    return [x.text for x in res]
```

Assim, ao enviar uma requisição `GET` para `http://localhost:8000/api/`, obteremos uma lista dos conteúdos das tags span dentro de anchor dentro de uma lista ul.

