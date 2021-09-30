import json
import jieba
import re

# os.chdir('../..')
projectDir = 'c:/Users/Tibame_25/Desktop/TFB-3_Project/Recipe/'

with open(projectDir + 'data/recipe/dict/stopword.txt','r',encoding='utf-8') as f:
    stopWords = [w.replace('\n','') for w in f.readlines()]

with open(projectDir + 'data/recipe/dict/ingredient_synonym.txt', 'r', encoding='utf-8') as f:
    synonymList = [_.split('\n')[0] for _ in f.readlines()]

synonymDict = {synonym.split(',')[0]:[word.lower() for word in synonym.split(',')] for synonym in synonymList }
wordCountDict = {word:0 for word in synonymDict.keys()}
wordJobCountDict = wordCountDict.copy()

# # load recipeFinal
# with open(projectDir + 'data/recipe/recipeFinal.json', 'r', encoding='utf-8') as f:
#     recipe = json.load(f)

# load all recipe
with open(projectDir + 'data/recipe/recipeALL.json', 'r', encoding='utf-8') as f:
    recipe = json.load(f)

# get all ingredient and input in a list
ingredient = []
for post in recipe:
    materials = [ _ for _ in post['ingredient'].keys()]
    ingredient += materials
# ingredient = list(set(ingredient))
# ingredient.sort(reverse=False)

# clean the Punctuation Marks like ()
ING = ingredient.copy()
p = re.compile(r'\W\W*', re.S)  #最小匹配
n = 0

for mark in ingredient:
    index = [_.span() for _ in re.finditer(p,mark)]
    if len(index) == 0 or len(index)%2 == 1:
        ING[n] = mark
        n += 1
        continue
    
    outword = [ingredient[n][ index[2*i][0] : index[2*i+1][1] ] 
               for i in range(int(len(index)/2)) ]
    
    for word in outword:
        mark = mark.replace(word,'')

    ING[n] = mark
    n +=1 



# use jieba to count ingredient number
sb = ','.join(ingredient)

jieba.load_userdict(projectDir + 'data/recipe/dict/ingredient_mydict.txt')

wordCut = jieba.cut(sb)
wordCutList = [w for w in wordCut]

wordCountDict = dict()

for w in wordCutList:
    if w in stopWords:
        continue
    if w in wordCountDict:
        wordCountDict[w] += 1
    else:
        wordCountDict[w] = 1

wordCountList = [(k,v) for k, v in wordCountDict.items()]
wordCountList.sort(key=lambda x:x[1], reverse=True)

# for recipe final
# with open(projectDir + '/data/recipe/dict/ingredient_count_v2.txt','w+',encoding='utf-8') as f:
#     for word in wordCountList:
#         row = ','.join(list(map(lambda x:str(x), word)))
#         f.write(row + '\n')

# with open(projectDir + '/data/recipe/dict/ingredient_count02.txt','w+',encoding='utf-8') as f:
#     wordCountList.sort(key=lambda x:x[0], reverse=True)
#     for word in wordCountList:
#         row = ','.join(list(map(lambda x:str(x), word)))
#         f.write(row + '\n')

# for all recipe 
with open(projectDir + '/data/recipe/dict/ingredient_count_all_v2.txt','w+',encoding='utf-8') as f:
    for word in wordCountList:
        row = ','.join(list(map(lambda x:str(x), word)))
        f.write(row + '\n')

with open(projectDir + '/data/recipe/dict/ingredient_count_all_word_v2.txt','w+',encoding='utf-8') as f:
    wordCountList.sort(key=lambda x:x[0], reverse=True)
    for word in wordCountList:
        row = ','.join(list(map(lambda x:str(x), word)))
        f.write(row + '\n')

# for word in synonymDict.keys():
#     wordexist = 0
#     for w in synonymDict[word]:
#         wordCountDict[word] += wordCutList.count(w)
#         wordexist += wordCutList.count(w)
#     if wordexist > 0:
#         wordJobCountDict[word] += 1

with open(projectDir + '/data/recipe/dict/ingredient_all_v2.txt','w+',encoding='utf-8') as f:
    for row in ING:
        f.write(row + '\n')


## combine and see all ingredient name and another name from FDA database
# with open('./data/recipe/食品成分資料庫.json', 'r', encoding='utf-8') as f:
#     FDAData = json.load(f)
# name = []
# for fda in FDAData:
#     if fda['俗名'] == '':
#         name += [ fda['樣品名稱'] ]
#     else:
#         name += [ ','.join( [ fda['樣品名稱'], fda['俗名'] ] ) ]
# fdaName = list(set(name))
# with open('./data/recipe/食品成分資料庫_食品名稱字典.text','a+', encoding='utf-8') as f:
#     [ f.write(foodName + '\n') for foodName in fdaName ] 


