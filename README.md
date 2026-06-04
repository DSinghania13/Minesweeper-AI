# 💣 Minesweeper AI – Play, Solve, and Learn

**Minesweeper AI** is an interactive PyQt6-based Minesweeper game with **manual play, AI-assisted solving, and rule-based hints**.
It combines classic **gameplay** with modern AI agents (CNN & RL) trained on thousands of game sessions.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/Framework-PyQt6-green)
![AI](https://img.shields.io/badge/AI-CNN%20%7C%20RL-orange)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)

---

### 🖼️ Gameplay Preview

Players can switch between Manual Mode 🎮 and AI Mode 🤖, featuring smooth UI, sounds, and animations.

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
- **💻 Cross-Platform** – Works on macOS (DMG installer available) & Windows (Portable EXE available)

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

👉 Download [`Minesweeper-macOS-Installer.dmg`](https://github.com/DSinghania13/Minesweeper-AI/raw/refs/heads/main/Installers/Minesweeper-macOS-Installer.dmg?download=)

### How to Run (macOS)

1.	Double-click the .dmg file.
2.	Drag Minesweeper.app into the Applications folder.

    ![DMG](https://github.com/user-attachments/assets/ba0d8000-a74c-40e6-982c-6d4699cd4765)

3. Launch the app from the Applications folder.

> ℹ️ If macOS Gatekeeper blocks the app on first launch, go to **System Settings → Privacy & Security** and allow it manually.

---

## 🪟 Windows Portable EXE (No Installer Required)

For Windows users, Minesweeper AI is distributed as a **portable executable package**.

👉 Download: [`Minesweeper-Windows-Installer.zip`](https://github.com/DSinghania13/Minesweeper-AI/raw/refs/heads/main/Installers/Minesweeper-Windows-Installer.zip?download=)

### How to Run (Windows)

1. Download `Minesweeper-Windows-Installer.zip`
2. Extract the ZIP file.

![ZIP Extraction](https://github.com/user-attachments/assets/32597420-8689-487e-96e5-a228bb5c30b1)


3. After extraction, open the newly created folder.

![Extracted Folder](https://github.com/user-attachments/assets/dee45bc5-84ca-45b0-93ee-965620cdeb80)


4. Double-click `MinesweeperAI.exe` to launch the game.

✅ No installation required  
✅ No administrator permissions needed  
✅ Works offline  

---

### 📂 Folder Structure (Windows)

The extracted folder will look like this:

![Windows Folder Structure](https://github.com/user-attachments/assets/ac2c0772-9082-4920-9e98-f00d7aa337aa)

- `MinesweeperAI.exe` → Main application  
- `_internal/` → Required libraries, AI models, sounds, and assets  

⚠️ **Do not delete or move the `_internal` folder**, as the application depends on it.

To uninstall the game, simply **delete the extracted folder**.

> This portable setup is the **Windows equivalent of a macOS DMG drag-and-drop app**.

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

# macOS / Linux
source .venv/bin/activate

# Windows
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

## 📊 Neuro-Symbolic AI Performance

The performance of the AI is evaluated in two parts: the overall **Neuro-Symbolic Agent's** ability to win the game, and the underlying **CNN's** effectiveness at predicting mine locations during forced blind guesses.

### 1. Neuro-Symbolic Agent Performance

The current AI utilizes a Neuro-Symbolic Architecture, cascading through Rule-Based Logic, CSP Math, and Deep RL to make decisions.

**Overall Game Outcomes & Win Rate**

Across a 1000-game test batch, the AI achieved a highly robust 69.3% Win Rate. Because Minesweeper frequently generates board states that force 50/50 blind guesses, a 100% win rate is mathematically impossible. A 69.3% success rate demonstrates a highly optimized decision engine.

![Overall Game Outcomes](assets/win_loss_pie_chart.png)

The cumulative win rate stabilizes perfectly around 70% as the agent plays more games. The 50-game moving average highlights this sustained performance without volatile dips.

![Cumulative Win Rate](assets/win_rate_plot.png)
![Moving Win Rate](assets/moving_win_rate_plot.png)

**AI Workload Breakdown**

The architecture is highly computationally efficient. 87.4% of all moves are handled entirely by the fast, lightweight Rule-Based Logic engine. The more resource-intensive CNN and CSP matrix solvers are only triggered on complex frontiers or blind guessing scenarios.

![Workload Breakdown](assets/ai_workload_pie.png)

**Guessing Behavior**

When the AI is forced into a corner and *must* take a risk, it delegates the guess almost equally between exact CSP Mathematical probabilities and the CNN's global spatial intuition.

![Guessing Behavior](assets/guessing_behavior_bar.png)

**Behavioral & Loss Analysis**

Analysis of lost games proves that the AI's logic engine is virtually flawless in the mid-to-late game. 87.0% of all losses occur within the first 10 moves. 

![Loss Breakdown](assets/loss_breakdown_pie_chart.png)

Zooming in on those early game losses, the absolute highest spike in deaths occurs exactly on Moves 2 and Move 3. The AI predominantly dies to unavoidable early-game RNG before enough clues are revealed to form a logic frontier.

![Early Losses Distribution](assets/early_losses_distribution.png)

---

### 2. CNN Model Performance (Mine Prediction)

The CNN acts as a fallback to predict mine probabilities when no logically safe move exists. Its performance is measured on a highly imbalanced dataset (many more safe cells than mines).

**ROC Curve**

The model demonstrates strong predictive capability, separating safe tiles from mines effectively across different threshold values.
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
