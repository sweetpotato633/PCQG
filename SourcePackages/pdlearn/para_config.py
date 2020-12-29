

def SaveListToFile(file_name,msg):
    with open(file_name,'a+',encoding='utf-8') as fp:
        msg = msg + "\n"
        fp.write(msg)

def LoadListFromFile(file_name):
    try:
        with open(file_name,'r',encoding='utf-8') as fp:
            content = fp.read()
            mlist = content.split('\n')
            m2list = [m1 for m1 in mlist if m1 != '\n' and m1 != ""]
            return m2list
    except Exception as e:
        with open(file_name,'w+',encoding='utf-8') as fp:
            content = fp.read()
        return []