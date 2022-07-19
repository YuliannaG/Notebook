from abc import ABC, abstractmethod


class AbstractOutput (ABC):
    def print_result(self):
        pass


class NotesOutput(AbstractOutput):
    def __init__(self, data):
        self.data = data

    def print_result(self):
        print(self.data)


class AddressOutput(AbstractOutput):
    def __init__(self, data):
        self.data = data

    def print_result(self):
        print(self.data)






