import os
import shutil
import time
#import pandas as pd

#--------------------------------------------------------------------------------------#
def checkSC(Jenk):
    service = os.system('sc query jenkinsslave-D__' + Jenk+' > scSync.txt')
    tempT = open('x.txt','r')
    lines = tempT.readlines()
    for line in lines:
        if 'FAILED' in line:
            return 0
        if 'RUNNING' in line:
            return 1
        if  'STOPPED' in line:
            return 2
def JKP(path):
    os.chdir(path)

    s = os.listdir(path)
    for file in s:
        #print (file)
        if (file == 'jenkins-slave.xml'):
            s1 = open(file,'r')
            lines1 = s1.readlines()
            for line2 in lines1:
                if ('<user>' in line2):
                    f1 = line2.replace('<user>','')
                    f2 = f1.replace('</user>','')
                    f3 = f2.strip()
                    return f3
# --------------------------------------------------------------------------------------#
    return 0
def JKI(path):
    os.chdir(path)

    s = os.listdir(path)
    for file in s:
        if (file == 'jenkins-slave.xml'):
            s1 = open(file, 'r')
            lines1 = s1.readlines()
            for line2 in lines1:
                if ('<user>' in line2):
                    f1 = line2.replace('<user>', '')
                    f2 = f1.replace('</user>', '')
                    f3 = f2.strip()
                    return f3
# --------------------------------------------------------------------------------------#
    return 0
def GER(list):
    flag = 0
    for file in list:
        if ('.GER' in file):
            flag = 1
    if flag == 0:
        return 0
    if flag == 1:
        return 1
def CHECKSERVER(directory):
    try:
        os.chdir(directory)

        return 1
    except:
        return 0
def PING(server):
    temp = os.system('ping '+server)
    return temp
def CHECKMEMORY(direcotry,text):
    os.chdir(direcotry)
    total, used, free = shutil.disk_usage("/")
    print("Total: %d GiB" % (total // (2 ** 30)))
    text.write("\nTotal: %d GiB" % (total // (2 ** 30)))
    print("Used: %d GiB" % (used // (2 ** 30)))
    text.write("\nUsed: %d GiB" % (used // (2 ** 30)))
    x = free // (2 ** 30)
    y = total // (2 ** 30)
    z = y / 10
    print("Free Space: %d GiB" % (free // (2 ** 30)))
    text.write("\nFree Space: %d GiB\n" % (free // (2 ** 30)))
    if z > x :
        return  0
    else:
        return 1
   # dfiC['Space_Left'].append(free // (2 ** 30))
#--------------------------------------------------------------------------------------#
serverDB = open('listserver.txt','r')
newtextfile = open('logs.txt','w')
errorfile = open('Error.txt','w')
Gerfile = open('GERerror.txt','w')
Prod = open('Prodconnect.txt','w')
int = open('Intconnect.txt','w')
list = ['GERerror.txt','Error.txt','logs.txt','MemoryCheck.txt','Intconnect.txt','Prodconnect.txt']
#--------------------------------------------------------------------------------------#
pat  = os.getcwd()
MemoryIssue = open('MemoryCheck.txt','w')
MemoryIssue.write('Machine to clean memory\n--------------------\n\n ')
Gerfile.write('.GER files error \n--------------------\n\n')
Prod.write('Production machine connection\n-------------------------\n')
int.write('Integration machine connection\n-------------------------\n')
lines = serverDB.readlines()
#dfiC = {}
#dfC = ('Server','Production','Integration','.GER','Space_Left')
#df = pd.DataFrame()
#for x in dfC:
 #   dfiC[x] = []
#--------------------------------------------------------------------------------------#
Tservers=[]
Fservers = []
#--------------------------------------------------------------------------------------#
for line in lines:
    temp = line.strip()
    if 'ba' in temp:
        temp = temp+'.gar.corp.intel.com'
    pathG = '\\\\' + temp + '\\c$\\'
    patht = '\\\\' + temp + '\\d$\\'
    sDirectory = CHECKSERVER(patht)
    GDirectory = CHECKSERVER(pathG)
    if (sDirectory == 1):
        Tservers.append(temp)
    if (sDirectory == 0):
        Fservers.append(temp)
    print('finish check :' + temp)

#--------------------------------------------------------------------------------------#
for server in Tservers:
    #dfiC['Server'].append(server)
    print('\n\n'+server+'\n------------------------')
    newtextfile.write('\n\n'+server+'\n------------------------\n')
    flagI = 0
    flagP = 0
    stringpath = '\\\\' + server + '\\d$\\'
    GERcheck = '\\\\' + server + '\\c$\\Users'
    os.chdir(stringpath)
    listT  = os.listdir(stringpath)
    for file in listT:
        if (file == 'jkp'):# 1 value
            flagP = 1
            user = JKP(stringpath+'\\jkp')
            #sc = checkSC()
            if user == 0 :
                #dfiC['Production'].append(user)
                print('Production : file JKP exists , No connect with JNLP\n')
                newtextfile.write('Production : file JKP exists , No connect with JNLP\n')
                Prod.write(server +' : file JKP exists , No connect with JNLP\n')
            else:
                #dfiC['Production'].append(user)
                print('Production: '+ user+'\n')
                newtextfile.write('Production: ' + user + '\n')
                Prod.write(server + ' : ' + user + '\n')
        if (file == 'jki'):# 2 value
            flagI = 1
            user = JKI(stringpath+'\\jki')
            if user == 0 :
                #dfiC['Integration'].append(user)
                print('Integration: file JKI exists , No connect with JNLP\n')
                newtextfile.write('Integration: file JKI exists , No connect with JNLP\n')
                int.write(server + ': file JKI exists , No connect with JNLP\n'  )
            else:
                #dfiC['Integration'].append(user)
                print('Intedgartion: '+ user)
                newtextfile.write('Intedgartion: ' + user+'\n')
                int.write(server + ':' + user+'\n')
    if (flagP == 0):# 1 value
        #dfiC['Production'].append('-')
        print('Production : machine not connected to Production')
        newtextfile.write('Production : machine not connected to jenkins\n')
    if (flagI == 0):# 2 value
        #dfiC['Integration'].append('-')
        print('Integration: machine not connected to Production')
        newtextfile.write('Integration: machine not connected to jenkins\n')
    s = CHECKMEMORY(stringpath,newtextfile)
#--------------------------------------------------------------------------------------#
    if (s == 0):
        MemoryIssue.write(server + ' : need to clean space in D drive.\n')

    try:
        os.chdir(GERcheck)
        listG = os.listdir(GERcheck)
        Ger = GER(listG)
        if Ger == 1:# 3 value
            #dfiC['.GER'].append('YES')
            print('GER file : yes')
            newtextfile.write('\nGER file : yes\n')
            Gerfile.write(server + ' : .GER found in this machine\n')

        if Ger == 0:# 3 value
            #dfiC['.GER'].append('NO')
            print('GER file : no')
            newtextfile.write('\nGER file : no\n')
    except:
        #dfiC['.GER'].append('-')
        print('cant ger directory '+ GERcheck)
        newtextfile.write('cant ger directory ' + GERcheck+ '\n')
#--------------------------------------------------------------------------------------#
print('\n\n\n\nErrors:\n----------------------\n')
errorfile.write('Errors:\n----------------------\n')
for value in Fservers:
    ping = PING(value)
    if (ping == 1):
        print('\n'+value+'\n--------------------\n')
        print('this machines have no ping respond\n')
        errorfile.write('\n' + value + '\n--------------------\n')
        errorfile.write('this machines have no ping respond\n')
    if (ping == 0):
        try:
            os.chdir('\\\\' + value + '\\c$')
            print('\n' + value + '\n--------------------')
            print('this machine dont have D drive')
            errorfile.write('\n' + value + '\n--------------------\n')
            errorfile.write('this machine dont have D drive\n\n')
        except:
            print('\n'+value+'\n--------------------')
            print('the user have no permission to enter the machine')
            errorfile.write('\n' + value + '\n--------------------\n')
            errorfile.write('the user have no permission to enter the machine\n\n')
errorfile.close()
newtextfile.close()
Gerfile.close()
MemoryIssue.close()
Prod.close()
int.close()
os.chdir(pat)
os.system('mkdir logs')
for file in list:
    os.system('mv '+file+' logs/')

#--------------------------------------------------------------------------------------#

#for x in dfC:
 #   df[x] = dfiC[x]

#print(df)
#df.to_excel('C:\\Users\\imasasax\\Desktop\\servers.xlsx')
