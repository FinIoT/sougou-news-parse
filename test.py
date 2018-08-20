
# coding: utf-8

# In[70]:


import os
from xml.dom import minidom
from urllib.parse import urlparse


# In[71]:


#如文件缺少根元素标记，要用到此函数
def file_fill(file_dir):
    count=0
    #\n很容易漏掉
    start='<docs>\n'
    end='</docs>'
    for root,filefolder,files in os.walk(file_dir):
        print(len(files),type(files[0]))
        for file in files:
        #获取的root目录名中用的是正斜杠还是反斜杠,在windows下是反斜杠
            src_filename=root+'\\'+file
            #使用with语句好处多多
            with open(src_filename,encoding='GB18030') as src_file:
                src_filecont=src_file.readlines()
            tgt_fname=root+'\\new'+'\\'+file
            with open(tgt_fname,'a',encoding='utf8') as tgt_file:
                tgt_cont=tgt_file.write(start)
                for line in src_filecont:
                    text=line.replace('&','&amp;')
                    tgt_cont=tgt_file.write(text)
                tgt_cont=tgt_file.write(end)
            count+=1
            print(count)#查看程序进展
            


# In[72]:


def file_read(file_dir):
    count=0
    for root,fdir,fname in os.walk(file_dir):
        for f in fname:
            #原文件名
            f_src=root+'\\'+f
            #开始解析
            f_par=minidom.parse(f_src)
            f_doc=f_par.documentElement
            content=f_doc.getElementsByTagName('content')
            url=f_doc.getElementsByTagName('url')
            for i in range(len(url)):
                if content[i].firstChild==None or url[i].firstChild==None:
                    continue
                url_par=urlparse(url[i].firstChild.data)
                if url_par.hostname in dicurl:
                    if not os.path.exists(root+'\\'+dicurl[url_par.hostname]):
                        os.makedirs(root+'\\'+dicurl[url_par.hostname])
                    doc_path=root+'\\'+dicurl[url_par.hostname]+'\\'+'%d.txt'%(len(os.listdir(root+'\\'+dicurl[url_par.hostname]))+1)
                    #下面的encoding=utf8不能少啊，否则要出错gbk codec can't....
                    with open(doc_path,'w',encoding='utf8') as f_in:       
                        f_in.write(content[i].firstChild.data)
            
            count+=1
            print(count)
            
        
    


# In[73]:


if __name__=='__main__':
    #该函数会创将原来的ANSI更改为utf8编码文件，加入根元素<docs>,替换<和&.
    #file_fill(r'C:\Users\liks\liks\10IT\DataSet\Sougoumimi')
    dicurl = {'auto.sohu.com':'qiche','it.sohu.com':'hulianwang','health.sohu.com':'jiankang',
              'sports.sohu.com':'tiyu','travel.sohu.com':'lvyou','learning.sohu.com':'jiaoyu',
              'career.sohu.com':'zhaopin','cul.sohu.com':'wenhua','mil.news.sohu.com':'junshi',
              'house.sohu.com':'fangchan','yule.sohu.com':'yule','women.sohu.com':'shishang',
              'media.sohu.com':'chuanmei','gongyi.sohu.com':'gongyi','2008.sohu.com':'aoyun',
              'business.sohu.com': 'shangye'}
    #解析所有文件，并分类写到各类文件夹
    file_read(r'C:\Users\liks\liks\10IT\DataSet\sougoureducedTrain\new')
    

