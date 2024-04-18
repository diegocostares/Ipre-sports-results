# Ipre de deep learning aplicado a la predicción de resultados deportivos

Investigación en pregrado (Ipre) de deep learning aplicado a la predicción de resultados deportivos

## Requisitos

- Python >= 3.12

### Linter y Formatter

Para mantener la consistencia en el código y respetar el pep8, hay que instalar globalmente:

```shell
pip install ruff
pip install black
```

### Dependencias

Para listar las dependencias del proyecto usaremos [poetry](https://python-poetry.org/docs/).

Para configurar el proyecto, ejecuta:

```shell
poetry install
```

Para agregar nuevas dependencias, utiliza:

```shell
poetry add <nombre-del-paquete>
```

Y para actualizar las dependencias existentes:

```shell
poetry update
```

## Ejecutar scrapers

Para ejecutar los proyectos con scrapy ejecutar:

```shell
poetry run playwright install chromium
```

Ejecutar araña y obtener un csv con los datos:

```shell
poetry run scrapy crawl football_manager -o database/raw/football_manager.csv
```

