from collections import UserDict, UserList, OrderedDict
import shelve
from interface import *


class Note:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class Tag:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class NoteRecord(UserDict):
    def __init__(self, note: Note, tag: Tag = None):
        self.note = note
        self.tags = []
        if tag:
            self.tags.append(tag)

    def __repr__(self):
        if len(self.tags) > 0:
            return f'Tags: {[t.value for t in self.tags]}\n{self.note.value}'
        return f'{self.note.value}'

    def add_tag(self):
        while True:
            tag_input = input('Please, add tag name or skip:')
            if not tag_input:
                break
            my_tag = Tag(tag_input)
            if my_tag.value not in [t.value for t in self.tags]:
                self.tags.append(my_tag)
        return self.tags


class Notebook(UserDict):
    
    def __init__(self):
        self.data = {}
    
    def __repr__(self):
        return f'{self.data}'

    def add_note(self, note: Note):
        my_note = Note(note)
        rec = NoteRecord(my_note)
        self.data[my_note.value] = rec.tags
        return rec.add_tag()

    def delete_note(self, note: Note):
        for k, v in self.data.items():
            #if isinstance(note, NoteRecord):
            if k == note.value:
                deleted_note = k
                self.data.pop(k)
                return deleted_note

    def save_to_file(self):
        with shelve.open(filename) as db:
            db['NoteBook'] = self.data

    def get_tags(self):
        tags_list = []
        for tags in self.values():
            for tag in tags:
                tags_list.append(str(tag))
            tags_set = sorted(set(tags_list), reverse=False)
            return tags_set
        else:
            return None

    def search_by_tag(self, search_word: str):
        search_output = Notebook()
        for note, tags in self.items():
            for t in tags:
                if search_word in str(t):
                    search_output[note] = tags
        return search_output

    def search_in_note(self, search_word: str):
        search_output = Notebook()
        for note, tags in self.items():
            if search_word in str(note):
                search_output[note] = tags
        return search_output

    def save_to_last_search(self):
        global last_search
        last_search = self.data.copy()

    def numbering(self):
        result = ''
        if len(self.data) == 0:
            return "No results"
        for num, (note, tags) in enumerate(self.data.items(), 1):
            result += f'{num} Note: {note}\nTags:{tags}\n'
        return result.strip()


def input_error_note(func):
    def inner(*args):
        try:
            return func(*args)
        # except KeyError:
        #     return 'No records found'
        # except IndexError:
        #     return 'No tags records in the notebook.'
        # except ValueError:
        #     return 'Search the note first.'
        except TypeError:
            return 'Note changed'
    return inner


def load(my_filename):
    try:
        with shelve.open(my_filename) as db:
            notebook.data = db['NoteBook']
    except KeyError:
        with shelve.open(my_filename) as db:
            db['NoteBook'] = notebook


def add_note(note: Note):
    notebook.add_note(note)
    notebook.save_to_file()
    return 'Note added'


@input_error_note
def show_all(*args):
    notebook.save_to_last_search()
    return notebook.numbering()


@input_error_note
def search(search_info):
    if search_info.lower().startswith('by tag'):
        search_tag = search_info[7:].strip()
        search_output = notebook.search_by_tag(search_tag)
    else:
        search_output = notebook.search_by_tag(search_info)
        for k, v in notebook.search_in_note(search_info).items():
            search_output[k] = v
    search_output.save_to_last_search()
    return search_output.numbering()


@input_error_note
def change(my_input):
    global last_search
    if not last_search:
        raise ValueError
    commands = my_input.split(' ')
    num = commands[0]
    new_note = Note(my_input[len(num):].strip())
    if int(num) > 0 and len(new_note.value) > 0:
        counter = 1
        for note, tags in last_search.items():
            if counter == int(num):
                note = Note(note)
                old_tags = tags.copy()
                print(old_tags)
                notebook.delete_note(note)
                notebook.add_note(new_note)
                for t in old_tags:
                    notebook[new_note] = list(set(notebook[new_note].append(t)))
                print(notebook)
            counter += 1
        last_search = {}
        notebook.save_to_file()
        return 'Note changed'
    else:
        return 'Please, enter number of the note you want to change followed by the new note text.'


def bot_help(*args):
    return """
    The following functions are available in the Notebook:
    "add note [note text]" - create a new note with follow up tag request.
    "delete note [number]" - delete note by the number from the previous search results 
    from show all or search function."help" - see all available commands.
    "change note [number] [new note text]" - change note by the number from the previous search results 
    from show all or search function to new note. Tags change will follow.
    "show all" - Show all notes records with tags.
    "tags" - show all saved tags. 
    "search note [text]" - Search notes and tags by text.
    "search note by tag [text]" - Search tags only by text.
    "sort notes" - Sort notes by tags.
    "good bye", "close", "exit" - exit from the bot.
    """


@input_error_note
def delete(del_num):
    global last_search
    if not last_search:
        raise ValueError
    counter = 1
    for k in last_search.keys():
        if counter == int(del_num):
            k = Note(k)
            result = notebook.delete_note(k)
            last_search = {}
            notebook.save_to_file()
            return f'Note: "{result}" deleted.'
        counter += 1


@input_error_note
def show_tags(*args):
    result = notebook.get_tags()
    if result:
        return ','.join(result)
    else:
        raise IndexError


@input_error_note
def sort_notes(*args):
    tags = notebook.get_tags()
    no_tag_list = []
    sort_result = {}
    for t in tags:
        sort_result[t] = []
        for rec in notebook.values():
            if not rec.tags:
                no_tag_list.append(rec.note.value)
            for tag in rec.tags:
                if t == str(tag):
                    sort_result[t].append(rec.note.value)
    sort_result['no tag'] = set(no_tag_list)
    result = ""
    for k, v in sort_result.items():
        result += f'\n{k}:\n'
        for value in v:
            result += f'{value}\n'
    return result.strip()


def func_exit(*args):
    return 'Good bye!'


notebook = Notebook()
filename = 'some_db'
last_search = {}
COMMANDS = {search: ["search note"],
            func_exit: ["good bye", "close", "exit", "."],
            add_note: ["add note"],
            show_all: ["show all"],
            change: ["change note"],
            bot_help: ["help"],
            delete: ["delete note"],
            show_tags: ['tags'],
            sort_notes: ['sort notes']
            }


def parse_command(user_input: str):
    for code_function, input_function in COMMANDS.items():
        for i in input_function:
            if user_input.lower().startswith(i.lower()):
                note = user_input[len(i):].strip()
                return [code_function, note]
    return 'Unknown command'


def main():
    load(filename)
    while True:
        user_input = input("Please, enter command: ")  # add note, search notes
        user_command = parse_command(user_input)
        if user_command == 'Unknown command':
            continue
        result = user_command[0](user_command[1])
        print(result)
        # output_code(CreatorConsole(result))
        # output_code(CreatorWeb(result))
        if result == 'Good bye!':
            break


if __name__ == "__main__":
    # load(filename)
    # print(show_all())
    # print(notebook[0])
    main()
