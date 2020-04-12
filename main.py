from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ
# срежем шапку, чтоб не мешалась:
header = contacts_list[0]
contacts_list.remove(contacts_list[0])

# разносим ФИО по полям [0], [1], [2]:
for contact in contacts_list:
  lastname_list = contact[0].split(' ')
  if len(lastname_list) > 1:
    if len(lastname_list) > 2:
      contact[0] = lastname_list[0]
      contact[1] = lastname_list[1]
      contact[2] = lastname_list[2]
    else:
      contact[0] = lastname_list[0]
      contact[1] = lastname_list[1]
  firstname_list = contact[1].split(' ')
  if len(firstname_list) > 1:
    contact[1] = firstname_list[0]
    contact[2] = firstname_list[1]

# приводим телефоны в заданный формат:
phone_pattern = "(\+7|8)(\s\(|\s|\(|)(\d{3})(\)\s|\-|\)|)(\d{3})(\-|)(\d{2})(\-|)(\d{2})(\s\(|\s|)(\w{3}.|)(\s|)(\d{4}|)(\)|)"
for contact in contacts_list:
  result = re.sub(phone_pattern, r'+7(\3)\5-\7-\9 \11\13', contact[5])
  contact[5] = result.strip()

# принимаем, что в телефонной книге нет однофамильцев
lastname_list = []
repeat_lastname_set = set()
for contact in contacts_list:
  lastname_list.append(contact[0])
  if lastname_list.count(contact[0]) > 1:
    repeat_lastname_set.add(contact[0])

# повторы удаляем из основного списка, выносим их в отдельный список и работаем с ним
repeat_list = []
i = 0
while i < len(contacts_list):
  if contacts_list[i][0] not in repeat_lastname_set:
    i += 1
  else:
    repeat_list.append(contacts_list[i])
    contacts_list.remove(contacts_list[i])

# здесь объединяем соответствующие поля повторяющихся списков:
i = 0
while i < len(repeat_list):
  k = i + 1
  if repeat_list[k][0] != repeat_list[i][0]:
    k += 1
  else:
    for field in range(len(repeat_list[i])):
      if repeat_list[i][field] == '':
        repeat_list[i][field] = repeat_list[k][field]
    repeat_list.remove(repeat_list[k])
  i += 1

contacts_list.extend(repeat_list)
contacts_list.sort()
contacts_list.insert(0, header)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
new_phonebook = "phonebook.csv"
with open(new_phonebook, "w", newline='', encoding='utf-8') as f:
   datawriter = csv.writer(f, delimiter=',')
   # Вместо contacts_list подставьте свой список
   datawriter.writerows(contacts_list)
print(f'Обновленная книга контактов создана в файле {new_phonebook}')