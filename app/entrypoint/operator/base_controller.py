from typing import Callable


class BaseController:

    def register(self):
        raise Exception("Not implemented")

    def register_method(self, handler_type: Callable, method: Callable, kind: str,
                        group: str = 'enforcement.globo.com', version: str = 'v1beta1', **kwargs):
        decorate = handler_type(group, version, kind, **kwargs)
        decorate(method)
