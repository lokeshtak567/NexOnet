# 📡 NexOnet - Auto WiFi Portal Login Utility

A GUI-based tool developed in Python using Tkinter and PyWiFi to automate the process of detecting and logging into captive WiFi portals, especially for college networks. The tool continuously scans for networks, connects to available ones, logs in, and ensures a stable internet connection.

---

## 🛠 Features

- ✅ GUI with custom graphics 
- 📶 Scans and connects to the strongest available WiFi networks
- 🔐 Auto-login to a captive portal with username and password cycling
- 🌐 Internet connectivity check and re-login if disconnected
- 📜 Logging of errors and actions into a `log.txt` file
- 🧪 Integrated multi-threaded design (future support)

---

## 📁 Project Structure

```
NexOnet/
├── runner.py             # Main GUI script (launch this)
├── wifiexploit.py        # Backend logic for WiFi scanning and login
├── log.txt               # Runtime logs (generated at execution)
└── resources/            # Image assets used in the GUI
    ├── background.png
    ├── start.png
    ├── autorun.png
    ├── credits.png
    ├── credits_screen.png
    ├── logo1.png
    ├── logo2.png
    ├── source.png
    └── update.png
```

---

## 🚀 Getting Started

### 1. Requirements

- Python 3.x
- Modules: `pywifi`, `requests`

Install dependencies:

```bash
pip install pywifi requests
```

### 2. Run the GUI

```bash
python runner.py
```

> Ensure the `resources/` folder with image files is present in the same directory.

---

## 🔐 Login System Logic

- Disconnects from current WiFi
- Scans and connects to the strongest open college WiFi
- Attempts login with default user `event/Event@123`
- On failure, cycles through predefined usernames from `working_Id` list

---

## 👥 Credits

Made by a group of passionate developers Lokesh, Rudra, Vaishnavi, Atharva as a utility for automating captive WiFi login experiences in educational institutions.

---

## 📜 License

This project is intended for educational use only. Use responsibly and only on networks you are authorized to access.
