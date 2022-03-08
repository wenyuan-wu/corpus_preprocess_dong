import os

def run(open_path,write_path):
    with open(open_path, 'r') as f:#read path
        lines = f.readlines()
        title=lines[3].strip()[10:-1]#title
        text=''
        for i in lines:
            i=i.strip()
            if(len(i)>6):
                if(i[1:5]=='text'):#text
                    text+=i[9:-2]
        fw=open(write_path,'w')#write path
        fw.write(title+'\n'+text)
        fw.close()
        f.close()
open_list='C:\Users\shuai31\Desktop\文章\论文成果\博一\cvoid-19\corpus\academic\2021-08-30\document_parses\pmc_json'#需处理的文件所在文件夹
write_path='C:\Users\shuai31\Desktop\文章\论文成果\博一\cvoid-19\corpus\academic\2021-08-30\document_parses\txt'#结果文件所在文件夹
for filename in os.listdir(open_list):#列举文件夹下所有文件
     run(open_list+'/'+filename,write_path+'/'+filename)#尽量读取和写入的路径不同