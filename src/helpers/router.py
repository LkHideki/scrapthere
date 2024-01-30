from fastapi import APIRouter
from helpers.drive import Driver

router = APIRouter(prefix="/api")


"""Exemplo de uso
@router.get("/")
def hello_world():
    res = []
    with Driver("chrome", "https://www.selenium.dev/documentation/") as driver:
        driver.wait_for("p")
        driver.cook_a_soup()
        res = driver.select_from_soup("ul.ul-1 a span")

    return [x.text for x in res]
"""
