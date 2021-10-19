extractors = {}
transformers = {}
loaders = {}

flows__registry = {}


def _timer():
    raise NotImplemented


def _register(flow, cls):
    if not hasattr(cls, 'flow'):
        raise KeyError(f'{flow} class must implement the flow name parameter')
    registry = globals()[flow]
    registry[cls.flow] = cls
    flows__registry[cls.flow] = _timer()  # TODO: JOBS TIMER CONFIGURATION, NEEDS SETTINGS UP
    return cls


def extractor(cls):
    return _register('extractors', cls)


def transformer(cls, ):
    return _register('transformers', cls, )


def loader(cls, ):
    return _register('loaders', cls, )


def load_cls(flow, cls_type):
    registry = globals()[cls_type]
    if flow not in registry:
        raise KeyError(f'the flow {flow} was not found on the {cls_type} registry, '
                       f'have you decorated the class with the register_{cls_type} decorator?')

    return registry[flow]
