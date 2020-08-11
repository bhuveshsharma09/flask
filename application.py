import os
from flask import Flask, render_template, request

global total_sum
total_sum = 0
import math
import PyPDF2
import os

from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher



__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))







#enter your path here where you saved the resumes
mypath='C:\\Users\\65909\\Desktop\\ii' 
onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

def pdfextract(file):
    fileReader = PyPDF2.PdfFileReader(open(file,'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:    
        pageObj = fileReader.getPage(count)
        count +=1
        t = pageObj.extractText()
       # print (t)
        text.append(t)
    return text


def create_Data_Scientist_profile(file):
    text = pdfextract(file) 
    text = str(text)
    text = text.replace("\\n", "")
    text = text.lower()
    #below is the csv where we have all the keywords, you can customize your own
    keyword_dict = pd.read_csv('data_science_keywords.csv')
    
    keyword_total = list(keyword_dict.count())
    global total_sum
    total_sum = 0
    for i in keyword_total:
        total_sum = total_sum + i
        
    print('ee',total_sum)
    
    
    
    stats_words = [nlp(text) for text in keyword_dict['Statistics'].dropna(axis = 0)]
    NLP_words = [nlp(text) for text in keyword_dict['NLP'].dropna(axis = 0)]
    ML_words = [nlp(text) for text in keyword_dict['Machine Learning'].dropna(axis = 0)]
    DL_words = [nlp(text) for text in keyword_dict['Deep Learning'].dropna(axis = 0)]
    R_words = [nlp(text) for text in keyword_dict['R Language'].dropna(axis = 0)]
    python_words = [nlp(text) for text in keyword_dict['Python Language'].dropna(axis = 0)]
    Data_Engineering_words = [nlp(text) for text in keyword_dict['Data Engineering'].dropna(axis = 0)]

    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Stats', None, *stats_words)
    matcher.add('NLP', None, *NLP_words)
    matcher.add('ML', None, *ML_words)
    matcher.add('DL', None, *DL_words)
    matcher.add('R', None, *R_words)
    matcher.add('Python', None, *python_words)
    matcher.add('DE', None, *Data_Engineering_words)
    doc = nlp(text)
    
    d = []  
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start : end]  # get the matched slice of the doc
        d.append((rule_id, span.text))      
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
    
    ## convertimg string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    
    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
       
    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()
    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)
    print(dataf)
    return(dataf)
#=========================================
def create_web_dev_profile(file):
    text = pdfextract(file) 
    text = str(text)
    text = text.replace("\\n", "")
    text = text.lower()
    #below is the csv where we have all the keywords, you can customize your own
    keyword_dict = pd.read_csv('web_developer_keywords.csv')
    keyword_total = list(keyword_dict.count())
    global total_sum
    total_sum = 0
    for i in keyword_total:
        total_sum = total_sum + i
        
    print('ee',total_sum)
    
    front_end = [nlp(text) for text in keyword_dict['Front End'].dropna(axis = 0)]
    back_end = [nlp(text) for text in keyword_dict['Back End'].dropna(axis = 0)]
    database = [nlp(text) for text in keyword_dict['Database'].dropna(axis = 0)]
    project = [nlp(text) for text in keyword_dict['Projects'].dropna(axis = 0)]
    frameworks = [nlp(text) for text in keyword_dict['Frameworks'].dropna(axis = 0)]
    
    #print(front_end)
   # print(back_end)
    #print(database)
   
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('FrontEnd', None, *front_end)
    matcher.add('BackEnd', None, *back_end)
    matcher.add('Database', None, *database)
    matcher.add('Projects', None, *project)
    matcher.add('Frameworks', None, *frameworks)
 
    doc = nlp(text)
    #print(doc)
    
    d = []  
    matches = matcher(doc)
   # print(matches)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start : end]  # get the matched slice of the doc
        d.append((rule_id, span.text))      
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
    
    ## convertimg string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    
    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
       
    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()
    ## converting str to dataframe
    name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)
    print(dataf)
    return(dataf)









#--------------------------------------
@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    
    
    print('eer  0', request.form)
    dropdown_selection = str(request.form)
    dropdown_selection = dropdown_selection.split()
    dropdown_selection = dropdown_selection[1]
    
    if 'XMEN' in dropdown_selection:
        return ('Your are not an X men. You can never be.')
    
        #print(final_database)
    
   
        
    #code to count words under each category and visulaize it through Matplotlib
    
   
        
        
        
    
    target = os.path.join(APP_ROOT, 'images/')
    print('tt' , target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print('des',destination)
        file.save(destination)
        
        
        
        
    mypath = os. getcwd()
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    
    final_database=pd.DataFrame()
    i = 0 
    while i < 1:
        file = destination
        if 'WD' in dropdown_selection:
            print('-------------YES----------------')
            dat = create_web_dev_profile(file)
            selection = 'Web Developer'
        if 'DS' in dropdown_selection:
            print("--------------DS la ----------------")
            dat = create_Data_Scientist_profile(file)
            selection = 'Data Scientist'
        final_database = final_database.append(dat)
        i +=1
        
        

    final_database2 = final_database['Keyword'].groupby([final_database['Candidate Name'], final_database['Subject']]).count().unstack()
    final_database2.reset_index(inplace = True)
    final_database2.fillna(0,inplace=True)
    print(final_database2)
    #=====================
    ff = list(final_database2.columns)
    ff.pop(0)
    sum = 0
    for i in ff:
        sum = sum + final_database2[i]
        #print(final_database2[i])
    
    sum = int(sum)
    f = (sum/total_sum) * 100 
    print(f) 
    f = math.floor(f)
    
    
    
   
    return ('Your resume is  '+str(f)+'% like a '+str(selection))

if __name__ == "__main__":
    app.run()
    
    
    