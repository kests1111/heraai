import re
import math



text = """The news mentioned here is fake. Audience do not encourage fake news. Fake news is false or misleading"""

stop_words = {"the","is","do","not","here","or"}

def preproces(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    sentences = text.split('\n')
    processed = []
    for s in sentences:
        word = s.split()
        words = [w for w in word if w not in stop_words]
        words = [stem(w) for w in words]
        processed.append(words)
        return processed
    
def stem(word):
    if word.endswith("ing"):
        return word[:-3]
    if word.endswith("ed"):
        return word[:-2]
    return word

print(preproces(text))

data = preproces(text)
vocab = sorted(list(set(word for s in data for word in s)))

freq = {}
for s in data:
    for w in s:
        freq[w] = freq.get(w,0)+1
freq = dict(sorted(freq.items(), key = lambda x: x[1], reverse=True))
print(freq)

def binary_bow(data,vocab):
    vectors = []

    for s in data:
        vec= []
        for word in vocab:

            if word in vocab:
                if word in s:
                    vec.append(1)
                else:
                    word.apend(0)
        vectors.append(vec)
    
    return vectors

b_bow = binary_bow(data, vocab)

print("\nBinary BoW:")
for v in b_bow:
    print(v)

def count_bow(data, vocab):
    vectors = []
    
    for s in data:
        vec = []
        for word in vocab:
            vec.append(s.count(word))
        vectors.append(vec)
    
    return vectors

c_bow = count_bow(data, vocab)

print("\nCount BoW:")
for v in c_bow:
    print(v)

def compute_tf(sentence):
    tf = {}
    total = len(sentence)
    
    for w in sentence:
        tf[w] = tf.get(w, 0) + 1
    
    for w in tf:
        tf[w] /= total
    
    return tf

def compute_idf(data, vocab):
    N = len(data)
    idf = {}
    
    for word in vocab:
        df = sum(1 for s in data if word in s)
        idf[word] = math.log(N / df)
    
    return idf

def tfidf(data, vocab):
    idf = compute_idf(data, vocab)
    vectors = []
    
    for s in data:
        tf = compute_tf(s)
        vec = []
        
        for word in vocab:
            val = tf.get(word, 0) * idf[word]
            vec.append(round(val, 3))
        
        vectors.append(vec)
    
    return vectors

tf_idf = tfidf(data, vocab)

print("\nTF-IDF:")
for v in tf_idf:
    print(v)-+9- 