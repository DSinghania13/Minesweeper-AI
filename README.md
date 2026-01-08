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

#### Main Window
![Main](https://github.com/user-attachments/assets/3a151381-eb3d-4a9f-ac6a-4dea9e8a6550)


#### Manual Gameplay
![Manual](https://github.com/user-attachments/assets/32be7d7c-bff1-4b4a-b0fd-15a74ee6b1a6)



#### AI Gameplay
![AI](https://github.com/user-attachments/assets/2c3e7883-7550-4b5e-988e-505864e457a0)


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

## 📦 Distribution Summary

| Platform | Format | Python Required |
|--------|-------|----------------|
| macOS | `.dmg` | ❌ No |
| Windows | `.zip` (Portable EXE) | ❌ No |
| Source | GitHub | ✅ Yes (3.10+) |

---

## macOS DMG Installer

For macOS users, you can directly install the game without running from source.

👉 Download [`Minesweeper-Installer.dmg`](https://github.com/DSinghania13/Minesweeper-AI/raw/refs/heads/main/Minesweeper-Installer.dmg?download=)
1.	Double-click the .dmg file.
2.	Drag Minesweeper.app into the Applications folder.
    ![DMG](https://github.com/user-attachments/assets/f010264b-ffec-4686-94fd-1d56a08d086f)

3.	Launch from Applications (you may need to give access from Privacy and Security (in Settings) when opening the first time if Gatekeeper blocks it).

---

## 🪟 Windows Portable EXE (No Installer Required)

For Windows users, Minesweeper AI is distributed as a **portable executable package**.

👉 Download: [`MinesweeperAI_Windows.zip`](https://github.com/DSinghania13/Minesweeper-AI/raw/refs/heads/main/Minesweeper-Windows-Installer.zip?download=)

### How to Run (Windows)

1. Download `MinesweeperAI_Windows.zip`
2. Extract the ZIP file
3. Open the extracted folder
4. Double-click `MinesweeperAI.exe`

✅ No installation required  
✅ No administrator permissions needed  
✅ Works offline  

### Important Notes (Windows)

- The folder contains:
  - `MinesweeperAI.exe`
  - `_internal/` (required libraries, AI models, sounds, assets)
- **Do not delete or move the `_internal` folder**
- To uninstall the game, simply **delete the extracted folder**

> This portable setup is the Windows equivalent of a macOS DMG drag-and-drop app.

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
├── .gitattributes
├── .gitignore
└── README.md
```

---

## 📊 Kaggle Notebooks

Our full training process (CNN, RL, Hint reasoning) is documented in Kaggle notebooks.
- 📘 [CNN Model Training (Author: Divit Singhania)](https://www.kaggle.com/code/divitsinghania/minesweeper-cnn)
- 📙 [RL Agent Training (Author: Divit Singhania)](https://www.kaggle.com/code/divitsinghania/minesweeper-rl)

Sample data (.npz) is included in this repo.
Full datasets are available via Kaggle links above.

---

## 🧑‍💻 Installation & Setup

> If you only want to play the game, prefer the **Windows EXE** or **macOS DMG**.
> Running from source is intended for development, research, or training the AI models.

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

### Running from Source
- **Python 3.10+**
- PyQt6
- numpy
- tensorflow (required for AI mode)

> Note:
> - Development was done on macOS using Python 3.13
> - **Windows builds require Python 3.10 for stability**
>   (TensorFlow, PyInstaller, and PyQt6 are most stable on Windows with Python 3.10)

### Running Prebuilt Apps
- **Windows EXE** → No Python required
- **macOS DMG** → No Python required

---

## 📊 Performance

The performance of the AI is evaluated in two parts: the overall Reinforcement Learning (RL) agent's ability to win the game, and the underlying CNN's effectiveness at predicting mine locations.

**1. Reinforcement Learning (RL) Agent Performance**

The RL agent was trained over ~15,000 games to learn a winning strategy.

**Learning Progress**

The agent's learning is demonstrated by the cumulative win rate, which starts volatile and stabilizes as the agent gains experience. This shows a clear, positive learning trend.

![win_rate](https://github.com/user-attachments/assets/3d2ac88a-f989-4d13-b1fc-4d6a94035db8)

**Final Win Rate**

After training, the agent achieves a stable win rate of 30.4%, a strong performance for a game with high uncertainty.

![final_win_rate](https://github.com/user-attachments/assets/7420ced6-6265-43c7-a854-0e2864a1bec2)

**Behavioral Analysis**

Analysis of lost games shows that the AI is most vulnerable in the early stages, with 66.5% of losses occurring within the first 10 moves. This suggests that the agent's primary weakness is navigating the sparse information available at the beginning of a game.

![early_loss](https://github.com/user-attachments/assets/cb5acadd-9065-45f7-8823-b769b23356de)

**2. CNN Model Performance (Mine Prediction)**

The CNN acts as a fallback to predict mine probabilities when no logically safe move exists. Its performance is measured on a highly imbalanced dataset (many more safe cells than mines).

![roc](https://github.com/user-attachments/assets/b6219166-3664-4fc4-a0ab-54e9bc9ea9a5)

**Classification Report & Confusion Matrix**

The model achieves 99% accuracy, but this is misleading due to the class imbalance. The key metrics are precision and recall for the "Mine" class.

![confusion_matrix](https://github.com/user-attachments/assets/ca0500cc-d22a-4139-aba8-3c4206193c1c)

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

![precision](https://github.com/user-attachments/assets/9250edc2-478f-49fb-94a1-2fe213031c9f)

---

## 🎯 Future Work

- 🎓 Transformer-based reasoning for complex board states
- 🌍 Online leaderboard & multiplayer mode
- 📦 Optional Windows installer (Inno Setup) for Start Menu integration
- 🧠 Improved AI-human interaction with explainable move reasoning


> _Minesweeper is easy to play, but hard to master. With AI, it becomes a whole new challenge._

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software with proper attribution.

---
