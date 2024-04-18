import re
import sys
import time
from datetime import datetime, timedelta, timezone


def abort_conditions(req):
    abort_resource_types = ["image", "font"]
    yield req.resource_type in abort_resource_types
    # yield req.url.startswith("https://www.googletagmanager.com")
    yield req.url.startswith("https://www.google-analytics.com")  # TODO
    yield req.url.startswith("https://connect.facebook.net")
    yield "facebook" in req.url
    # si es que no empieza con https://fminside.net/ o no tiene css en su url ni json o javascript
    yield not req.url.startswith("https://fminside.net/") and not any([ext in req.url for ext in ["css", "json", "js"]])
    # yield "css" in req.url


def should_abort_request(req):
    return any(abort_conditions(req))


async def playwright_save_page(page, name="logs/response.html"):
    body = await page.content()
    with open(name, "wb") as f:
        f.write(body.encode("utf-8"))
    print(f"Página guardada en {name}")


def try_convert(value, conversion_func):
    """
    try_convert('123', int)  # Devuelve 123
    try_convert(None, int)  # Devuelve None
    try_convert('123.45', float)  # Devuelve 123.45
    try_convert('abc', int)  # Devuelve 'abc'
    try_convert('abc', float)  # Devuelve 'abc'
    """
    if value is None:
        return None
    try:
        return conversion_func(value)
    except ValueError:
        return value


def clean_key(key):
    # Reemplaza uno o más espacios, puntos, o tabuladores por un guión bajo
    key = re.sub(r"[.\s\t]+", "_", key)
    # Elimina cualquier carácter que no sea alfanumérico o guión bajo
    key = re.sub(r"[^a-zA-Z0-9_]", "", key)
    # Reduce múltiples guiones bajos a un solo guión bajo
    key = re.sub(r"_{2,}", "_", key)
    return key.lower()
