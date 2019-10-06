from bs4 import BeautifulSoup
import urllib
import re
import wikipedia

all_pages = ['https://www.tripadvisor.com/Attractions-g293916-Activities-c47-Bangkok.html','https://www.tripadvisor.com/Attractions-g293916-Activities-c47-oa30-Bangkok.html#FILTERED_LIST','https://www.tripadvisor.com/Attractions-g293916-Activities-c49-Bangkok.html','https://www.tripadvisor.com/Attractions-g293916-Activities-c57-Bangkok.html']
information = '{\n'

all_names = list()
for eachpage in all_pages:
    page_list = urllib.urlopen(eachpage)
    soup_list = BeautifulSoup(page_list, 'html.parser')
    mydivs = soup_list.findAll("div", {"class": "photo_booking non_generic"})


    for div in mydivs:
        for link in div.findAll('a'):
            a = link.get('href')
        # use english names from Tripadvisor's Top 100 ranking  
        page1 = urllib.urlopen('https://www.tripadvisor.com{}'.format(a))
        soup1 = BeautifulSoup(page1, 'html.parser')
        engName = soup1.findAll('title')[0].getText().split(' (')[0].replace('- TripAdvisor','')
        engName = engName.replace(', Bangkok','')
        engName = engName.replace('- 2019 All You Need to Know BEFORE You Go','')
        
        # find matched Thai names on th page of tripadvisor
        page2 = urllib.urlopen('https://th.tripadvisor.com{}'.format(a))
        soup2 = BeautifulSoup(page2, 'html.parser')
        thaiName = soup2.findAll('title')[0].getText().split(' (')[0].replace('- TripAdvisor','')
        thaiName = thaiName.replace('- 2019 All You Need to Know BEFORE You Go','')

        # search for about in wikipedia
        about = ''
        se_ab = wikipedia.search(' '.join([engName,'thailand','tourist']))
        ## top result
        if len(se_ab) > 0:
            if u'Thailand' == se_ab[0]:
                w = wikipedia.page(se_ab[1])
                ## get about from summary (use only first 3 sentences)
                sen = wikipedia.summary(se_ab[1],sentences=2)
                ## remove thai characters and additional information from the sentences
                about=re.sub('\([^)]*\)', '', sen)
                about = about.replace(' )','')
                ## cleaner version (find all full stop and cut only at the end of the second full stop)
                fullstops = [i for i, j in enumerate(about) if j == '.']
                about = about[:fullstops[1]]+'.'
            else:
                w = wikipedia.page(se_ab[0])
                ## get about from summary (use only first 3 sentences)
                sen = wikipedia.summary(se_ab[0],sentences=2)
                ## remove thai characters and additional information from the sentences
                about=re.sub('\([^)]*\)', '', sen)
                about = about.replace(')','')
                about = about.replace(']','')
                ## cleaner version (find all full stop and cut only at the end of the second full stop)
                fullstops = [i for i, j in enumerate(about) if j == '.']
                about = about[:fullstops[1]]+'.'
        
        #remove unicode characters, which might hurt TTS,  from the sentence 
        about = about.encode('ascii', 'ignore')
        #remove double-quote and newline from about to write as json
        about = about.replace('\"','')
        about = about.replace('\n','')
        print about
        
        if thaiName != engName:
            if engName not in all_names:
                print engName,
                print '>>>>',
                print thaiName.encode('utf8')
                #write in json format
                #removing leading and trailing whitespaces, use lowercase for index
                information += '  \"{}\": {{\n'.format(engName.strip().lower())
                #use utf8 encoding for thai characters
                information += '    \"thai\": \"{}\",\n'.format(thaiName.encode('utf8'))
                information += '    \"about\": \"{}\"\n  }},\n'.format(about)
                all_names.append(engName)
information = information[:-2] + '\n}'


with open('places_en2th.json','w') as f:
    f.write(information)
