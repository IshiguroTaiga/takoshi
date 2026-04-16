# 🎮 TicTacDistro: Distributed Tic-Tac-Toe Server

A real-time, multi-user distributed gaming system built with **Python (Flask)** and **WebSockets**. This project demonstrates core distributed systems concepts including state synchronization, concurrency, and centralized monitoring.

---

## 🚀 Key Features

### 👤 Client Side
- **Role-Based Auth:** Secure signup and login for individual player tracking.
- **Matchmaking Queue:** A distributed queue that pairs two live players into a shared game session.
- **Minimax AI:** A "Play vs AI" mode featuring a recursive backtracking algorithm (impossible to beat).
- **Real-time Gameplay:** Zero-refresh gameplay powered by WebSockets.
- **Rematch System:** Distributed agreement logic for restarting games.

### 🛡️ Admin Side (The "/ishi" Panel)
- **Live Monitor:** Real-time view of all active game boards across the network.
- **System Stats:** Track total users and active vs. finished games.
- **Activity Log:** A live stream of every network event (Logins, moves, matchmaking).
- **Remote Termination:** Ability for the admin to force-close any game session.

---

## 🏗️ Distributed Systems Concepts Applied

1. **Client-Server Architecture:** Centralized server managing multiple remote client nodes.
2. **State Synchronization:** Ensuring all players and the admin see the exact same game state at the same time.
3. **Concurrency:** Handling multiple simultaneous game rooms and database transactions.
4. **Event-Driven IPC:** Inter-Process Communication using Socket.IO events for low-latency updates.
5. **Transparency:** Location transparency for the database and AI processing logic.

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Real-time:** Flask-SocketIO (WebSockets)
- **Database:** SQLite & SQLAlchemy
- **Security:** Flask-Bcrypt (Password hashing)
- **Frontend:** HTML5, JavaScript (ES6), Tailwind CSS

---

## 📋 Installation & Setup

### 1. Clone the environment

# Navigate to project folder
cd tictactoe-server

# Activate virtual environment
.\venv\Scripts\activate

### 2. Install Dependencies

pip install flask flask-socketio flask-sqlalchemy flask-login flask-bcrypt eventlet

### 3. Initialize Database & Admin

# This script creates the SQLite database and a default admin account.

python seed.py

Default Admin: admin
Default Password: ishi123

### 4. Run the Server

python run.py

# The server will start at http://localhost:5000.

### 🌐 How to Connect Other Devices
To demonstrate the Distributed nature, follow these steps to connect a second device (Phone/Laptop):
Find your Local IP: Open a terminal and type ipconfig. Note the IPv4 Address (e.g., 192.168.1.15).
Open Firewall: Ensure your Windows Firewall allows python.exe through.
Access URL: On the second device, enter:
http://<YOUR_IP_ADDRESS>:5000/game/lobby

### 🎮 Usage Guide
Admin: Access http://localhost:5000/ishi to monitor the network.
Player: Access http://localhost:5000/game/lobby to join the game.
Matchmaking: Click "Find Online Player" on two different devices to be paired.

### Tip for  Presentation:
Use a tool like **Ngrok** (which you already installed) to generate a public link. 
1. Run `python run.py`.
2. In a second terminal, run `ngrok http 5000`.
3. Give the `https://...` link to your teacher. 
4. They can join the game from their own computer anywhere, which looks **extremely impressive** for a Distributed Systems project!

### Ngrok GUIDE
get ur auth here: https://dashboard.ngrok.com/get-started/your-authtoken

### 🌐 Remote Testing Guide (Ngrok Tunneling)
To demonstrate this as a true distributed system, follow these steps to connect multiple devices (Phone, Laptop, Tablet) from any network using Ngrok.
### 1. Start the Flask Server (Terminal A)

This terminal acts as the Host. It manages the database and the game logic.
Open your terminal in the project folder.
Activate your virtual environment: .\venv\Scripts\activate
Run the server: python run.py
Status: You should see wsgi starting up on http://0.0.0.0:5000

### 2. Start the Ngrok Tunnel (Terminal B)
This terminal creates a secure "bridge" from the internet to your laptop.
Open a second terminal window.
Ensure you have added your authtoken (only needed once):
ngrok config add-authtoken <YOUR_TOKEN>
Start the tunnel:
ngrok http 5000

Copy the Forwarding URL provided (e.g. https://<YOUR_NGROK_ID>.ngrok-free.app/game/lobby)

### 📱 How to Connect Devices
Device	Role	URL to Visit
Main Laptop	Admin Monitor	http://localhost:5000/ishi
Secondary Laptop	Player 1	https://<YOUR_NGROK_ID>.ngrok-free.app/game/lobby
Smartphone	Player 2	https://<YOUR_NGROK_ID>.ngrok-free.app/game/lobby
Note: When opening the Ngrok link on a phone for the first time, you may see a "Warning" page. Click "Visit Site" to proceed to the game.

#DETAILED STEP BY STEP
1. Locate tictactoe-server folder
2. Open terminal there
3. run .\venv\Scripts\activate
4. python seed.py (This script creates the database schema and a default administrator.)
5. python run.py (only on flask or 1 terminal)or Terminal A
6. Terminal B: Run ngrok http 5000
7. Connect: Use the https://... link provided by Ngrok.
   in my case itsL https://getaway-unmixable-data.ngrok-free.dev/game/lobby
