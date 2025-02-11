from setuptools import setup, find_packages

setup(
    name="lang-portal-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "aiosqlite",
        "pytest",
        "pytest-asyncio",
        "httpx"
    ],
)
