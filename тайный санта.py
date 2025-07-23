# Скрипт для генерации "тайного санты". Если на новый год вам надо выбрать рандомные пары
# которые будут дарить друг другу подарки, то этот скрипт для вас!

import random
import pprint

def generator():
    print('Составим список работников. Введите имена, затем напишите "все"')
    while True:
        all_persons = []
        while True:
            person = input('Имя работника: ').strip()
            if person.lower() == 'все':
                break
            elif person:
                all_persons.append(person)
        if len(all_persons) >= 2 and len(all_persons) % 2 == 0:
            return all_persons
        else:
            print('Ошибка: нужно ввести как минимум двоих работников и их количество должно быть четным. Пожалуйста, начните заново.')
    
def gener_dict(all_persons):
    shuffled = all_persons.copy()
    random.shuffle(shuffled)
    return {shuffled[i]: shuffled[i+1] for i in range(0, len(shuffled), 2)}

workers = generator()
result = gener_dict(workers)
pprint.pprint(result)