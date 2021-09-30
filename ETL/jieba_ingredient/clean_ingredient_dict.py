projectDir = 'c:/Users/Tibame_25/Desktop/TFB-3_Project/Recipe/'

# clean ingredient format from net
# with open(projectDir + 'data/recipe/dict/ingredient_synonym.txt', 'r', encoding='utf-8') as f:
#     ingredientDict = [_.split('\n')[0] for _ in f.readlines()]

# with open(projectDir + 'data/recipe/dict/ingredient_synonym02.txt', 'w+', encoding='utf-8') as f:
#     for food in ingredientDict:
#         row = list(filter(None, food.split(',')))[1:]
#         row = ','.join(row)
#         f.write(row + '\n')

# make a ingredient dict as my_dict for jieba
with open(projectDir + 'data/recipe/dict/ingredient_synonym.txt', 'r', encoding='utf-8') as f:
    ingredientDict = [_.split('\n')[0] for _ in f.readlines()]

ingredient = [name for row in ingredientDict for name in row.split(',') ]

with open(projectDir + 'data/recipe/dict/ingredient_mydict.txt', 'w+', encoding='utf-8') as f:
    [f.write(row + '\n') for row in ingredient]