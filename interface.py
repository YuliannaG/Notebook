from abc import ABC, abstractmethod


class Creator(ABC):
    @abstractmethod
    def create(self):
        pass

    def output_data(self) -> str:
        data = self.create()
        result = data.output()
        return result


class OutputData(ABC):
    @abstractmethod
    def output(self) -> str:
        pass


class CreatorWeb(Creator):
    def create(self) -> OutputData:
        '''обработка строки в красивый вид'''
        return OutputDataWeb()


class CreatorConsole(Creator):
    def create(self) -> OutputData:
        '''не надо обработки строки в красивый вид, вывод как есть'''
        return OutputDataConsole()


class OutputDataWeb(OutputData):
    def output(self) -> str:
        '''механизм вывода в веб'''
        return "Выполнен вывод в веб"


class OutputDataConsole(OutputData):
    def output(self) -> str:
        ''' простой вывод в консоль, вместо принт в основном коде'''
        return "Выполнен вывод в консоль"


def output_code(creator: Creator) -> None:
    result = creator.output_data()
    print(f"Результат: {result}")


if __name__ == "__main__":
    output_code(CreatorConsole())
    output_code(CreatorWeb())






