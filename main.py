from typing import List

from injector import Injector

from app.config import DataModule, UseCaseModule,  DomainModule, InfraModule
from app.entrypoint.operator import BaseController, ClusterRuleController


def register_controllers(controllers: List[BaseController]):
    for controller in controllers:
        controller.register()


injector = Injector([
    UseCaseModule(),
    DataModule(),
    DomainModule(),
    InfraModule()
])

if __name__ == "main":
    all_controllers: List[BaseController] = [
        injector.get(ClusterRuleController),
    ]
    register_controllers(all_controllers)
