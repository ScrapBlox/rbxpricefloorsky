import os
import requests
import json
from atproto import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bluesky credentials
BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")

# Roblox authentication cookie
ROBLOX_COOKIE = os.getenv("ROBLOX_COOKIE")

# File to store previous price data
PRICE_HISTORY_FILE = "roblox_price_history.json"

# Create a Bluesky client
client = Client("https://bsky.social")

# Fetch Roblox price floor data with authentication
def fetch_roblox_price_floors():
    url = "https://itemconfiguration.roblox.com/v1/collectibles/metadata"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print("⚠️ Unauthorized (401). Your .ROBLOSECURITY cookie may be invalid or expired.")
        return {}
    elif response.status_code != 200:
        print(f"⚠️ Failed to fetch data. Status Code: {response.status_code}")
        return {}

    try:
        data = response.json()
        return {item: details["priceFloor"] for item, details in data["unlimitedItemPriceFloors"].items()}
    except json.JSONDecodeError:
        print("⚠️ Error decoding JSON response from Roblox API.")
        return {}


# Load previous price data
def load_previous_prices():
    if os.path.exists(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE, "r") as file:
            return json.load(file)
    return {}


# Save the latest prices
def save_prices(prices):
    with open(PRICE_HISTORY_FILE, "w") as file:
        json.dump(prices, file)


# Compare prices to determine changes
def compare_prices(old_prices, new_prices):
    increases, decreases, no_changes = [], [], []

    for item, new_price in new_prices.items():
        old_price = old_prices.get(item)

        if old_price is None:
            no_changes.append(f"• {item.replace('Accessory','')}: {new_price}")
        elif new_price > old_price:
            increases.append(f"• {item.replace('Accessory','')}: {new_price} (↑{new_price - old_price})")
        elif new_price < old_price:
            decreases.append(f"• {item.replace('Accessory','')}: {new_price} (↓{old_price - new_price})")
        else:
            no_changes.append(f"• {item.replace('Accessory','')}: {new_price}")

    return increases, decreases, no_changes


# Format the Bluesky post
def format_post(increases, decreases, no_changes):
    post = f"Roblox Price Floors #Roblox\n"

    post += "⬆️ Increase\n" + ("\n".join(increases) if increases else "• N/A") + "\n"
    post += "⬇️ Decrease\n" + ("\n".join(decreases) if decreases else "• N/A") + "\n"
    post += "🔄 No Change\n" + "\n".join(no_changes)

    return post[:300]  # Ensure within Bluesky character limit


# Post update to Bluesky
def post_to_bluesky(content):
    client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
    client.send_post(content)
    print("✅ Posted to Bluesky!")


# Main function
def main():
    old_prices = load_previous_prices()
    new_prices = fetch_roblox_price_floors()

    # If fetching data failed, just print an error instead of posting
    if not new_prices:
        print("⚠️ No data fetched. Skipping Bluesky post.")
        return

    increases, decreases, no_changes = compare_prices(old_prices, new_prices)

    if old_prices == {}:
        print("none")
        post_content = format_post(increases, decreases, no_changes)
        post_to_bluesky(post_content)
    else:
        print("something")

    # Post only if changes occurred
    if increases or decreases:
        post_content = format_post(increases, decreases, no_changes)
        post_to_bluesky(post_content)
    else:
        print("ℹ️ No changes detected. No post needed.")

    # Save the latest prices
    save_prices(new_prices)

if __name__ == "__main__":
    main()
