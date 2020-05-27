import vk_api
import time
import codecs


if __name__ == '__main__':
    # Заходим ВКонтакте под своим логином
    vk_session = vk_api.VkApi('', '')
    vk_session.auth()
    vk = vk_session.get_api()

    # Пишем возраст от и до людей которых надо спарсить
    age = 14
    age_max = 100

    # Номер города
    city_number = 7279

    # 1 - девушки, 2 - парни
    gender = 2

    # Открываем файл для записи результатов
    ff = codecs.open('mans.txt', 'w', encoding='utf8')

    # Перебор возрастов
    while age <= age_max:
        month = 1
        # Перебор месяцев рождения
        while month <= 12:
            # Пауза для API
            time.sleep(4)
            # Пишем какую группу людей качаем
            print(str(age) + ' лет, родилась в ' + str(month))
            # Получаем 1000 юзеров - их ФИО, айди, и фотку
            z = vk.users.search(count=1000,
                                fields='id',
                                city=city_number,
                                sex=gender,
                                age_from=age,
                                age_to=age,
                                birth_month=month)
            month = month + 1
            print('Количество: ' + str(z['count']))
            for x in z['items']:
                s = str(x['id'])+'\n'
                ff.write(s)
        age = age + 1

    ff.close()
    print('Done!')
