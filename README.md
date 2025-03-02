# Roblox Price Floor Bot 👆👇

This bot automatically fetches and posts **Roblox price floor updates** to Bluesky every 15 minutes using GitHub Actions. It tracks price changes for various UGC items and ensures the latest data is shared.

## 📌 Features
- ✅ Fetches **Roblox price floors** from the API.
- ✅ Detects and logs **price changes**.
- ✅ Posts updates to **Bluesky** when changes occur.
- ✅ Runs **automatically** using GitHub Actions.
- ✅ Stores historical data in `roblox_price_history.json`.

## ⚙️ Installation & Setup

1. **Clone the repository**  
   ```sh
   git clone https://github.com/YOUR_USERNAME/roblox-price-floor-bot.git
   cd roblox-price-floor-bot
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up environment variables**

   Rename the `.env.example` to `.env` and fill in the information
   - `BLUESKY_USERNAME`=HANDLE FOR SAID BLUESKY ACCOUNT
   - `BLUESKY_PASSWORD`=[APP PASSWORD](https://bsky.app/settings/app-passwords)
   - `ROBLOX_COOKIE`=ROBLOX SESSION COOKIE
4. **Run the script**
   ```sh
   python index.py
   ```
## 📜 License
This project is licensed under the MIT License. See LICENSE for details.


Made with 💖 by ScrapBlox