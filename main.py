
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

def import_phone_list():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def export_phone_list(contacts_list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)

def convert(contacts_list):
    convert_data = []
    for contact in contacts_list:
        if len(convert_data) == 0:
            convert_data.append(contact)
        else:
            #1. поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
            #В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
            full_name = ' '.join(contact[:3]).strip().split(' ')
            for i in range(0, 3):
                if i < len(full_name):
                    contact[i] = full_name[i]
                else:
                    contact[i] = ""

            #2. привести все телефоны в формат +7(999)999-99-99.
            # Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
            phone = re.sub('[^0-9]', '', re.sub('^8', '7', contact[5]))
            if len(phone) == 0:
                contact[5] = ""
            elif len(phone) > 11:
                contact[5] = f'+{phone[:11]} доб.{phone[11:]}'
            else:
                contact[5] = f'+{phone[:11]}'
            convert_data.append(contact)
    return convert_data
# Press the green button in the gutter to run the script.

def get_name(l):
    return f'{l[0]} {l[1]}'

def merge(contacts_list):
    names = []
    merge_list = []
    # 3. объединить все дублирующиеся записи о человеке в одну.
    for c in contacts_list:
        name =  get_name(c)
        if name in names:
            for i, val in enumerate(merge_list):
               if name == get_name(merge_list[i]):
                   for j, val in enumerate(merge_list[i]):
                       if merge_list[i][j] == "":
                           merge_list[i][j] = c[j]
        else:
            names.append(name)
            merge_list.append(c)
    pprint(merge_list)
    return merge_list
if __name__ == '__main__':
    export_phone_list(merge(convert(import_phone_list())))

