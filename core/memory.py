class Memory:
    def __init__(self):
        self.store = {}

    def write(self, k, v):
        self.store[k] = v

    def read(self, k):
        return self.store.get(k)
