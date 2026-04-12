import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

np.random.seed(42)
X, y = make_classification(
    n_samples=600,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    class_sep=0.5,
    random_state=42
)

class_names = ['не спам', 'спам']
feature_names = ['восклицательные знаки', 'доля заглавных букв']
colors = {0: '#2ECC71', 1: '#E74C3C'}

df = pd.DataFrame(X, columns=feature_names)
df['Класс'] = [class_names[i] for i in y]

print(f'Всего писем: {len(df)}')
print(f'Не спам: {sum(y==0)}  |  Спам: {sum(y==1)}')
df.head(6)
fig, ax = plt.subplots(figsize=(8, 5))
for label, color in colors.items():
    mask = y == label
    ax.scatter(X[mask, 0], X[mask, 1],
               label=class_names[label], color=color, alpha=0.6, s=50, edgecolors='white', linewidth=0.5)
ax.set_xlabel(feature_names[0], fontsize=12)
ax.set_ylabel(feature_names[1], fontsize=12)
ax.set_title('Два класса в пространстве двух признаков', fontsize=13)
ax.legend(fontsize=11)
plt.tight_layout()
plt.show()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Считаем вручную — именно это делает GaussianNB.fit() внутри
stats = {}
for label in [0, 1]:
    mask = y_train == label
    stats[label] = {
        'mean':  X_train[mask].mean(axis=0),
        'std':   X_train[mask].std(axis=0),
        'prior': mask.sum() / len(y_train)  # P(класс)
    }

print('Что модель запомнила после fit():')
print()
for label in [0, 1]:
    s = stats[label]
    print(f'  [{class_names[label].upper()}]')
    print(f'    P(класс) = {s["prior"]:.3f}')
    for i, fn in enumerate(feature_names):
        print(f'    {fn}: mu = {s["mean"][i]:.3f},  sigma = {s["std"][i]:.3f}')
    print()
# Gaussian в названии GaussianNB — потому что каждый признак
# моделируется нормальным (гауссовым) распределением.
# Вот как это выглядит:

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

for ax, feat_i, fname in zip(axes, [0, 1], feature_names):
    for label, color in colors.items():
        values = X_train[y_train == label, feat_i]
        mu    = stats[label]['mean'][feat_i]
        sigma = stats[label]['std'][feat_i]

        # гистограмма реальных данных
        ax.hist(values, bins=20, alpha=0.35, color=color, density=True)

        # гауссова кривая поверх — то что модель «видит»
        x_range = np.linspace(values.min() - 1, values.max() + 1, 200)
        ax.plot(x_range, norm.pdf(x_range, mu, sigma),
                color=color, linewidth=2.5, label=f'{class_names[label]}  μ={mu:.2f}')
        ax.axvline(mu, color=color, linestyle='--', linewidth=1.2, alpha=0.7)

    ax.set_xlabel(fname, fontsize=11)
    ax.set_ylabel('Плотность вероятности', fontsize=10)
    ax.set_title(f'Признак: {fname}', fontsize=12)
    ax.legend(fontsize=10)

plt.suptitle('Модель аппроксимирует каждый признак гауссовой кривой', fontsize=12, y=1.02)
plt.tight_layout()
plt.show()
# Новое письмо: много восклицательных знаков и заглавных букв — похоже на спам
new_email = np.array([1.5, 1.2])

def gaussian_pdf(x, mu, sigma):
    """Вероятность значения x при нормальном распределении N(mu, sigma)"""
    return (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

print(f'Новое письмо:')
print(f'  {feature_names[0]} = {new_email[0]}')
print(f'  {feature_names[1]} = {new_email[1]}')
print()

scores = {}
for label in [0, 1]:
    prior = stats[label]['prior']
    p_x1  = gaussian_pdf(new_email[0], stats[label]['mean'][0], stats[label]['std'][0])
    p_x2  = gaussian_pdf(new_email[1], stats[label]['mean'][1], stats[label]['std'][1])

    # НАИВНОЕ допущение: перемножаем как независимые
    score = prior * p_x1 * p_x2
    scores[label] = score

    print(f'  [{class_names[label].upper()}]')
    print(f'    P(класс)         = {prior:.3f}')
    print(f'    P(x1 | класс)    = {p_x1:.5f}')
    print(f'    P(x2 | класс)    = {p_x2:.5f}')
    print(f'    prior * p1 * p2  = {score:.2e}  <- score')
    print()

total = sum(scores.values())
probs = {label: scores[label] / total for label in [0, 1]}
winner = max(probs, key=probs.get)

print(f'Нормализуем scores в вероятности:')
print(f'  P(не спам | письмо) = {probs[0]:.4f}')
print(f'  P(спам    | письмо) = {probs[1]:.4f}')
print()
print(f'  >>> Вручную: {class_names[winner]}')
# Проверяем через sklearn — результат должен совпасть
model = GaussianNB()
model.fit(X_train, y_train)

prob_sklearn = model.predict_proba([new_email])[0]
pred_sklearn = model.predict([new_email])[0]

print('Сравниваем:')
print(f'  Вручную:  не спам={probs[0]:.4f}  спам={probs[1]:.4f}')
print(f'  sklearn:  не спам={prob_sklearn[0]:.4f}  спам={prob_sklearn[1]:.4f}')
print()
print(f'  sklearn говорит: {class_names[pred_sklearn]}')
print()
print('  Результаты совпадают — sklearn делает ровно то же самое.')
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Точность: {accuracy:.1%}')
print(f'Правильно классифицировано: {int(accuracy * len(y_test))} из {len(y_test)}')

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# --- Confusion matrix ---
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred,
    display_labels=class_names,
    cmap='Blues', ax=axes[0]
)
axes[0].set_title(f'Confusion Matrix — точность {accuracy:.1%}', fontsize=12)
# Строки = реальный класс, столбцы = предсказанный, диагональ = правильные ответы

# --- Граница решений ---
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                      np.linspace(y_min, y_max, 300))
Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

axes[1].contourf(xx, yy, Z, alpha=0.25, cmap='RdYlGn')
axes[1].contour(xx, yy, Z, colors='grey', linewidths=1.2, linestyles='--')
for label, color in colors.items():
    mask = y_test == label
    axes[1].scatter(X_test[mask, 0], X_test[mask, 1],
                    color=color, label=class_names[label], s=60,
                    edgecolors='white', linewidth=0.5, alpha=0.9)
axes[1].set_xlabel(feature_names[0], fontsize=11)
axes[1].set_ylabel(feature_names[1], fontsize=11)
axes[1].set_title('Граница решений модели', fontsize=12)
axes[1].legend(fontsize=10)

plt.tight_layout()
plt.show()
