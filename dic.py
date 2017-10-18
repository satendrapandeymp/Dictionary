from MySQLdb import escape_string as thwart
import MySQLdb, time, easygui

conn = MySQLdb.connect("localhost","root","  ","mydic")
c = conn.cursor()

fieldNames = ["part of speech type", 'meaning']


def translate(word):
    word = thwart(word)
    check = c.execute("SELECT * from entries WHERE word = '{0}'".format(word))
    if int(check)>0:
        data = c.fetchall()
        out = '\n'
        for datas in data:
            name = datas[0]
            typ = datas[1]
            meaning = datas[2]
            meaning = meaning.replace('.', '.\n')
            out =  out + '\n' + 'type - ' + typ + '\n' + 'meaning - ' + meaning + '\n'
        out = 'name - ' + name + out 
        easygui.msgbox(out, title="result")
    else:
        sugg = matching(word)
        sugg.append('NOTA')
        choice = easygui.buttonbox('Is your words are one of these?', 'Favorite Flavor', sugg)
        if choice == 'NOTA':
            check = easygui.ynbox('Could not find the word, do you want to add?', 'Title', ('Yes', 'No'))
            if check :
                fieldValues = list(easygui.multenterbox(msg='word to translate.', title='Enter', fields=(fieldNames)))
                typ = thwart(fieldValues[0])
                meaning = thwart(fieldValues[1])
                update(word, typ, meaning)
        else:
            translate(choice)

def update(w, t, m):
    c.execute("INSERT INTO entries (word, wordtype, definition) VALUES ('{0}','{1}','{2}')".format(w,t,m ))
    conn.commit()

def matching(word):
    templist = insertion(word)
    templist += swaping(word)
    templist += replaceing(word)
    templist += deletion(word)
    return final(templist)

def insertion(word):
    templist = []
    temp = 'abcdefghijklmnoprstuvxyz'
    for i in range(len(word)):
        arr1 = word[:i]
        arr2 = word[i:]
        for j in range(len(temp)):
            samp = arr1 + temp[j] + arr2
            templist.append(samp)         
    return templist
         
def swaping(word):
    templist = []
    for i in range(len(word)-1):
        arr1 = word[:i]
        arr2 = word[2+i:]
        samp = arr1 + word[i+1] + word[i] + arr2
        templist.append(samp)  
    return templist

def deletion(word):
    templist = []
    for i in range(len(word)):
        arr1 = word[:i]
        arr2 = word[1+i:]
        samp = arr1 + arr2
        templist.append(samp)  
    return templist

def replaceing(word):
    temp = 'abcdefghijklmnoprstuvxyz'
    templist = []
    for i in range(len(word)):
        arr1 = word[:i]
        arr2 = word[i+1:]
        for j in range(len(temp)):
            samp = arr1 + temp[j] + arr2
            templist.append(samp)  
    return templist

def final(wordlist):
    finallist = []
    for word in wordlist:
        check = c.execute("SELECT * from entries WHERE word = '{0}'".format(word))
        if int(check)>0:
            finallist.append(word)
    return finallist


while(True):
    word = easygui.enterbox(msg="Type your word below", title="Dictionary")
    if word == 'quit':
        break
    translate(word)
