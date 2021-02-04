import json
from scipy import spatial


def mk_vec(WC_wrd1,WC_wrd2):

    vec1=[]
    vec2=[]

    for key1, value1 in WC_wrd1.items():
        vec1.append(value1)
        if key1 in WC_wrd2:
            vec2.append(WC_wrd2[key1])
        else:
            vec2.append(0.0)

    for key2, value2 in WC_wrd2.items():
        if key2 not in WC_wrd1:
            vec2.append(value2)
            vec1.append(0.0)

    return vec1,vec2



def calc_sim(author_f1,author_f2):

    with open(author_f1, 'r') as f1:
        data1 = f1.read().replace('\n', '')

    with open(author_f2, 'r') as f2:
        data2 = f2.read().replace('\n', '')

    WC_wrd1=json.loads(data1)
    WC_wrd2=json.loads(data2)

    vec1,vec2=mk_vec(WC_wrd1,WC_wrd2)

    return 1-spatial.distance.cosine(vec1, vec2)

#print (calc_sim("./word_cloud/words/author1.txt","./word_cloud/words/author2.txt"))
