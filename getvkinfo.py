import vk_api, time
import sqlite3
from progress.bar import IncrementalBar
vk_session = vk_api.VkApi(token='')
vk = vk_session.get_api()

scount=sum(1 for l in open('itogo.log', 'r', encoding='UTF-8'))
bar = IncrementalBar('Countdown', max = scount)

conn = sqlite3.connect('vkusers.sqlite')
cursor = conn.cursor()

conn2 = sqlite3.connect('vkuserserror.sqlite')
cursor2 = conn2.cursor()

# Создаём файл базы данных, если его еще нет
try:
    cursor.execute('''CREATE TABLE IF NOT EXISTS vkusers (vkid text, firstname text, lastname text, nick text, birthday text, city text, photo longtext, phone text, work text, partner text, relation text, relatives longtext)''')
except:
    pass

# Создаём файл базы данных, если его еще нет
try:
    cursor2.execute('''CREATE TABLE IF NOT EXISTS vkuserserror (vkid text)''')
except:
    pass

def getprofileinfo(prid):
    vkid=prid
    global cursor
    global conn
    global cursor2
    global conn2
    firstname=''
    lastname=''
    nick=''
    birthday=''
    city=''
    photo=''
    phone=''
    work=''
    partner=''
    relation=''
    relatives=''
    cursor.execute('SELECT vkid FROM vkusers WHERE vkid = ?', (vkid,))
    row = cursor.fetchone()
    cursor2.execute('SELECT vkid FROM vkuserserror WHERE vkid = ?', (vkid,))
    row2 = cursor.fetchone()
    if row is None and row2 is None:
        try:
            profiles = vk.users.get(user_id=prid, fields = "photo_max_orig, domain, bdate, city, contacts, exports, occupation, relation, relatives")
        except:
            print('ERROR VK')
            cursor2.execute('INSERT INTO vkuserserror (vkid) VALUES (?)', (vkid,))
            conn2.commit()
            return ''
        if('first_name' in profiles[0]):
            firstname=profiles[0]['first_name']
        if('last_name' in profiles[0]):
            lastname=profiles[0]['last_name']
        if('domain' in profiles[0]):
            nick=profiles[0]['domain']
        if('bdate' in profiles[0]):
            birthday=profiles[0]['bdate']
        if('city' in profiles[0]):
            city=profiles[0]['city']['title']
        if('photo_max_orig' in profiles[0]):
            photo=profiles[0]['photo_max_orig']
        if('mobile_phone' in profiles[0] and profiles[0]['mobile_phone']!=''):
            phone=profiles[0]['mobile_phone']
        if('occupation' in profiles[0]):
            work='Род занятий: '+profiles[0]['occupation']['type']+' в '+ profiles[0]['occupation']['name']
        if('relation_partner' in profiles[0]):
            partner='https://vk.com/id'+str(profiles[0]['relation_partner']['id'])
        if('relation' in profiles[0]):
            relation=str(profiles[0]['relation'])
        if('relatives' in profiles[0]):
            for x in profiles[0]['relatives']:
                relatives=relatives+'Родственник: https://vk.com/id'+str(x['id']) + ' (' + str(x['type'])+')\n'
        try:
            cursor.execute('INSERT INTO vkusers (vkid, firstname, lastname, nick, birthday, city, photo, phone, work, partner, relation, relatives) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (vkid, firstname, lastname, nick, birthday, city, photo, phone, work, partner, relation, relatives))
            conn.commit()
            time.sleep(1)
        except:
            cursor2.execute('INSERT INTO vkuserserror (vkid) VALUES (?)', (vkid,))
            conn2.commit()
            print('Error DB')
            return ''


f=open('itogo.log', 'r')
flag=1
for x in f:
    s=x.strip()
    getprofileinfo(s)
    flag=flag+1
    bar.next()

bar.finish()
f.close()

cursor.close()
conn.close()

cursor2.close()
conn2.close()
                                        


