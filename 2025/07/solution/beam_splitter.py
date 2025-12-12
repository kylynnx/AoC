class BeamSplitter:
    def __init__(self):
        self._is_active = False

    @property
    def is_active(self):
        return self._is_active

    def activate(self):
        self._is_active = True
