
import requests, bs4
import sqlite3
import re
import time

f=open(u'adresa.txt', 'w', encoding="UTF-8")


flag1=1
flag2=1
while(flag1<100):
    flag2=1
    while(flag2<50):
        s=requests.get('http://spra.vkaru.net/peoples/7/7152/list'+str(flag1)+'_'+str(flag2)+'/')
        print('http://spra.vkaru.net/peoples/7/7152/list'+str(flag1)+'_'+str(flag2)+'/')
        b=bs4.BeautifulSoup(s.text, "html.parser")
        p=b.select('.main-block1 tr')
        for x in p:        
            s=(x.getText().strip())
            f.write(s+'/n')
        flag2=flag2+1
    flag1=flag1+1



f.close()

print('DONE')
        
