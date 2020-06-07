import vk_api
import time
import random, codecs, requests
import dlib, os, shutil
import numpy as np
from skimage import io
from scipy.spatial import distance
import sqlite3
from progress.bar import IncrementalBar

# С какого юзера начинать парсинг
previosuserid=0

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()

vk_session = vk_api.VkApi('', '')
vk_session.auth()
vk = vk_session.get_api()

scount=sum(1 for l in open('itogo.log', 'r', encoding='UTF-8')) - previosuserid
bar = IncrementalBar('Users', max = scount) 

f=codecs.open(u'itogo.log', 'r', encoding='utf8')


def getvkava(userid):
    conn = sqlite3.connect('vkusers.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT photo FROM vkusers WHERE vkid = ?', (userid,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is not None:
        return(row[0])
    else:
        return None

def getfacedescriptor(filename):
    try:
        findfaces=0
        img = io.imread(filename)
        dets = detector(img, 1)
        if(dets):
            findfaces=1
        q=0
        for k, d in enumerate(dets):
            shape = sp(img, d)
            try:
                q=q+1
                f = facerec.compute_face_descriptor(img, shape)
                mas = np.array(f)
                filename2=filename.replace('.jpg','')
                fname=filename2.replace('jpg/','npy/')
                np.save(fname, mas)
            except:
                print('Ошибка распознавания лиц в ' + filename)
                return False
        os.remove(filename)
        if(findfaces==1):
            return True
        else:
            return False
    except:
        os.remove(filename)
        return False
        


# Функция для скачивания фото
def loadfile(name,url):
    if not(os.path.exists('jpg/'+str(name)+'.jpg')):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open('jpg/'+str(name)+'.jpg', 'wb') as f:
               r.raw.decode_content = True
               shutil.copyfileobj(r.raw, f)
        return True

def getphotosbyid(userid):
    faceflag=0
    fotki=[]
    vkava=getvkava(str(userid))
    fotki.append(vkava)
    try:
        prev=''
        flag=0
        try:
            z=vk.photos.getAll(owner_id=userid, count=10, no_service_albums=0)

        # Получаем первые 10 ссылок на фотографий
        
            for x in z['items']:
                for t in x['sizes']:
                    s=str(t['url'])
                    mas=s.split('/')
                    ident=mas[4]
                    if(prev!=ident):
                        prev=ident
                        flag=0
                    else:
                        flag=flag+1
                        if(flag==3):
                            fotki.append(s)
        except:
            pass
                       
        # По очереди качаем фото и ищем на них лица
        photonumber=0
        for t in fotki:
            photonumber=photonumber+1
            if loadfile(str(userid)+'_'+str(photonumber),t):
                if getfacedescriptor('jpg/'+str(userid)+'_'+str(photonumber)+'.jpg'):
                    faceflag=1
    except:
        print(str(userid)+' e')
    if(faceflag==1):
        return True
    else:
        return False



z=0
for x in f:
    z=z+1
    if(z<previosuserid):
        continue
    bar.next()
    f2=codecs.open(u'log.log', 'a', encoding='utf8')
    if(getphotosbyid(int(x.strip()))):
        f2.write(x.strip()+' +\n')
    else:
        f2.write(x.strip()+' -\n')
    f2.close()


bar.finish()
f.close()


    


