# src/di/dependency_injector.py
from injector import Injector
from src.di.repository_module import RepositoryModule
from src.di.service_module import ServiceModule
from src.di.schema_module import SchemaModule

def setup_injector() -> Injector:
    return Injector([RepositoryModule, ServiceModule, SchemaModule])
