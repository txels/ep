from ..main import EP


class MockEP(EP):
    def __init__(self):
        self.calls = []

    def shell(self, **kwargs):
        self.calls.append(('shell', kwargs))

    def run(self):
        self.calls.append(('run', {}))
