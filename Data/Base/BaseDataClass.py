class BaseDataProcess:
    flow = None

    def __init__(self):
        if not self.flow:
            raise NotImplementedError('the flow class attribute must be implemented')
