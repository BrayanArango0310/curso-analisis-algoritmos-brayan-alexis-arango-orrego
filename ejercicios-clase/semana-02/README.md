# Semana 02 — Configuración del entorno de trabajo

## Entorno virtual

Para crear el entorno virtual (una sola vez, desde la raíz del repositorio), use:

    python -m venv venv

Para activarlo en Windows (PowerShell), use:

    .\venv\Scripts\Activate.ps1

## Reproducir el entorno

Con el entorno activado, instale todas las dependencias exactas registradas en requirements.txt (ubicado en la raíz del repositorio):

    pip install -r requirements.txt

Esto instalará matplotlib y sus dependencias en las mismas versiones con las que se desarrolló este laboratorio.

## Archivos de esta semana

- refactor_pep8.py: script refactorizado aplicando PEP 8 y type hints.
- clasificador_anios.py: ejercicio integrador, clasificador de años bisiestos.