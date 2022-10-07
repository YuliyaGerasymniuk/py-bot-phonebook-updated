from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phones=None):
        self.name = Name(name)
        self.phones = phones

    def __str__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phones])}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def del_phone(self, new_phone) -> bool:
        for phone in self.phones:
            if phone.value == new_phone:
                self.phones.remove(phone)
                return True

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)
                return True


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            print("Repeat and enter correct user name and phone")
        else:
            return result
    return wrapper


def greeting():
    return 'Hello! Can I help you?'


@input_error
def add(contacts, *args):
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in contacts:
        contacts[name.value].add_phone(phone)
        return f'Add phone {phone} to user {name}'
    else:
        contacts[name.value] = Record(name, [phone])
        return f'Add user {name} with phone number {phone}'


@input_error
def change(contacts, *args):
    name, old_phone, new_phone = args[0], args[1], args[2]
    contacts[name].edit_phone(old_phone), new_phone
    return f'Change {name} phone number from {old_phone} to {new_phone}'


@input_error
def phone(contacts, *args):
    name = args[0]
    phone = contacts[name]
    return f'{phone}'


@input_error
def del_phone(contacts, *args):
    name, phone = args[0], args[1]
    contacts[name].del_phone(phone)
    return f'Delete phone {phone} from user {name}'


def show_all(contacts):
    result = 'List of all users:'
    for key in contacts:
        result += f'\n{contacts[key]}'
    return result


def exiting():
    return 'Good bye!'


def unknown_command():
    return 'Unknown command! Enter again!'


COMMANDS = {greeting: ['hello'],
            add: ['add '],
            change: ['change '],
            phone: ['phone '],
            show_all: ['show all'],
            exiting: ['good bye', 'close', 'exit', '.'],
            del_phone: ['del ']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    contacts = AddressBook()
    while True:
        user_command = input('Enter command >>> ')
        command, data = command_parser(user_command)
        print(command(contacts, *data))
        if command is exiting:
            break


if __name__ == '__main__':
    main()
