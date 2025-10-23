#include <bits/stdc++.h>
using namespace std;

struct Sample {
    vector<double> x;
    int y; // класс
};

double euclidean(const vector<double>& a, const vector<double>& b) {
    double s = 0.0;
    for (size_t i = 0; i < a.size(); ++i) {
        double d = a[i] - b[i];
        s += d * d;
    }
    return sqrt(s);
}

class KNN {
    int k;
    vector<Sample> train;
    function<double(const vector<double>&, const vector<double>&)> dist;
public:
    KNN(int k_, decltype(dist) metric = euclidean) : k(k_), dist(metric) {}

    void fit(const vector<Sample>& data) { train = data; }

    int predict(const vector<double>& x) const {
        vector<pair<double,int>> ds;
        ds.reserve(train.size());
        for (auto& s : train) {
            ds.emplace_back(dist(x, s.x), s.y);
        }
        nth_element(ds.begin(), ds.begin() + min((size_t)k, ds.size()) , ds.end(),
                    [](auto& a, auto& b){ return a.first < b.first; });
        int kk = min((int)ds.size(), k);
        unordered_map<int,int> cnt;
        int bestLabel = -1, bestCnt = -1;
        for (int i = 0; i < kk; ++i) {
            int lbl = ds[i].second;
            int c = ++cnt[lbl];
            if (c > bestCnt || (c == bestCnt && lbl < bestLabel)) {
                bestCnt = c; bestLabel = lbl;
            }
        }
        return bestLabel;
    }

    // regression 
    double predict_reg(const vector<double>& x, const vector<double>& yvals) const {
        vector<pair<double,size_t>> ds;
        ds.reserve(train.size());
        for (size_t i = 0; i < train.size(); ++i)
            ds.emplace_back(dist(x, train[i].x), i);
        nth_element(ds.begin(), ds.begin() + min((size_t)k, ds.size()) , ds.end(),
                    [](auto& a, auto& b){ return a.first < b.first; });
        int kk = min((int)ds.size(), k);
        double s = 0.0;
        for (int i = 0; i < kk; ++i) s += yvals[ds[i].second];
        return s / kk;
    }
};

int main() {
    vector<Sample> data = {
        {{0.0,0.0}, 0}, {{1.0,1.0}, 0}, {{0.9,1.1}, 0},
        {{3.0,3.0}, 1}, {{3.2,2.9}, 1}, {{2.8,3.1}, 1}
    };
    KNN knn(3);
    knn.fit(data);

    vector<vector<double>> queries = {{0.2,0.1}, {2.9,3.2}, {1.5,1.5}};
    for (auto& q : queries) {
        cout << "pred(" << q[0] << "," << q[1] << ") = "
             << knn.predict(q) << "\n";
    }
    return 0;
}
