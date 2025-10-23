#include <bits/stdc++.h>
using namespace std;

// --------------------------- Data model ---------------------------
struct Sample {
    vector<double> x;
    int y;
};


inline double euclidean_sq(const vector<double>& a, const vector<double>& b) {
    double s = 0.0;
    for (size_t i = 0; i < a.size(); ++i) { double d = a[i] - b[i]; s += d * d; }
    return s;
}

// --------------------------- Brute-force KNN ----------------------
class KNNBrute {
    int k_;
    vector<Sample> train_;
public:
    explicit KNNBrute(int k): k_(k) {}
    void fit(vector<Sample> data) { train_ = std::move(data); }

    int predict(const vector<double>& x) const {
        vector<pair<double,int>> ds;
        ds.reserve(train_.size());
        for (auto& s : train_) ds.emplace_back(euclidean_sq(x, s.x), s.y);
        size_t kk = min((size_t)k_, ds.size());
        nth_element(ds.begin(), ds.begin()+kk, ds.end(),
                    [](auto& a, auto& b){ return a.first < b.first; });
        unordered_map<int,int> cnt;
        int bestLabel = -1, bestCnt = -1;
        for (size_t i = 0; i < kk; ++i) {
            int c = ++cnt[ds[i].second];
            if (c > bestCnt || (c == bestCnt && ds[i].second < bestLabel)) {
                bestCnt = c; bestLabel = ds[i].second;
            }
        }
        return bestLabel;
    }
};

// --------------------------- KD-Tree ------------------------------
struct KDNode {
    // point index into points_
    size_t idx;
    int split_dim;
    double split_val;
    KDNode* left = nullptr;
    KDNode* right = nullptr;
    // bounding box per node (optional optimization)
    vector<double> bbox_min, bbox_max;
    KDNode(size_t i, int d, double v, size_t dim)
        : idx(i), split_dim(d), split_val(v), bbox_min(dim, +numeric_limits<double>::infinity()),
          bbox_max(dim, -numeric_limits<double>::infinity()) {}
};

class KDTree {
    vector<vector<double>> points_;
    vector<int> labels_;
    KDNode* root_ = nullptr;
    size_t dim_ = 0;

public:
    KDTree() = default;
    ~KDTree() { free_node(root_); }

    void build(const vector<Sample>& data) {
        points_.clear(); labels_.clear();
        points_.reserve(data.size()); labels_.reserve(data.size());
        for (auto& s : data) { points_.push_back(s.x); labels_.push_back(s.y); }
        dim_ = points_.empty() ? 0 : points_[0].size();
        vector<size_t> idx(points_.size());
        iota(idx.begin(), idx.end(), 0);
        root_ = build_rec(idx.begin(), idx.end(), 0);
        compute_bbox(root_);
    }

    // kNN query: returns vector of (dist2, index)
    vector<pair<double,size_t>> knn(const vector<double>& q, size_t k) const {
        // Max-heap by distance (dist2, index)
        vector<pair<double,size_t>> heap;
        heap.reserve(k);
        knn_rec(root_, q, k, heap);
        return heap; // contains k best with max-heap property, but it’s fine for voting
    }

    int label(size_t i) const { return labels_[i]; }
    const vector<double>& point(size_t i) const { return points_[i]; }

private:
    using It = vector<size_t>::iterator;

    KDNode* build_rec(It begin, It end, int depth) {
        if (begin >= end) return nullptr;
        size_t n = end - begin;
        int axis = depth % (int)dim_;
        It mid = begin + n/2;
        nth_element(begin, mid, end, [&](size_t a, size_t b){
            return points_[a][axis] < points_[b][axis];
        });
        size_t idx = *mid;
        KDNode* node = new KDNode(idx, axis, points_[idx][axis], dim_);
        node->left  = build_rec(begin, mid, depth+1);
        node->right = build_rec(mid+1, end, depth+1);
        return node;
    }

    void compute_bbox(KDNode* node) {
        if (!node) return;
        // initialize with this point
        const auto& p = points_[node->idx];
        for (size_t d = 0; d < dim_; ++d) node->bbox_min[d] = node->bbox_max[d] = p[d];
        // merge from children
        if (node->left) {
            compute_bbox(node->left);
            for (size_t d = 0; d < dim_; ++d) {
                node->bbox_min[d] = min(node->bbox_min[d], node->left->bbox_min[d]);
                node->bbox_max[d] = max(node->bbox_max[d], node->left->bbox_max[d]);
            }
        }
        if (node->right) {
            compute_bbox(node->right);
            for (size_t d = 0; d < dim_; ++d) {
                node->bbox_min[d] = min(node->bbox_min[d], node->right->bbox_min[d]);
                node->bbox_max[d] = max(node->bbox_max[d], node->right->bbox_max[d]);
            }
        }
    }

    // squared distance from q to AABB
    double dist2_aabb(const vector<double>& q, const KDNode* node) const {
        double s = 0.0;
        for (size_t d = 0; d < dim_; ++d) {
            double v = q[d];
            if (v < node->bbox_min[d]) { double t = node->bbox_min[d] - v; s += t*t; }
            else if (v > node->bbox_max[d]) { double t = v - node->bbox_max[d]; s += t*t; }
        }
        return s;
    }

    static void heap_push_k(vector<pair<double,size_t>>& heap, size_t k, pair<double,size_t> cand) {
        if (heap.size() < k) {
            heap.push_back(cand);
            push_heap(heap.begin(), heap.end()); // max-heap by default on pair (lexicographic)
        } else if (cand.first < heap.front().first) {
            pop_heap(heap.begin(), heap.end());
            heap.back() = cand;
            push_heap(heap.begin(), heap.end());
        }
    }

    void knn_rec(KDNode* node, const vector<double>& q, size_t k,
                 vector<pair<double,size_t>>& heap) const {
        if (!node) return;

        // Visit current point
        double d2 = euclidean_sq(q, points_[node->idx]);
        heap_push_k(heap, k, {d2, node->idx});

        // Choose side to visit first
        KDNode* nearChild = (q[node->split_dim] < node->split_val) ? node->left : node->right;
        KDNode* farChild  = (nearChild == node->left) ? node->right : node->left;

        knn_rec(nearChild, q, k, heap);

        // Decide if far child could contain closer points
        double best_d2 = heap.empty() ? numeric_limits<double>::infinity() : heap.front().first;
        // Bounding box check is stronger; as a quick check we can also use hyperplane distance.
        bool need_far = false;
        if (farChild) {
            // AABB pruning
            double aabb_d2 = dist2_aabb(q, farChild);
            if (aabb_d2 < best_d2) need_far = true;
            // Hyperplane check (optional, may allow earlier branch):
            double plane_d = q[node->split_dim] - node->split_val;
            if (!need_far && plane_d*plane_d < best_d2) need_far = true;
        }
        if (need_far) knn_rec(farChild, q, k, heap);
    }

    void free_node(KDNode* node) {
        if (!node) return;
        free_node(node->left);
        free_node(node->right);
        delete node;
    }
};

// --------------------------- KNN with KDTree ----------------------
class KNNKDTree {
    size_t k_;
    KDTree tree_;
public:
    explicit KNNKDTree(size_t k): k_(k) {}
    void fit(const vector<Sample>& data) { tree_.build(data); }
    int predict(const vector<double>& x) const {
        auto heap = tree_.knn(x, k_);
        unordered_map<int,int> cnt;
        int bestLabel = -1, bestCnt = -1;
        for (auto& it : heap) {
            int lbl = tree_.label(it.second);
            int c = ++cnt[lbl];
            if (c > bestCnt || (c == bestCnt && lbl < bestLabel)) { bestCnt = c; bestLabel = lbl; }
        }
        return bestLabel;
    }
};

// --------------------------- Demo main ----------------------------
int main() {
    vector<Sample> data = {
        {{0.0,0.0}, 0}, {{1.0,1.0}, 0}, {{0.9,1.1}, 0},
        {{3.0,3.0}, 1}, {{3.2,2.9}, 1}, {{2.8,3.1}, 1},
        {{-1.0,0.5}, 2}, {{-1.2,0.7}, 2}
    };
    int k = 3;

    KNNBrute brute(k);
    brute.fit(data);

    KNNKDTree kd(k);
    kd.fit(data);

    vector<vector<double>> queries = {{0.2,0.1}, {2.9,3.2}, {1.5,1.5}, {-1.1,0.6}};
    cout << "Brute-force:\n";
    for (auto& q : queries)
        cout << "  (" << q[0] << "," << q[1] << ") -> " << brute.predict(q) << "\n";

    cout << "KD-tree:\n";
    for (auto& q : queries)
        cout << "  (" << q[0] << "," << q[1] << ") -> " << kd.predict(q) << "\n";

    return 0;
}
