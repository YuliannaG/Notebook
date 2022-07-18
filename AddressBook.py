import re
from collections import UserDict
from datetime import datetime, timedelta
import shelve


class AddressBook(UserDict):

    def __init__(self):
        self.data = {}
        self.listdata = []

    def show_all(self):
        counter = 0
        for k, v in self.data.items():
            counter += 1
            print(v)
        return f'Database has {counter} profile(s)'

    def add_record(self, record):
        self.data[record.name.value] = record
        self.listdata.append(record)

    def load(self, filename):
        try:
            with shelve.open(filename) as db:
                phone_book.listdata = db['PhoneBook'].listdata
                phone_book.data = db['PhoneBook'].data
        except:
            with shelve.open(filename) as db:
                db['PhoneBook'] = phone_book

    def save_close(self, filename):
        with shelve.open(filename) as db:
            db['PhoneBook'] = phone_book

    def birthday_in_n_days(num_day):
        searched_profiles = []
        num_days = timedelta(days = int(num_day))
        d_now = datetime.now()
        day_end = datetime(day=d_now.day, month=d_now.month, year=d_now.year) + num_days
        for k, v in phone_book.data.items():            
            try:
                m = datetime(day=v.birthday.value.day, month=v.birthday.value.month, year=d_now.year)
            except AttributeError:
                continue
            if day_end == m:
                searched_profiles.append(v.name.value)
        if len(searched_profiles) == 0:
            return f'Nobody in database has birthday at {day_end.strftime("%d %B %Y")}.'
        elif len(searched_profiles) == 1:
            return f'{searched_profiles[0]} has birthday at {day_end.strftime("%d %B %Y")}.'
        else:  
            return f'{", ".join(searched_profiles)} have birthday at {day_end.strftime("%d %B %Y")}.'       


    def search_common(searched_text):
        searched_profiles = []
        for k, v in phone_book.data.items():
                if searched_text.lower() in v.name.value.lower():
                    searched_profiles.append(v.name.value)
        if len(searched_profiles) == 0:
            return f'Anything common haven`t been found in database.'
        if len(searched_profiles) == 1:
            return f'{searched_profiles[0]} has something in common with your search.'
        else:
            return f'{", ".join(searched_profiles)} have something in common with your search.'

    def delete_contact(self, contact_name):
        for k, v in self.data.items():
            if k == contact_name:
                self.data.pop(contact_name)
                return f'Contact {contact_name} deleted from database'
        return f'Contact {contact_name} isn`t exist in database'


    def iterator(self, num):
        counter = 0
        start_counter = counter
        while True:
            temp_list = []
            try:
                while counter < start_counter + num:
                    temp_list.append(self.listdata[counter])
                    counter += 1
            except IndexError:
                yield temp_list
                break
            yield temp_list
            start_counter = counter
            temp_list.clear


class Record:

    def __init__(self, name, phone=None, birthday=None, email=None, home=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.home = home
        if phone != None:
            self.phones.append(phone)

    def change(self, phone1, phone2):
        for i in self.phones:
            if i.value == phone1:
                i.value = phone2
                return f'Number {phone1} from {self.name}`s list changed to {phone2}'
        return f'Number {phone1} is not exist in {self.name} list'

    def delete(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)
                return f'Number {phone} deleted from {self.name}`s number list'
        return f'Number {phone} is not exist in {self.name} list'

    def add_number(self, phone):
        for i in self.phones:
            if i.value == phone.value:
                return f'This number is already in database'
        self.phones.append(phone)

    def days_to_birthday(self):
        if self.birthday == None:
            return f'{self.name.value}`s birth date is not exist in this database.'
        else:
            d_now = datetime.now()
            day_now = datetime(
                day=d_now.day, month=d_now.month, year=d_now.year)
            day_end = datetime(day=self.birthday.value.day,
                               month=self.birthday.value.month, year=d_now.year)
            if day_now < day_end:
                diff = (day_end - day_now).days
                return f'{diff} day(s) to {self.name.value}`s birthday'
            elif day_now > day_end:
                diff = (datetime(day=self.birthday.value.day,
                        month=self.birthday.value.month, year=d_now.year+1) - day_now).days
                return f'{diff} day(s) to {self.name.value}`s birthday'
            elif day_now == day_end:
                return f'Today is {self.name.value}`s birthday'

    def __str__(self) -> str:
        self.phones_show = None
        if len(self.phones) == 0:
            self.phones_show = 'None'
        elif len(self.phones) == 1:
            self.phones_show = str(self.phones[0])
        elif len(self.phones) > 1:
            self.phones2 = [*self.phones]
            self.phones_show = [*self.phones2]
        return f'{self.name.value}`s profile: Phone: {self.phones_show}; Birthday: {self.birthday}; Email: {self.email}; Home address: {self.home}.'

    def __repr__(self) -> str:
        return f'{self.name.value}, {self.phones}, {self.birthday}, {self.email}, {self.home}'


class Field:
    pass


class Name(Field):
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'


class Phone(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        match = re.search(r'\+38\d{10}', value)
        if match:
            self.__value = value
        else:
            raise PhoneError

    def __repr__(self) -> str:
        return f'{self.value}'


class Birthday(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        match = re.search(r'\d{2}\.\d{2}\.\d{4}', value)
        if match:
            d, m, y = value.split('.')
            try:
                self.__value = datetime(day=int(d), month=int(m), year=int(y))
            except ValueError:
                raise ValueError
        else:
            raise DateError

    def __repr__(self) -> str:
        return f'{self.value.strftime("%d %B %Y")}'


class Email(Field):
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        match = re.search(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)", value)
        if match:
            self.__value = value
        else:
            raise EmailError

    def __repr__(self) -> str:
        return f'{self.value}'


class Home(Field):
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

    def __str__(self) -> str:
        return f'{self.value}'


def is_birthday_valid(value):
    searcher = re.findall(r'\d{2}\.\d{2}\.\d{4}', value)
    if value == searcher[0]:
        d, m, y = value.split('.')
        try:
            _ = datetime(day=int(d), month=int(m), year=int(y))
            return True
        except ValueError:
            return False
    else:
        return False


def is_number_valid(value):
    searcher = re.findall(r'\+38\d{10}', str(value))
    if value == searcher[0]:
        return True
    else:
        return False


phone_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except TypeError:
            return 'TypeError! Try to type command again.'
        except IndexError:
            return 'IndexError! Try to type command again.'
        except KeyError:
            return 'KeyError! Try to type command again.'
        except ValueError:
            return 'This date isn`t exsist, type corect date'
        except EmailError:
            return 'Wrong format of email, try again. Exampe of email: "jsmith@example.com".'
        except PhoneError:
            return 'Wrong format of phone, try again. Phone numer should start with "+38" and have 10 numbers after "+38".'
        except DateError:
            return 'Wrong format of date, try again. Data format: "dd.mm.yyyy"'
    return wrapper

### Кастомні помилки

class EmailError(Exception):
    pass
class PhoneError(Exception):
    pass
class DateError(Exception):
    pass


def exit(*args):
    return "Opening main menu"

# Функції


@input_error
def add_contact(*args): # В цій функції можна додати або Ім'я або Ім'я і Номер телефону
    for k, v in phone_book.items():
        if k == args[0]:
            return f'{args[0]} is already in list'
    name = Name(args[0])
    if len(args) == 2:
        phone = Phone(args[1])
    if len(args) == 1:
        rec = Record(name)
    elif len(args) == 2:
        rec = Record(name, phone)
    phone_book.add_record(rec)
    if len(args) == 1:
        return f'Contact {name.value} added successfuly'
    elif len(args) == 2:
        return f'Contact {name.value} added successfuly with number {phone.value}'


# Варіант функції де можна додати або Ім'я або Ім'я і Номер телефону, або Ім'я, Номер телефону і День народження
    # for k, v in phone_book.items():
    #     if k == args[0]:
    #         return f'{args[0]} is already in list'
    # name = Name(args[0])
    # if len(args) == 2:
    #     phone = Phone(args[1])
    # if len(args) == 3:
    #     phone = Phone(args[1])
    #     birthday = Birthday(args[2])
    # if len(args) == 1:
    #     rec = Record(name)
    # elif len(args) == 2:
    #     rec = Record(name, phone)
    # else:
    #     rec = Record(name, phone, birthday)
    # phone_book.add_record(rec)
    # return f'Contact {name.value} added successfuly'

@input_error
def add_number(*args):  # Для add_number потрібно ввести Ім'я і Новий номер, який хочете додати
    rec = phone_book[args[0]]
    new_number = Phone(args[1])
    if rec.add_number(new_number) == None:
        return f'Number {new_number.value} added to {rec.name}`s list of numbers successfuly'
    else:
        return rec.add_number(new_number)


@input_error
# Для add_birthday потрібно ввести Ім'я і Дату народження, яку хочете додати
def add_birthday(*args):
    rec = phone_book[args[0]]
    if rec.birthday != None:
        print(f'This contact already has birthday date it`s {rec.birthday.value.strftime("%d.%m.%Y")}. Print yes if you want to change it into {args[1]}')
        ask_permision = input('>>>')
        if ask_permision.lower().startswith('yes'):
            rec.birthday = Birthday(args[1])
            return f'{rec.name}`s birthday is updated to {rec.birthday.value.strftime("%d.%m.%Y")}'
        else:
            return f'Birthday isn`t updated'
    else:
        rec.birthday = Birthday(args[1])
        return f'Birthday is updated to {rec.birthday.value.strftime("%d.%m.%Y")}'

@input_error
def add_email(*args):
    rec = phone_book[args[0]]
    if rec.email != None:
        print(f'This contact already has email it`s {rec.email}. Print yes if you want to change it into {args[1]}')
        ask_permision = input('>>>')
        if ask_permision.lower().startswith('yes'):
            rec.email = Email(args[1])
            return f'{rec.name}`s email is updated to {rec.email}'
        else:
            return f'Email isn`t updated'
    else:
        rec.email = Email(args[1])
        return f'Email address added successfully!'

@input_error
def add_home(*args):
    rec = phone_book[args[0]]
    if rec.home != None:
        print(f'This contact already has home address it`s {rec.home}. Print yes if you want to change it into {args[1]}')
        ask_permision = input('>>>')
        if ask_permision.lower().startswith('yes'):
            full_home = " ".join(args[1:])
            rec.home = Home(full_home)
            return f'{rec.name}`s home address is updated to {rec.home}'
        else:
            return f'Home address isn`t updated'
    else:    
        full_home = " ".join(args[1:])
        rec.home = Home(full_home)
        return f'Home address added successfully!'

@input_error
def show_all(*args):  # Показує всі контакти
    return phone_book.show_all()

@input_error
def show_num(*args):  # Ітератор
    iter = phone_book.iterator(int(args[0]))
    for i in iter:
        a = i
        for i2 in a:
            print(i2)
    return f'{len(phone_book.listdata)} profile(s) showed'

@input_error
def search_common(*args):  # Функція знаходить схоже в Імені контактів або в номері телефону
    result = AddressBook.search_common(*args)
    return result

@input_error
def show_profile(*args):  # Вивести номер або номери телефону контакту
    rec = phone_book[args[0]]
    return rec

@input_error
def change_phone(*args):  # Для change потрібно ввести Ім'я, Старий номер і Новий номер
    for k, v in phone_book.items():
        if k == args[0]:
            rec = phone_book[args[0]]
            return rec.change(args[1], args[2])
    return f'{args[0]} isn`t exist in list of names'

@input_error
def delete_contact(*args):  # Для delete потрібно ввести Ім'я та Номер який хочете видалити
    func = phone_book.delete_contact(args[0])
    return func

@input_error
def delete_phone(*args):  # Для delete потрібно ввести Ім'я та Номер який хочете видалити
    for k, v in phone_book.items():
        if k == args[0]:
            rec = phone_book[args[0]]
            return rec.delete(args[1])
    return f'{args[0]} isn`t exist in list of names'


@input_error
def birthday_in_n_days(*args):
    result = AddressBook.birthday_in_n_days(args[0])
    return result

@input_error
def days_to_birthday(*args): # Показує скільки днів до дня народження контакта
    for k, v in phone_book.items():
        if k == args[0]:
            rec = phone_book[args[0]]
            return rec.days_to_birthday()
    return f'{args[0]} isn`t exist in list of names'

def bot_help(*args):
    return """
    The following functions are available in the Addressbook:
    "add contact [note name of contact] [phone number]" - create a new contact with one phone number, also you can add profile without phone number;
        *Name of contact shouldn`t consist of any spaces. If you want add contact with more than 1 word use _ except space.
        *This bot get phone number only in +38 format.
    "add phone [name of contact] [phone number]" - you can add more than one phone number to contact;
    "add bitrhday [name of contact] [date of bitrhday in format dd.mm.yyyy]" - you can add birthday to contact, to change contact birthday also use this command;
    "add email [name of contact] [email in format johnsmith@gmail.com/.org/.edu]" - you can add email to contact, to change contact email also use this command;
    "add home [name of contact] [home address]" - you can add home address to contact, to change contact home address also use this command;

    "show all" - this comand show all profiles in database;
    "show profile [name of contact]" - show contact profile;
    "delete contact [name of contact]" - delete contact from datebase;
    "delete phone [name of contact] [phone number]" - delete number from contacts profile;
    "change phone [name of contact] [old phone number] [new phone number]" - change phone number which already in db into new;
    
    "days to birthday [name of contact]" - this command shows how many days to birthday of contact;
    "birthday after [number]" - this command shows who have birthday in number of days from tomorrow;

    "good bye", "close", "exit" - back to main menu.
    """

COMMANDS = {  
    add_contact: ["add contact", "add c"],
    add_number: ["add number", "add n", "add phone", "add p"],
    add_birthday: ["add birthday", "add b"],
    add_email: ["add email", "add e"],
    add_home: ["add home", "add h"],

    show_all: ["show all", "show a"],
    show_num: ["show num", "show n"], # цю функцію можна не описувати
    show_profile: ["show profile", "show p"],
    search_common: ["search common"],

    change_phone: ["c p", "change phone"],

    delete_contact: ["delete contact", "d c"],
    delete_phone: ["delete phone", "d p"],

    birthday_in_n_days:["birthday after", "b a"],
    days_to_birthday: ["days to birthday", "d t b"],

    bot_help: ["help"],
    
    exit: ["good bye", "close", "exit", "."],
}


### Парсер команд

def parse_command(user_input:str):
    for k,v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")
    return 'Unknown command', user_input


def main():
    filename = 'some_db'
    phone_book.load(filename)
    while True:
        user_input = input("Please, enter command: ")
        result, data = parse_command(user_input)
        if result == 'Unknown command':
            print(f'{result}: {data}.\nType help to see list of commands.')
            continue
        print(result(*data))
        if result is exit:
            break
    phone_book.save_close(filename)


if __name__ == "__main__":
    main()
