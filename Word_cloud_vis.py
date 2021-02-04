from wordcloud import WordCloud, STOPWORDS
import re
import matplotlib.pyplot as plt
import glob
import os.path
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_numeric
import csv
import nltk
import json



TXT_path="Authors_TXT/"
output_PNG="word_cloud/PNG/"
output_words="word_cloud/words/"

if not os.path.exists("word_cloud/"):
    os.makedirs("word_cloud/")

if not os.path.exists(output_PNG):
    os.makedirs(output_PNG)

if not os.path.exists(output_words):
    os.makedirs(output_words)

Authors={}
Auth_WC={}

## makding stoplists
with open('stopwords') as f:
    astop = set(f.read().splitlines())

with open('punc') as f:
    puncstop = set(f.read().splitlines())

with open('phyq') as f:
    phyqstop = set(f.read().splitlines())



stopwords = set(STOPWORDS)
stopwords.update(astop)
stopwords.update(puncstop)
stopwords.update(phyqstop)



## chemical symbols list
with open('chemSymbol') as f:
    chemsy = set(f.read().splitlines())
chemsy = list(dict.fromkeys(chemsy))


## measurment methods list
Me=[]
with open("measurement_terms") as f:
    for line in f.readlines():
        Me.append(line.replace("_method","").replace("_"," ").rstrip())


def gen_wf(text):
    words = nltk.tokenize.word_tokenize(strip_numeric(remove_stopwords(text)))

    resultwords = [word.lower() for word in words if ((word.lower() not in stopwords) and (len(word)>2))]

    fdist = nltk.FreqDist(resultwords)
    return dict (fdist)

def gen_wf_paper(doc):
    title_wf=gen_wf(doc[0])
    title_wf.update((x, y * 1.2) for x, y in title_wf.items())

    keys_wf = gen_wf(doc[1])
    keys_wf.update((x, y * 1.5) for x, y in keys_wf.items())

    abs_wf=gen_wf(doc[2])

    update_dic_freq(abs_wf,title_wf)
    update_dic_freq(abs_wf,keys_wf)

    return abs_wf


def gen_wf_author(author):
    author_terms={}
    papers_wf=[]
    for paper in author:
        papers_wf.append(gen_wf_paper(paper))

    for paper_wf in papers_wf:
        update_dic_freq(author_terms,paper_wf)

    return author_terms



def ext_mat_f_regex(text):
    chems = []
    sent_text = nltk.sent_tokenize(text)
    for sentence in sent_text:
        c=re.findall(r'\b(?:[A-Z][a-z]{0,1}\d{0,2}[.]{0,1}\d{0,2})+\b', sentence)

        chems.extend(c)

    chems_filt = []
    for chem in chems:
        if not chem.isupper():
            if len(chem)==1 or len(chem)==2:
                if chem in chemsy:
                    chems_filt.append(chem)
            else:
                chems_filt.append(chem)

    chemdist = nltk.FreqDist(chems_filt)

    return dict(chemdist)


def ext_mat_f_regex_paper(doc):
    all_txt=' '.join([doc[0],doc[1],doc[2]])
    paper_mat_f=ext_mat_f_regex(all_txt)

    return paper_mat_f


def ext_mat_f_regex_author(author):
    author_mat_f = {}
    papers_mat_f = []
    for paper in author:
        papers_mat_f.append(ext_mat_f_regex_paper(paper))

    for paper_mat_f in papers_mat_f:
        update_dic_freq(author_mat_f, paper_mat_f)

    return author_mat_f



def ext_me_f(text):
    mef = {}
    for met in Me:
        if text.count(met)!=0:
            mef[met]= text.count(met)

    return mef


def ext_me_f_paper(doc):
    all_txt=' '.join([doc[0],doc[1],doc[2]])
    paper_me_f=ext_me_f(all_txt)

    return paper_me_f


def ext_me_f_author(author):
    author_me_f = {}
    papers_me_f = []
    for paper in author:
        papers_me_f.append(ext_me_f_paper(paper))

    for paper_me_f in papers_me_f:
        update_dic_freq(author_me_f, paper_me_f)

    return author_me_f



def update_dic_freq(origin_dic,new_dic):
    for key in new_dic:
        if key in origin_dic:
            origin_dic[key]+=new_dic[key]
        else:
            origin_dic[key]=new_dic[key]


def update_dic_freq_x(origin_dic,new_dic):

    for key in list(new_dic.keys()):
        if key.lower() in list(origin_dic.keys()):
            del origin_dic[key.lower()]

    origin_dic.update(new_dic)



def gen_WC(author):
    tot_w_count = 0
    for paper in author:
        for sec in paper:
            tot_w_count += len(nltk.tokenize.word_tokenize(sec))

    author_wf=gen_wf_author(author)
    ### normalization of term frequency
    for term in author_wf:
        author_wf[term] = author_wf[term] / tot_w_count


    author_mat=ext_mat_f_regex_author(author)

    for mat in author_mat:
        author_mat[mat] = author_mat[mat] / tot_w_count

    update_dic_freq_x(author_wf,author_mat)


    author_me = ext_me_f_author(author)

    for me in author_me:
        author_me[me] = author_me[me] / tot_w_count

    update_dic_freq_x(author_wf, author_me)


    return WordCloud(stopwords=stopwords,collocations=False, background_color='white',prefer_horizontal=1, colormap="Dark2").generate_from_frequencies(frequencies=author_wf)



for dir in os.listdir(TXT_path):
    if not dir.startswith('.'):
        Authors[dir]=[]
        for filename in glob.glob(TXT_path+dir+'/*.txt'):
            doc=['','','']
            with open(filename, 'r') as f:
                reader = csv.reader(f, delimiter="\t")
                for row in reader:
                    if row[0]=='title':
                        doc[0]+=row[1]+" "
                    elif row[0]=='keyword':
                        doc[1]+=row[1]+" "
                    elif row[0]=='abstract':
                        doc[2]+=row[1]+" "
                    else:
                        print ('error, was not able to identify row')
            Authors[dir].append(doc)


for author in Authors:
    if len(Authors[author])!=0:
        Auth_WC[author]=gen_WC(Authors[author])
        with open (output_words+author+".txt", 'w+') as f:
            f.write(json.dumps(Auth_WC[author].words_))
        plt.imshow(Auth_WC[author], interpolation='bilinear')
        plt.axis("off")
        plt.savefig(output_PNG+author+'.png',dpi=320, format='png',bbox_inches="tight")








