import os
import re
from t0mm0.common.net import Net
import stripe
net = Net()

PATH2=os.path.join('C:/Users/Mike/Desktop','TEST')

#xunitytalk-playlist-directory
#PATH2='C:/Users/Mike/Desktop/script.icechannel.extn.extra.uk/plugins/livetv_uk'


def FOLDER(filename):
    #tt= PATH+'/'+filename   
    #a=open(tt).read()

    a=open(filename).read()
    uniques=[]
    match=re.compile('msgid ".+?OLOR(.+?)\].+?"\nmsgstr ".+?OLOR(.+?)\].+?"',re.IGNORECASE).findall(a)
    for original , trans in match:
        print original
        print trans

    #f = open(bb, mode='w')
    #f.write(a.replace('script.icechannel.extn.xunitytalk','script.icechannel.extn.extra.uk'))
    #f.close()

def start():
    for root, dirs, files in os.walk(PATH2):
       for f in files:
            print os.path.join(root, f)
            FOLDER(os.path.join(root, f))
start()    
print 'FINISHED'


    #if '<!--Basic-->' in a:
        #print filename    
        #f = open(tt, mode='w')
        #f.write(a.replace('<!--Basic-->','<!--XunityChronos-->'))
       # f.close()
