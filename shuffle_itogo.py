import random
f = open('itogo.log', 'r', encoding='UTF-8')
text = f.readlines()
text[-1]=text[-1]+'\n'
f.close()
random.shuffle(text)
text[-1]=text[-1].replace('\n','')
f = open('itogo.log', 'w', encoding='UTF-8')
f.writelines(text)
f.close()
