# Scrap there!

Conjunto de módulos que permite scrap e exposição das informações numa api.

Contém dois módulos:
- *drive.py*: tem a classe Driver que faz o handle do navegador.
- *router.py*: tem as rotas (a partir) de /api/*.

O *main.py* usa a `uvicorn` que é um servidor para rodar a api.

Ative o seu *ambiente virtual* e rode `pip install -r requirements.txt` para instalar tudo o que precisa.

## Módulo Driver
Contém a classe `Driver` que é usada para interagir com páginas da web usando o Selenium WebDriver.

### Dependências

Este módulo depende das seguintes bibliotecas:

- `time`
- `typing`
- `selenium`
- `bs4`

### Uso

Para usar este módulo, você precisa instanciar a classe `Driver` (sugiro que use o gerenciador de contexto do python `with` para não esquecer de sair do objeto webdriver).

A classe `Driver` tem uma constante `KEYS` que representa as teclas do teclado.

```python
from drive import Driver

with Driver("firefox", "https://www.selenium.dev/", headless=True, incognito=True) as driver:
  driver.wait_for("p")
  driver.cook_a_soup()
  res = driver.select_from_soup("span")
```

Explicação:
1. `Driver("firefox", "https://www.selenium.dev/", headless=True, incognito=True)` instancia o firefox do webdriver do selenium acessando a url fornecida sem exibir a interface gráfica (headless) e no modo "anônimo" (incognito).
2. `driver.wait_for("p")` aguarda que exista uma tag p renderizada na página.
3. `driver.cook_a_soup()` faz o parse do html para um objeto BeautifulSoup guardado no atributo .soup.
4. `res = driver.select_from_soup("span")` nesse objeto BeautifulSoup (do .soup) o script procura as tags com seletor css "span" e guarda a lista resultante na variável `res`.

## Módulo Router

É onde ficam as lógicas das rotas e onde se pode usar o Driver (ou qualquer outro recurso).

### Dependência

- `fastapi`
- `uvicorn` (que será usado na *main.py*)

### Uso

Declare as rotas e suas lógicas de funcionamento.


### Exemplo

Você só precisa implementar rotas no módulo *router.py*.

Um exemplo pode ser

```python
@router.get("/")
def hello_world():
    res = []
    with Driver("safari", "https://www.selenium.dev/documentation/", True, True) as driver:
        driver.wait_for("p")
        driver.cook_a_soup()
        res = driver.select_from_soup("ul.ul-1 a span")

    return [x.text for x in res]
```

Assim, ao enviar uma requisição `GET` para `http://localhost:8000/api/`, obteremos uma lista dos conteúdos das tags span dentro de anchor dentro de uma lista ul.

