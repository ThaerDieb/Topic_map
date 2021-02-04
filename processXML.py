import glob
import csv
import os
import bs4 as bs



## extract title, keywords, abstract for each paper
XML_path="Authors_XML/"
TXT_path="Authors_TXT/"

##elsevier: title:dc:title, keywords:ce:keyword, abstract:ce:abstract
##AIP: title:article-title, keywords:, abstract:abstract, on the web, they have subjects as keywaords but not in the XML
##Wiley: title:titleGroup, keywrods:keyword, abstract:abstract
##ACS: title:article-title,keywords:, abstract:abstract, on the web, they have subjects as keywaords but not in the XML
##RSC: title:titlegrp,keywords:,abstract:abstract, the have footnnote in the title
##springer: title:ArticleTitle, keywords:,abstract:abstract
##JJAP: title:article-title ,keywords:,abstract:abstract
##IOP: title:article-title, keywords:,abstract:abstract
#APS

title_tags=['dc:title','article-title','titlegroup','titlegrp','articletitle']
keywords_tags=['ce:keyword','keyword']
abstract_tags=['ce:abstract','abstract','dc:description']

err_file="./error_file.txt"

if not os.path.exists(TXT_path):
    os.makedirs(TXT_path)

with open(err_file, 'w+') as err:

    for dir in os.listdir(XML_path):
        if (not dir.startswith('.')) and (os.path.isdir(XML_path+dir)):
            if not os.path.exists(TXT_path+dir):
                os.makedirs(TXT_path+dir)
            for filename in glob.glob(XML_path+dir+'/*.xml'):
                txt_filename = filename.replace(XML_path, TXT_path).replace('xml', 'txt')
                with open(filename, 'r') as f:
                    soup = bs.BeautifulSoup(f, 'lxml')
                    with open(txt_filename, 'w+') as tf:
                        writer = csv.writer(tf, delimiter="\t")

                        titles = soup.find_all(title_tags)
                        if len(titles)!=0:
                            for title in titles:
                                if (title.name=="dc:title") or (title.name=="article-title") or (title.name=="titlegrp") or (title.name=="articletitle"):
                                    foots=title.find_all('footnote')
                                    if len(foots)!=0:
                                        for foot in foots:
                                            foot.replaceWith('')
                                    writer.writerow(['title',title.text.strip().replace("/[\r\n]+/", " ")])
                                    break
                                elif title.name=="titlegroup":
                                    foundt=False
                                    subts=title.find_all('title')
                                    for subt in subts:
                                        if (subt['type']=='main') and not subt.has_attr('sort'):
                                            writer.writerow(['title', subt.text.strip().replace("/[\r\n]+/", " ")])
                                            foundt=True
                                            break
                                    if foundt:
                                        break

                        else:
                            err.write (filename+"\n")
                            err.write ("no title detected\n")


                        keywords=soup.find_all(keywords_tags)
                        if len(keywords)!=0:
                            for keyword in keywords:
                                writer.writerow(['keyword', keyword.text.strip().replace("/[\r\n]+/", " ")])
                        else:
                            subjkeys=soup.find_all('dcterms:subject')
                            if len(subjkeys)!=0:
                                for subjkey in subjkeys:
                                    writer.writerow(['keyword', subjkey.text.strip().replace("/[\r\n]+/", " ")])
                            else:
                                err.write (filename+"\n")
                                err.write ("no keywords detected\n")


                        abstracts=soup.find_all(abstract_tags)
                        if len(abstracts)!=0:
                            for abstract in abstracts:
                                if abstract.name=='abstract':
                                    if not (abstract.has_attr('type') or abstract.has_attr('abstract-type')):
                                        writer.writerow(['abstract', abstract.text.replace('Abstract','').strip().replace("/[\r\n]+/", " ")])
                                        break
                                    elif abstract.has_attr('type'):
                                        if abstract['type']=="main":
                                            writer.writerow(['abstract',abstract.text.replace('Abstract', '').strip().replace("/[\r\n]+/", " ")])
                                            break
                                    elif abstract.has_attr('abstract-type'):
                                        if abstract['abstract-type']=="main":
                                            writer.writerow(['abstract',abstract.text.replace('Abstract', '').strip().replace("/[\r\n]+/", " ")])
                                            break
                                    else:
                                        err.write(filename+"\n")
                                        err.write("no abstract detected\n")

                                elif abstract.name=='ce:abstract':
                                    founda=False
                                    abs_titles=abstract.find_all('ce:section-title')
                                    for abs_title in abs_titles:
                                        if abs_title.text=='Abstract':
                                            writer.writerow(['abstract', abstract.text.replace('Abstract','').strip().replace("/[\r\n]+/", " ")])
                                            founda=True
                                            break
                                    if founda:
                                        break

                                elif abstract.name=='dc:description':
                                    writer.writerow(['abstract',abstract.text.replace('Abstract', '').strip().replace("/[\r\n]+/"," ")])
                                    break



                        else:
                            err.write (filename+"\n")
                            err.write ("no abstract detected\n")
