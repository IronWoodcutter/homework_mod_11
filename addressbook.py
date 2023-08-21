'''
У цьому домашньому завданні ми:

Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
Додамо функціонал роботи з Birthday у клас Record, а саме функцію days_to_birthday, 
яка повертає кількість днів до наступного дня народження.
Додамо функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
Додамо пагінацію (посторінковий висновок) для AddressBook для ситуацій, 
коли книга дуже велика і треба показати вміст частинами, а не все одразу. 
Реалізуємо це через створення ітератора за записами.
'''


from collections import UserDict
from datetime import datetime, timedelta
import re


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return self.iterator()
    
    def iterator(self, number_records=None):
        keys = list(self.data.keys())
        current_index = 0

        while current_index < len(keys):
            list_to_show = keys[current_index : current_index + number_records]
            yield [(self.data[key]) for key in list_to_show]
            current_index += number_records



class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def del_phone(self, phone):
        self.phones.remove(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        self.phones[self.phones.index(Phone(old_phone))] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now()
            birthday_in_this_year = self.birthday.replace(
                year=current_datetime.year)
            if birthday_in_this_year >= current_datetime:
                days_left = birthday_in_this_year - current_datetime
                return f"{self.name}'s birthday {days_left.days} days away"
            else:
                birthday_in_next_year = birthday_in_this_year + \
                    timedelta(year=1)
                days_left = birthday_in_next_year - current_datetime
                return f"{self.name}'s birthday {days_left.days} days away"

    def __repr__(self):
        return f'{self.name}, phones: {self.phones}, birthday: {self.birthday}'


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __repr__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    def validate_phone_number(phone):
        addon = {9: '+380', 10: '+38', 11: '+3', 12: '+'}
        sanitize_number = re.sub('["(",")","\-", "+", " "]', '', phone)

        if sanitize_number.isdigit():
            digit_count = len(sanitize_number)
            if digit_count >= 9 and digit_count <= 12:
                return addon.get(digit_count) + sanitize_number
            else:
                print('Wrong number of digits')
        else:
            print('Phone number must be numeric!')


class Birthday(Field):
    # 25-07-2023

    def validate_birthday(self):
        try:
            birthday = datetime.strptime(self, "%d-%m-%Y")
        except ValueError:
            print('Wrong date')
        return birthday


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    birthday = Birthday('25-07-2023')
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)

    name1 = Name('Gorg')
    phone1 = Phone('5864259781')
    birthday1 = Birthday('10-10-2015')
    rec1 = Record(name1, phone1, birthday1)
    ab.add_record(rec1)

    rec2 = Record(Name('Olga'), Phone('026856241'), Birthday('01-01-2001'))
    ab.add_record(rec2)




# test
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
    assert ab['Bill'].birthday.value == '25-07-2023'

    print('All Ok)')
