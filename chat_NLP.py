import re
from collections import Counter, defaultdict
import pymorphy3
import nltk
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ── ПАРСИНГ ───────────────────────────────────────────────────────────────────

def parse(filepath):
    pattern = re.compile(r"\[[\d., :]+\]\s+(.+?):\s+(.*)")
    skip = {"видеозаметка", "изображение", "аудиофайл", "документ", "Карточка", "удалили", "Аудиозвонок"}
    messages = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                author, text = m.groups()
                if any(s in text for s in skip):
                    continue
                author = "Тимур" if author == "qwquqyu2e" else author
                messages.append((author, text))
    return messages

# ── ПРЕДОБРАБОТКА ─────────────────────────────────────────────────────────────

morph = pymorphy3.MorphAnalyzer()
STOP = set(stopwords.words("russian")) | {"это","ну","вот","да","нет","ок","окей","ща","привет","пока"}

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^а-яё ]", " ", text)
    tokens = [t for t in text.split() if len(t) > 2 and t not in STOP]
    lemmas = [morph.parse(t)[0].normal_form for t in tokens]
    return [l for l in lemmas if l not in STOP and len(l) > 2]

# ── АНАЛИЗ ────────────────────────────────────────────────────────────────────

messages = parse(r"C:\Users\soldierofgabe\Desktop\_chat.txt")

# Топ слов по всему чату
all_words = []
for author, text in messages:
    all_words.extend(preprocess(text))

print("=== ТОП-20 СЛОВ ===")
for word, count in Counter(all_words).most_common(20):
    print(f"  {word:20s} {count}")

# Топ слов по каждому автору
print("\n=== СЛОВА ПО АВТОРАМ ===")
author_words = defaultdict(list)
for author, text in messages:
    author_words[author].extend(preprocess(text))

for author, words in author_words.items():
    print(f"\n[{author}]")
    for word, count in Counter(words).most_common(10):
        print(f"  {word:20s} {count}")

# Пример предобработки
print("\n=== ПРИМЕР ПРЕДОБРАБОТКИ ===")
for author, text in messages[:5]:
    lemmas = preprocess(text)
    if lemmas:
        print(f"  Исходное : {text}")
        print(f"  Результат: {lemmas}\n")

# Кластеризация
print("=== КЛАСТЕРИЗАЦИЯ (KMeans) ===")
docs = [" ".join(preprocess(text)) for _, text in messages]
docs = [d for d in docs if d.strip()]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)

km = KMeans(n_clusters=4, random_state=42, n_init=10)
km.fit(X)

terms = vectorizer.get_feature_names_out()
for i, center in enumerate(km.cluster_centers_):
    top = [terms[j] for j in center.argsort()[-6:][::-1]]
    count = list(km.labels_).count(i)
    print(f"\n  Кластер {i+1} ({count} сообщ.): {', '.join(top)}")