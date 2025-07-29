# NexOnet

**NexOnet** is a modern, intelligent WiFi captive portal automation utility designed exclusively for college networks. Created and maintained by **Lokesh Tak** and **Rudra Sharma**, NexOnet eliminates the hassle of logging in and maintaining a captive portal session so you can stay focused on your work, not your WiFi.

## 🚀 Features

- **Automated Captive Portal Login:** Seamless connection with your college WiFi. No more manual logins!
- **Ad Block Integration:** Instantly switches your DNS to public resolvers (Cloudflare & Google) to block most ads and trackers at a network level.
- **System Tray Integration:** Clean, non-intrusive tray notifications and controls. NexOnet runs quietly in the background.
- **Auto-Connect Mode:** Enable it once, and NexOnet takes care of your connection every time your device is in range.
- **User-Friendly GUI:** Modern PyQt-based interface with real-time status and controls. You don’t need to be a techie.
- **Robust Session Management:** Automatically re-establishes dropped connections and logs out gracefully.
- **Admin Awareness:** Ad block features prompt for admin privileges for best security and reliability.
- **Persistent Settings:** Saves your preferences and toggle states across restarts.
- **Minimal, Stylish, and Ultra-Lightweight:** No bloat, pure productivity.

## 🌟 Screenshots

> _Add screenshots here for an even more stunning README!_  
> (E.g., NexOnet main window, connection status, tray notification, toggles, etc.)

## 🏁 Getting Started

### 1. **Clone the repository**

git clone https://github.com/lokeshtak567/NexOnet.git
cd NexOnet


### 2. **Install Python Requirements**

Ensure you have Python 3.8+ installed.

### 3. **Run the Application**


## ⚙️ How It Works

- **Captive Portal Detection:**  
Periodically probes your college gateway for login prompts. If detected, randomly picks a user ID, sends credentials, and confirms connection success.

- **Auto Connect & Ad Block Toggles:**  
Custom toggle switches enable/disable features on-the-fly, with admin-check for network-level DNS changes.

- **Tray & Persistence:**  
Safely minimizes to the tray on close. Restores settings and re-launches auto-connect on start, if enabled.

## 🛠️ Configuration & Customization

- **ID Pool:**  
Customize or expand your user ID list in the `idpool` variable in `main.py`.

- **DNS Servers:**  
The Ad Block toggle uses Cloudflare (`1.1.1.1`) and Google DNS (`8.8.8.8`). Edit `dns_servers` in `handle_ad_block` for different resolvers.

- **Portal URLs:**  
Target and endpoint URLs are embedded for your network (`http://172.16.35.1:8090`). Adjust in the worker thread if your college uses a different portal address.

## 💡 Pro Tips

- **Run as Administrator** for ad-blocker to work effectively.
- **Bring Your Own Logo!** Put your custom logo at `logo.ico` and `logo.png` in the root directory for a personalized look.
- **Experiencing issues?** Use the console for logs or tweak the timeouts for slower college networks.

## 🙌 Authors

- **Lokesh Tak**  
- **Rudra Sharma**

Proudly built for the student community, by fellow students! ✨

## ❤️ Contributing

Feedback, pull requests, and ideas are welcome!  
Fork the repo and share your improvements.

## 📜 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

## ⭐ Star this project!

If NexOnet saved you time or made your WiFi experience better, don’t forget to ⭐ star the repo and share with your friends!
