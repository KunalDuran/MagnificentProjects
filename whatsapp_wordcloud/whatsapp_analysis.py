import re
import nltk
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


def analyze(filename):
    # reading the uploaded file
    # uploaded = os.listdir('uploaded_files')[0]
    file = open(os.path.join("uploaded_files",filename), encoding='utf-8')
    file.readline()
    

    # new clean file (csv version) for reading in pandas
    newfile_name = 'cleaned_'+filename
    newfile = open(newfile_name, 'w', encoding='utf-8')


    # converting txt file to usable csv format with help of regex
    raw = []
    count=0
    for index, line in enumerate(file.readlines()):
        x = re.search(r'(.+), (\d+:\d+) - (\w+): (.*)',line)
        if x == None:

            count+=1
            raw[index-count][-1]+= line.strip()
        else:
            raw.append([*x.groups()])


    for line in raw:
        newfile.write(','.join(line)+'\n')

    file.close()
    newfile.close()


    # Reading converted file (txt to csv) 
    df = pd.read_csv(newfile_name,
                     names=['date','time','sender','message'],skiprows=1, encoding='utf-8')


    # Filtering Voice notes, images and other documents 
    new_df = df[(df.message != '<Media omitted>')]
    new_df = new_df.dropna()


    # Text processing 
    raw = []
    for word in new_df.message:
        token = nltk.word_tokenize(str(word).lower())
        raw.extend(token)

    fdist = nltk.FreqDist(raw)

    stopwords = {'han', '.', 'ni', 'nahi', 'toh', 'to', 'phir', 'abhi', 'hi', 'he', 'kar', 'Ye', 'se', 'kuch', 'ki', 'are',
                 'aur', ',', '?', 'ko', 'h', 'hai', 'ho', '😅', 'ka', 'k', 'ab', 'kya', 'tha', 'm', 'bhi', 'rhi', 'thi',
                 'rha'}

    # print(fdist.most_common(10))
    words_for_wordcloud = ' '.join([w[0] for w in fdist.most_common(200)])
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white',
                            stopwords=stopwords,min_font_size = 10).generate(words_for_wordcloud)

    # plot the WordCloud image
    
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad = 0)
    #plt.show()
    imagename = os.path.splitext(filename)[0]
    imagename = imagename+'_image.jpg'
    # print(imagename) 
    plt.savefig('static/output_files/'+imagename)
