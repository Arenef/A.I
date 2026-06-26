<h1 align="center">Artificial Intelligence Search Algorithms Visualization</h1>
<p align="center">
<b>Huỳnh Ngọc Bảo Khang</b><br>
Student ID: <b>24110241</b>
</p>

---

# 📑 Table of Contents

- 🎬 Algorithm Demonstrations
  - 🔹 Uninformed Search (Vacuum World)
  - 🤖 Informed Search (Vacuum World)
  - ⛰️ Local Search (Vacuum World)
  - 🧩 Complex Vacuum World
  - 🎨 Graph Coloring (CSP)
  - ❌ Adversarial Search (Tic-Tac-Toe)
- 📚 Algorithms Implemented

---

# 🎬 Algorithm Demonstrations
# 🧹 AppVacuum
# 🔹 Uninformed Search
Các thuật toán tìm kiếm cơ bản không sử dụng thông tin về khoảng cách hay chi phí tới mục tiêu. Thuật toán chỉ duyệt qua các trạng thái dựa trên cấu trúc đồ thị của môi trường Vacuum World để tìm đường đi.
## 🌲 Depth First Search (DFS)

| DFS Example 1 | DFS Example 2 |
|:-------------:|:-------------:|
| <img src="gif/uninform/dfs1.gif" width="430"> | <img src="gif/uninform/dfs2.gif" width="430"> |

---

## 🌊 Breadth First Search (BFS)

| BFS Example 1 | BFS Example 2 |
|:-------------:|:-------------:|
| <img src="gif/uninform/bfs1.gif" width="430"> | <img src="gif/uninform/bfs2.gif" width="430"> |

---

## 🔍 Iterative Deepening Search (IDS)

<p align="center">
<img src="gif/uninform/ids.gif" width="700">
</p>

---

## 💰 Uniform Cost Search (UCS)

<p align="center">
<img src="gif/uninform/ucs.gif" width="700">
</p>

---

# 🤖 Informed Search
Nhóm thuật toán tối ưu hơn nhờ sử dụng hàm Heuristic ước lượng khoảng cách từ trạng thái hiện tại đến cái đích cần dọn dẹp. Giúp Robot hút bụi định hướng thông minh hơn, giảm thiểu số bước duyệt thừa.
## ⭐ A* Search

<p align="center">
<img src="gif/inform/a star.gif" width="700">
</p>

---

## 🧭 Greedy Best First Search

<p align="center">
<img src="gif/inform/greedy.gif" width="700">
</p>

---

## 🚀 Iterative Deepening A* (IDA*)

<p align="center">
<img src="gif/inform/ida star.gif" width="700">
</p>

---

# ⛰️ Local Search
Nhóm thuật toán tập trung vào việc cải tiến trạng thái hiện tại bằng cách di chuyển sang các trạng thái lân cận tốt hơn. Phù hợp cho việc tối ưu hóa lộ trình trực tiếp mà không cần lưu trữ toàn bộ cây tìm kiếm.
## 📈 Simple Hill Climbing

<p align="center">
<img src="gif/local search/simple hill climbing.gif" width="700">
</p>

---

## 🏔️ Steepest Ascent Hill Climbing

<p align="center">
<img src="gif/local search/steepest ascent hill climbing.gif" width="700">
</p>

---

## 🎲 Stochastic Hill Climbing

<p align="center">
<img src="gif/local search/stochastic ascent hill climbing.gif" width="700">
</p>

---

## 🔄 Random Restart Hill Climbing

<p align="center">
<img src="gif/local search/random restart hill climbing.gif" width="700">
</p>

---

## 🌡️ Simulated Annealing

<p align="center">
<img src="gif/local search/simulated annealing.gif" width="700">
</p>

---

## 🔦 Local Beam Search

<p align="center">
<img src="gif/local search/local beam search.gif" width="700">
</p>

---

# 🧩 Complex Vacuum World

Mô phỏng các kịch bản nâng cao và thực tế hơn của Robot hút bụi khi đối mặt với môi trường không chắc chắn, không thể quan sát toàn diện hoặc có các yếu tố ngẫu nhiên xảy ra.
## 🌳 AND-OR Search

<p align="center">
<img src="gif/complex/and or search.gif" width="700">
</p>

---

## 🧠 Belief State Search

<p align="center">
<img src="gif/complex/belief state.gif" width="700">
</p>

---

## 👀 Partially Observable Environment

<p align="center">
<img src="gif/complex/partially observable.gif" width="700">
</p>

---

# 🎨 Graph Coloring (Constraint Satisfaction Problems)
Advanced Constraint Satisfaction Problems (CSP) algorithms demonstrated via **Ho Chi Minh City Map District Coloring**.
## ↩️ Backtracking Search

<p align="center">
<img src="gif/csp/backtracking.gif" width="700">
</p>

---

## 🔍 Forward Checking

<p align="center">
<img src="gif/csp/forward checking.gif" width="700">
</p>

---

## 📐 AC-3 (Arc Consistency)

<p align="center">
<img src="gif/csp/ac3.gif" width="700">
</p>

---

## 💥 Min-Conflicts Local Search

<p align="center">
<img src="gif/csp/min conflicts.gif" width="700">
</p>

---

# ❌ Adversarial Search (Tic-Tac-Toe)
Mô phỏng các thuật toán tìm kiếm đối kháng thông qua trò chơi **Cờ ca-rô (Tic-Tac-Toe)**. Trực quan hóa luồng tư duy, số lượng trạng thái phải duyệt và khả năng cắt tỉa của AI khi đối đầu với người chơi hoặc một AI khác.
## 🪵 Minimax Algorithm

<p align="center">
<img src="gif/game search/minimax.gif" width="700">
</p>

---

## ✂️ Alpha-Beta Pruning

<p align="center">
<img src="gif/game search/alpha-beta.gif" width="700">
</p>

---

## 🎲 Expectimax Search

<p align="center">
<img src="gif/game search/expectimax.gif" width="700">
</p>

---

# 📚 Algorithms Implemented

| Category | Algorithms |
|-----------|------------|
| 🔹 **Uninformed Search** | DFS • BFS • IDS • UCS |
| 🤖 **Informed Search** | Greedy Best First Search • A* • IDA* |
| ⛰️ **Local Search** | Simple Hill Climbing • Steepest Ascent Hill Climbing • Stochastic Hill Climbing • Random Restart Hill Climbing • Simulated Annealing • Local Beam Search |
| 🧩 **Complex Vacuum World** | AND-OR Search • Belief State Search • Partially Observable Search |
| 🎨 **Graph Coloring (CSP)** | Backtracking • Forward Checking • AC-3 • Min-Conflicts |
| ❌ **Tic-Tac-Toe (Adversarial)** | Minimax • Alpha-Beta Pruning • Expectimax |

---
