import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import string
#from sklearn.metrics import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import ssl
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords

keywords = "Getting the homepage"
# folder path
dir_path = r'/Users/shivanknag/Downloads/News-Summarizer-master'
# list to store files
res = []
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)
print(res)
import re
matchedfiles = []
for file in res:
    # search given pattern in the line 
    match = re.search("\.py$", file)
    # if match is found
    if match:
        print("The file ending with .py is:",file)
        matchedfiles.append(file)
print(matchedfiles)
dic = {}
for i in matchedfiles:
    pathway = '/Users/shivanknag/Downloads/News-Summarizer-master/'+i
    with open(pathway) as x:
        content = x.read()
        g = open("writefule.txt", "w")
        g.write(content)
        g.close()
    functions = content.split("def ")
    functions.pop(0)
    lens = len(functions)
    c = 0
    f = open("functions.txt", "a")
    for y in functions:
        if c == lens:
            break
        name = functions[c].split("(")
        #print(name[0])
        dic[name[0]] = y
        c += 1
        f.writelines(name[0]+"\n")
    f.close()
    imports = content.split("import ")
    finalimports = []
    length = len(imports)
    cc = 0
    for y in imports:
        sc = 0
        for s in y:
            if s=="#":
                break
            elif s=="\n":
                finalimports.append(y[:sc])
                break
            elif s==" ":
                finalimports.append(y[:sc])
                break
            elif s==",":
                continue
            sc += 1
    f = open("imports.txt", "a")
    for y in finalimports:
        f.writelines(y+"\n")
    f.close()
    packages = content.split("from ")
    lpl = len(packages)
    c = 1
    f = open("packages.txt", "a")
    for y in packages:
        if c == lpl:
            break
        name = packages[c].split(" ")
        c += 1
        f.writelines(name[0]+"\n")
    f.close()
matchscores = {}
for key in dic:
    matchscores[key] = fuzz.partial_ratio(keywords, key)
sorted_dict = dict(reversed(list(sorted(matchscores.items(), key = lambda kv: kv[1]))))
print("\n\n\n")
print('Functions in the repository: ',end="\n\n")
print('Using Fuzzy Matching - ',end="\n\n")
for item in sorted_dict:
    print(item+', Match Score: ',sorted_dict[item],end="\n")
print("\n\n\n")
print('Functions in the repository: ',end="\n\n")
print('Using Cosine Similarity  - ',end="\n\n")

def findcosine(X_list,Y_list):
    X_list = word_tokenize(X_list) 
    Y_list = word_tokenize(Y_list)
    
    sw = stopwords.words('english') 
    l1 =[]
    l2 =[]
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw}
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine
matchscores2 = {}
for key in dic:
    matchscores2[key] = findcosine(key,keywords)
sorted_dict2 = dict(reversed(list(sorted(matchscores2.items(), key = lambda kv2: kv2[1]))))
for item in sorted_dict2:
    print(item+', Match Score: ',sorted_dict2[item],end="\n")
print("\n\n\n")