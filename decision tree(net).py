import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import a
df = pd.read_csv(r"C:\Users\soldierofgabe\Downloads\postuplenie.csv")

target_col = 'Accept'


X = df.drop(columns=[target_col])
y = df[target_col]

model = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=5,
    random_state=42
)

model.fit(X, y)

target_col = 'Accept'


# -------------------------------------------------------------------
def entropy(y):
    values, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return -np.sum(probs * np.log2(probs + 1e-9))



def information_gain(X_column, y, threshold):
    parent_entropy = entropy(y)

    left_mask = X_column <= threshold
    right_mask = X_column > threshold

    if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
        return 0

    n = len(y)
    n_left = np.sum(left_mask)
    n_right = np.sum(right_mask)

    e_left = entropy(y[left_mask])
    e_right = entropy(y[right_mask])

    child_entropy = (n_left / n) * e_left + (n_right / n) * e_right

    return parent_entropy - child_entropy



def best_split(X, y):
    best_gain = -1
    split_idx = None
    split_threshold = None

    for col in X.columns:
        values = X[col].unique()

        for val in values:
            gain = information_gain(X[col].values, y.values, val)

            if gain > best_gain:
                best_gain = gain
                split_idx = col
                split_threshold = val

    return split_idx, split_threshold


# --- Узел дерева ---
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # если лист



def build_tree(X, y, depth=0, max_depth=5):
    # если все классы одинаковые
    if len(np.unique(y)) == 1:
        return Node(value=y.iloc[0])

    # если достигли глубины
    if depth >= max_depth:
        return Node(value=y.mode()[0])

    feature, threshold = best_split(X, y)

    if feature is None:
        return Node(value=y.mode()[0])

    left_mask = X[feature] <= threshold
    right_mask = X[feature] > threshold

    left = build_tree(X[left_mask], y[left_mask], depth+1, max_depth)
    right = build_tree(X[right_mask], y[right_mask], depth+1, max_depth)

    return Node(feature, threshold, left, right)



def predict_one(x, node):
    if node.value is not None:
        return node.value

    if x[node.feature] <= node.threshold:
        return predict_one(x, node.left)
    else:
        return predict_one(x, node.right)


def predict(X, tree):
    return np.array([predict_one(row, tree) for _, row in X.iterrows()])



X = df.drop(columns=[target_col])
y = df[target_col]

tree = build_tree(X, y, max_depth=5)

