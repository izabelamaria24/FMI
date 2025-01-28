#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <climits>
#include <stack>
#include <set>
#include <unordered_map>
#include <cstring>
#include <functional>
#include <iostream>

using namespace std;

// -------------------------------------------------------
// ALL YOUR FUNCTION DEFINITIONS (as in your code snippet)
// -------------------------------------------------------

// BFS
vector<int> BFS(const vector<vector<int>> &adj, int N, int start) {
    vector<int> dist(N, -1);
    queue<int> q;
    q.push(start);
    dist[start] = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}

// DFS
void DFSUtil(const vector<vector<int>> &adj, int u, vector<bool> &visited, vector<int> &order) {
    visited[u] = true;
    order.push_back(u);
    for (int v : adj[u]) {
        if (!visited[v]) {
            DFSUtil(adj, v, visited, order);
        }
    }
}

vector<int> DFS(const vector<vector<int>> &adj, int N, int start) {
    vector<bool> visited(N, false);
    vector<int> order;
    DFSUtil(adj, start, visited, order);
    return order;
}

// Kruskal
struct Edge {
    int u, v, weight;
    bool operator<(const Edge &other) const {
        return weight < other.weight;
    }
};

int findSet(vector<int> &parent, int x) {
    if (parent[x] != x) {
        parent[x] = findSet(parent, parent[x]);
    }
    return parent[x];
}

void unionSet(vector<int> &parent, vector<int> &rank, int x, int y) {
    int xr = findSet(parent, x);
    int yr = findSet(parent, y);
    if (xr != yr) {
        if (rank[xr] < rank[yr]) {
            parent[xr] = yr;
        } else if (rank[xr] > rank[yr]) {
            parent[yr] = xr;
        } else {
            parent[yr] = xr;
            rank[xr]++;
        }
    }
}

pair<int, vector<Edge>> Kruskal(const vector<Edge> &edges, int N) {
    vector<Edge> mst;
    vector<int> parent(N), rank(N, 0);
    for (int i = 0; i < N; ++i) {
        parent[i] = i;
    }

    vector<Edge> sortedEdges = edges;
    sort(sortedEdges.begin(), sortedEdges.end());

    int mstWeight = 0;
    for (const Edge &edge : sortedEdges) {
        if (findSet(parent, edge.u) != findSet(parent, edge.v)) {
            mstWeight += edge.weight;
            mst.push_back(edge);
            unionSet(parent, rank, edge.u, edge.v);
        }
    }
    return {mstWeight, mst};
}

// Bellman-Ford
pair<bool, vector<int>> BellmanFord(const vector<Edge> &edges, int N, int start) {
    vector<int> dist(N, INT_MAX);
    dist[start] = 0;

    for (int i = 0; i < N - 1; ++i) {
        for (const Edge &edge : edges) {
            if (dist[edge.u] != INT_MAX && dist[edge.u] + edge.weight < dist[edge.v]) {
                dist[edge.v] = dist[edge.u] + edge.weight;
            }
        }
    }

    // check for negative cycle
    for (const Edge &edge : edges) {
        if (dist[edge.u] != INT_MAX && dist[edge.u] + edge.weight < dist[edge.v]) {
            return {false, {}}; // negative cycle
        }
    }
    return {true, dist};
}

// Dijkstra
vector<int> Dijkstra(const vector<vector<pair<int,int>>> &adj, int N, int start) {
    vector<int> dist(N, INT_MAX);
    dist[start] = 0;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;

        for (auto &[v, w] : adj[u]) {
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

// Number of Connected Components
void DFS_CC(const vector<vector<int>> &adj, int u, vector<bool> &visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            DFS_CC(adj, v, visited);
        }
    }
}

int NumberOfConnectedComponents(const vector<vector<int>> &adj, int N) {
    vector<bool> visited(N, false);
    int count = 0;
    for (int i = 0; i < N; ++i) {
        if (!visited[i]) {
            count++;
            DFS_CC(adj, i, visited);
        }
    }
    return count;
}

// Topological Sort
void TopologicalSortUtil(const vector<vector<int>> &adj, int u, vector<bool> &visited, stack<int> &Stack) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            TopologicalSortUtil(adj, v, visited, Stack);
        }
    }
    Stack.push(u);
}

vector<int> TopologicalSort(const vector<vector<int>> &adj, int N) {
    vector<bool> visited(N, false);
    stack<int> Stack;

    for (int i = 0; i < N; ++i) {
        if (!visited[i]) {
            TopologicalSortUtil(adj, i, visited, Stack);
        }
    }

    vector<int> order;
    while (!Stack.empty()) {
        order.push_back(Stack.top());
        Stack.pop();
    }
    return order;
}

// Floyd-Warshall
pair<bool, vector<vector<int>>> FloydWarshall(const vector<vector<int>> &adj, int N) {
    vector<vector<int>> dist(N, vector<int>(N, INT_MAX));
    for (int i = 0; i < N; ++i) dist[i][i] = 0;

    for (int u = 0; u < N; ++u) {
        for (int v = 0; v < N; ++v) {
            if (adj[u][v] != INT_MAX) {
                dist[u][v] = adj[u][v];
            }
        }
    }

    for (int k = 0; k < N; ++k) {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX) {
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }

    // check for negative cycle
    for (int i = 0; i < N; ++i) {
        if (dist[i][i] < 0) {
            return {false, {}};
        }
    }
    return {true, dist};
}

// Edmond-Karp
int bfsEdmondKarp(const vector<vector<int>> &capacity,
                  const vector<vector<int>> &adj,
                  vector<vector<int>> &flow,
                  int source, int sink,
                  vector<int> &parent) {
    fill(parent.begin(), parent.end(), -1);
    parent[source] = -2;
    queue<pair<int,int>> q;
    q.push({source, INT_MAX});

    while (!q.empty()) {
        int u = q.front().first;
        int currFlow = q.front().second;
        q.pop();

        for (int v : adj[u]) {
            if (parent[v] == -1 && capacity[u][v] - flow[u][v] > 0) {
                parent[v] = u;
                int newFlow = min(currFlow, capacity[u][v] - flow[u][v]);
                if (v == sink) {
                    return newFlow;
                }
                q.push({v, newFlow});
            }
        }
    }
    return 0;
}

int EdmondKarp(const vector<vector<int>> &capacity,
               const vector<vector<int>> &adj,
               int N, int source, int sink) {
    vector<vector<int>> flow(N, vector<int>(N, 0));
    vector<int> parent(N);
    int maxFlow = 0;

    while (true) {
        int newFlow = bfsEdmondKarp(capacity, adj, flow, source, sink, parent);
        if (newFlow == 0) {
            break;
        }
        maxFlow += newFlow;

        int v = sink;
        while (v != source) {
            int u = parent[v];
            flow[u][v] += newFlow;
            flow[v][u] -= newFlow;
            v = u;
        }
    }
    return maxFlow;
}

// IsBipartite
bool IsBipartite(const vector<vector<int>> &adj, int N) {
    vector<int> color(N, -1);
    for (int start = 0; start < N; ++start) {
        if (color[start] == -1) {
            queue<int> q;
            q.push(start);
            color[start] = 0;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                for (int v : adj[u]) {
                    if (color[v] == -1) {
                        color[v] = 1 - color[u];
                        q.push(v);
                    }
                    else if (color[v] == color[u]) {
                        return false;
                    }
                }
            }
        }
    }
    return true;
}

// CountStronglyConnectedComponents (Kosaraju)
int CountStronglyConnectedComponents(const vector<vector<int>> &adj, int N) {
    vector<bool> visited(N, false);
    stack<int> Stack;

    function<void(int)> dfs1 = [&](int u) {
        visited[u] = true;
        for (int v : adj[u]) {
            if (!visited[v]) {
                dfs1(v);
            }
        }
        Stack.push(u);
    };

    // 1st pass
    for (int i = 0; i < N; i++) {
        if (!visited[i]) {
            dfs1(i);
        }
    }

    // build transpose
    vector<vector<int>> adjT(N);
    for (int u = 0; u < N; u++) {
        for (int v : adj[u]) {
            adjT[v].push_back(u);
        }
    }

    fill(visited.begin(), visited.end(), false);
    int sccCount = 0;

    function<void(int)> dfs2 = [&](int u) {
        visited[u] = true;
        for (int v : adjT[u]) {
            if (!visited[v]) {
                dfs2(v);
            }
        }
    };

    // 2nd pass
    while (!Stack.empty()) {
        int u = Stack.top();
        Stack.pop();
        if (!visited[u]) {
            sccCount++;
            dfs2(u);
        }
    }

    return sccCount;
}


int main() {
    // {
    //     cout << "Testing BFS & DFS\n";
    //     vector<vector<int>> adj = {
    //         {1,3},
    //         {0,2},
    //         {1,3},
    //         {0,2}
    //     };
    //     int N = 4;
    //     int start = 0;
    //     vector<int> bfsResult = BFS(adj, N, start);
    //     cout << "BFS from node 0: ";
    //     for (int d : bfsResult) cout << d << " ";
    //     cout << "\n";
    //     vector<int> dfsResult = DFS(adj, N, start);
    //     cout << "DFS from node 0: ";
    //     for (int d : dfsResult) cout << d << " ";
    //     cout << "\n";
    // }
    // {
    //     cout << "Testing Kruskal\n";
    //     vector<Edge> edges = {
    //         {0,1,10},{0,2,6},{0,3,5},{1,3,15},{2,3,4}
    //     };
    //     int N = 4;
    //     auto k = Kruskal(edges, N);
    //     cout << "MST weight = " << k.first << "\nEdges in MST:\n";
    //     for (auto &e : k.second) {
    //         cout << e.u << "-" << e.v << " (" << e.weight << ")\n";
    //     }
    // }
    // {
    //     cout << "Testing Bellman-Ford\n";
    //     vector<Edge> edges = {
    //         {0,1,1},{0,2,4},{1,2,-2},{1,3,2},{2,3,3}
    //     };
    //     int N = 4;
    //     int start = 0;
    //     auto b = BellmanFord(edges, N, start);
    //     if (!b.first) {
    //         cout << "Negative cycle detected\n";
    //     } else {
    //         cout << "Dist from 0: ";
    //         for (int i = 0; i < N; i++) {
    //             cout << b.second[i] << " ";
    //         }
    //         cout << "\n";
    //     }
    // }
    // {
    //     cout << "Testing Dijkstra\n";
    //     vector<vector<pair<int,int>>> adj = {
    //         {{1,1},{2,4}},
    //         {{2,2},{3,5}},
    //         {{3,1}},
    //         {}
    //     };
    //     int N = 4;
    //     int start = 0;
    //     vector<int> dist = Dijkstra(adj, N, start);
    //     cout << "Dist from node 0: ";
    //     for (int i = 0; i < N; i++) {
    //         cout << dist[i] << " ";
    //     }
    //     cout << "\n";
    // }
    // {
    //     cout << "Testing NumberOfConnectedComponents\n";
    //     vector<vector<int>> adj = {
    //         {1},
    //         {0,2},
    //         {1},
    //         {4},
    //         {3}
    //     };
    //     int N = 5;
    //     cout << "Connected components = " << NumberOfConnectedComponents(adj, N) << "\n";
    // }
    // {
    //     cout << "Testing TopologicalSort\n";
    //     vector<vector<int>> adj = {
    //         {},
    //         {},
    //         {3},
    //         {1},
    //         {0,1},
    //         {2,0}
    //     };
    //     int N = 6;
    //     vector<int> topo = TopologicalSort(adj, N);
    //     cout << "Topological order: ";
    //     for (int x : topo) {
    //         cout << x << " ";
    //     }
    //     cout << "\n";
    // }
    // {
    //     cout << "Testing Floyd-Warshall\n";
    //     int N = 4;
    //     vector<vector<int>> adj(N, vector<int>(N, INT_MAX));
    //     adj[0][1] = 5;
    //     adj[0][3] = 10;
    //     adj[1][2] = 3;
    //     adj[2][3] = 1;
    //     auto f = FloydWarshall(adj, N);
    //     if (!f.first) {
    //         cout << "Negative cycle detected\n";
    //     } else {
    //         cout << "All-pairs shortest paths:\n";
    //         for (int i = 0; i < N; i++) {
    //             for (int j = 0; j < N; j++) {
    //                 if (f.second[i][j] == INT_MAX) cout << "INF ";
    //                 else cout << f.second[i][j] << " ";
    //             }
    //             cout << "\n";
    //         }
    //     }
    // }
    // {
    //     cout << "Testing Edmond-Karp\n";
    //     int N = 4;
    //     vector<vector<int>> capacity = {
    //         {0,10,10,0},
    //         {0,0,5,5},
    //         {0,0,0,10},
    //         {0,0,0,0}
    //     };
    //     vector<vector<int>> adj = {
    //         {1,2},
    //         {2,3},
    //         {3},
    //         {}
    //     };
    //     int source = 0;
    //     int sink = 3;
    //     cout << "Max flow = " << EdmondKarp(capacity, adj, N, source, sink) << "\n";
    // }
    // {
    //     cout << "Testing IsBipartite\n";
    //     vector<vector<int>> adj = {
    //         {1,3},
    //         {0,2},
    //         {1,3},
    //         {0,2}
    //     };
    //     cout << (IsBipartite(adj,4) ? "Graph is bipartite\n" : "Graph is NOT bipartite\n");
    // }
    // {
    //     cout << "Testing CountStronglyConnectedComponents\n";
    //     vector<vector<int>> adj = {
    //         {1},
    //         {2},
    //         {0},
    //         {}
    //     };
    //     int N = 4;
    //     cout << "Number of SCCs = " << CountStronglyConnectedComponents(adj,N) << "\n";
    // }
    // return 0;
}
