import re
import jieba
import collections
from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences
import multiprocessing


stop_words = []
with open('stop_words_new.txt', "r", encoding="UTF-8") as f:
    line = f.readline()
    while line:
        stop_words.append(line[:-1])
        line = f.readline()
stop_words = set(stop_words)
print('停用词读取完毕，共{n}个词'.format(n=len(stop_words)))

jieba.load_userdict(r'dict1.txt')
output = open('word_new.txt','w',encoding='utf-8')
f = open('sample.txt',encoding='utf-8')
index = 0;raw_word_list = [];mm = ''
#去除emoji表情
emoji1 = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]');emoji2 =  re.compile(u'[\U00010000-\U0010ffff]')
pattern = re.compile('www');pattern1 = re.compile('http');pattern2 = re.compile('com');pattern3 = re.compile('xfplay');pattern4 = re.compile('WWW')
for i in f.readlines():
    line = i.strip()
    #去除网站信息的文本
    if len(pattern1.findall(line)) >= 1 or len(pattern.findall(line)) >= 1 or len(pattern2.findall(line)) >= 1 or len(pattern3.findall(line)) >= 1 or len(pattern3.findall(line)) >= 1:
        index = index + 1
    else:
        while ' ' in line:
            line = line.replace(' ', '')
        #去除纯数字的文本数据
        if len(emoji1.findall(line)) >= 1 or len(emoji2.findall(line)) >= 1:
            #emoji2.sub(r'',line)无法删掉表情，前面需要加上 line = ...
            line = emoji2.sub('',line)
            line = emoji1.sub('',line)

        try:
            int(line)
        except ValueError:
            if len(line) > 0 :  # 如果句子非空
                raw_words = list(jieba.cut(line, cut_all=False))
                tmp = ''
                for word in raw_words:
                    if word not in stop_words:
                        raw_word_list.append(word)
                        tmp += word + ' '
                tmp = tmp.strip()
                if tmp:
                    output.write(tmp + '\n')

word_count = collections.Counter(raw_word_list)
print(raw_word_list)
print('文本中总共有{n1}个单词,不重复单词数{n2},选取前30000个单词进入词典'
      .format(n1=len(raw_word_list), n2=len(word_count)))

f.close()
output.close()
print('匹配到的网站数量：',index)


def word2vec():
    print('Start...')
    model = Word2Vec(PathLineSentences('word.txt'),size=50, window=5, min_count=5, workers=multiprocessing.cpu_count(),negative = 5)
    model.save('gensim_wv_test.model')
    model.wv.save_word2vec_format('vector_gensim', binary=False)
    print("Finished!")
    return model


def wordsimilarity(word, model):
    semi = ''
    try:
        semi = model.most_similar(word, topn=10)
    except KeyError:
        print('The word not in vocabulary!')
    for term in semi:
        print('%s,%s' % (term[0],term[1]))

model = word2vec()
valid_word = ['支付宝','贷款','理财','金融','周星驰','可爱',"跑步","超级","吃饭",'电影','那个']
for i in valid_word:
    print('Nearset to ',i)
    print(wordsimilarity(word=i, model=model))
