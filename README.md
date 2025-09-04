# 💣 Minesweeper AI – Play, Solve, and Learn

**Minesweeper AI** is an interactive PyQt6-based Minesweeper game with **manual play, AI-assisted solving, and rule-based hints**.
It combines classic **gameplay** with modern AI agents (CNN & RL) trained on thousands of game sessions.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/Framework-PyQt6-green)
![AI](https://img.shields.io/badge/AI-CNN%20%7C%20RL-orange)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)

---

### 🖼️ Gameplay Preview

Players can switch between Manual Mode 🎮 and AI Mode 🤖 with smooth UI, sounds, and animations.

#### Manual Gameplay
![Manual](#)  

#### AI Gameplay
![AI](#)

---

## 🚀 Features

- **🎮 Manual Play** – Classic Minesweeper with smooth UI and sounds
- **🤖 AI Mode** – Let a trained CNN/RL agent play for you
- **🧩 Rule-Based Solver** – AI-powered hints explain safe/unsafe moves
- **🔔 Sound Effects & Animations** – Interactive experience with explosions, flags, and victory sounds
- **📊 Score System** – Separate high scores for Manual & AI play
- **📂 Sample Datasets** – Included JSON/NPZ files to showcase AI training
- **💻 Cross-Platform** – Works on macOS (DMG installer available) & Windows (EXE planned)

---

## macOS DMG Installer

For macOS users, you can directly install the game without running from source.

👉 [Download Minesweeper-Installer.dmg](./Minesweeper-Installer.dmg)
1.	Double-click the .dmg file.
2.	Drag Minesweeper.app into the Applications folder.
3.	Launch from Applications (you may need to right-click → Open the first time if Gatekeeper blocks it).

---

## 🛠️ Tech Stack

| Component        | Technology Used               |
|------------------|-------------------------------|
| GUI              | PyQt6                         |
| Game Logic       | Custom Python (env, hints)    |
| AI Models        | TensorFlow (CNN & RL)         |
| Dataset Format   | NumPy (.npz, JSON)            |
| Sounds/Graphics  | WAV, GIF, PNG assets          |

---

## 📁 Project Structure

📂 Here's how the core directory looks:

```bash
Minesweeper/
├── main.py
├── game_ui.py
├── game_ai.py
├── game_manual.py
│
├── ai/
│   ├── ai_agent.py
│   └── rule_based_solver.py
│
├── core/
│   ├── hint_manager.py
│   ├── minesweeper_env.py
│   ├── scoreManager.py
│   ├── settingsManager.py
│   └── soundManager.py
│
├── assets/
│   ├── icons/
│   ├── sounds/
│   ├── dmg_background.png
│   ├── explosion.gif
│   └── flame.gif
│
├── data/
│   ├── sessions_sample.json
│   ├── game_sample1.json
│   └── game_sample2.json
│
├── dataset/
│   └── final_moves_dataset.npz
│
├── model/
│   ├── final_rl_model.keras
│   └── minesweeper_cnn_model.keras
│
├── json/
│   ├── settings.json
│   ├── highscore_manual.json
│   └── highscore_ai.json
│
├── Minesweeper-Installer.dmg
├── requirements.txt
└── README.md
```

---

## 📊 Kaggle Notebooks

Our full training process (CNN, RL, Hint reasoning) is documented in Kaggle notebooks.
- 📘 CNN Model Training (Author: Divit Singhania) []
- 📙 RL Agent Training (Author: Divit Singhania) []

Sample data (.json and .npz) is included in this repo.
Full datasets are available via Kaggle links above.

---

## 🧑‍💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/DSinghania13/Minesweeper-AI.git
cd Minesweeper-AI
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv .venv
source .venv/bin/activate
.venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Game

```bash
python main.py
```

- Manual Mode → Play Minesweeper yourself
- AI Mode → Watch the AI solve in real-time

---

## ⚙️ Requirements

- Python 3.10+ (Developed in python 3.13)
- PyQt6
- numpy
- tensorflow (optional – only required for AI gameplay mode)

---

## 📊 Performance

The performance of the AI is evaluated in two parts: the overall Reinforcement Learning (RL) agent's ability to win the game, and the underlying CNN's effectiveness at predicting mine locations.

**1. Reinforcement Learning (RL) Agent Performance**

The RL agent was trained over ~15,000 games to learn a winning strategy.

**Learning Progress**

The agent's learning is demonstrated by the cumulative win rate, which starts volatile and stabilizes as the agent gains experience. This shows a clear, positive learning trend.

**Final Win Rate**

After training, the agent achieves a stable win rate of 30.4%, a strong performance for a game with high uncertainty.

**Behavioral Analysis**

Analysis of lost games shows that the AI is most vulnerable in the early stages, with 66.5% of losses occurring within the first 10 moves. This suggests that the agent's primary weakness is navigating the sparse information available at the beginning of a game.

**2. CNN Model Performance (Mine Prediction)**

The CNN acts as a fallback to predict mine probabilities when no logically safe move exists. Its performance is measured on a highly imbalanced dataset (many more safe cells than mines).

**Classification Report & Confusion Matrix**

The model achieves 99% accuracy, but this is misleading due to the class imbalance. The key metrics are precision and recall for the "Mine" class.

```bash
--- Classification Report ---
              precision    recall  f1-score   support
  Not a Mine       0.99      1.00      1.00    727559
        Mine       0.73      0.04      0.08      4519
```

- Precision (Mine) = 0.73: When the CNN predicts a mine, it's correct 73% of the time.

- Recall (Mine) = 0.04: The CNN only finds 4% of all actual mines.

This shows the model is risk-averse: it avoids guessing "Mine" unless it is very confident, making it good for finding the safest move, but not for identifying all mines.

**Precision-Recall Curve**

This curve is the most honest view of the model's performance on an imbalanced dataset. It shows that to achieve higher precision (certainty), the model must sacrifice recall (finding all mines). This trade-off is central to its risk-averse strategy.

---

## 🎯 Future Work

- 🪟 Windows EXE build (currently TensorFlow DLL issue under investigation)
- 🎓 More advanced AI with transformer-based reasoning
- 🌍 Online leaderboard & multiplayer mode


> _Minesweeper is easy to play, but hard to master. With AI, it becomes a whole new challenge._

---
