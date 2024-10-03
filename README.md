# 🏰 Stacy V2 - Minecraft Server Status Bot ⚔️🎮

**Stacy V2** is a cute, cool, and powerful Discord bot designed to fetch and display the status of both **Java** and **Bedrock** Minecraft servers with stylish, colorful embeds! Powered by the `mcstatus.io` API, Stacy V2 provides real-time updates on player counts, server versions, and lets you know if your server is online or offline. You can even add your custom server image for a personalized touch!

## 🚀 Features

- 🌍 **Java & Bedrock Server Support**: Quickly check status for both server types with one command.
- 🎨 **Stylish Embeds**: Get clean, visually appealing, and fully customizable status displays.
- 👥 **Live Player Count**: Instantly see how many players are currently online and the max server capacity.
- 🛠️ **Version Info**: Displays the Minecraft server version, including if it's outdated or the latest.
- 🖼️ **Customizable Image**: Add your server logo or banner directly into the status embed for personalization.
- ⚠️ **Error Handling**: Provides clear error messages when there’s an issue fetching server data (e.g., invalid IP).
- 🔄 **Automatic Refresh**: Stacy can refresh server status at regular intervals, providing real-time updates.
- 🎮 **Server Connection Instructions**: Users can add their own instructions for connecting to the server, visible in the embed.

## 🔧 Setup Guide

### Prerequisites

Before you start, ensure you have the following installed:

- 🐍 **Python 3.8+**: [Download here](https://www.python.org/downloads/)
- 🤖 **Discord Bot Token**: Create your bot and get a token from the [Discord Developer Portal](https://discord.com/developers/applications)
- 📦 Python Libraries: Install the required libraries using `pip`
    - `discord`
    - `requests`
    - `dotenv`

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/oxyzox/stacy-v2.git
    cd stacy-v2
    ```

2. **Install dependencies**:

    Install all the required libraries with the following command:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:

    Create a `.env` file in the project directory and add your Discord bot token:

    ```bash
    TOKEN=your-discord-bot-token-here
    ```

4. **Run the bot**:

    Start the bot by running the following command:

    ```bash
    python main.py
    ```

### 🎮 Usage

Once Stacy V2 is running, you can use the following command to get the status of any Minecraft server:

- `/status <server_type> <server_ip> [image_url] [connection_instructions]`

**Options:**
- `server_type`: Choose between `Java` or `Bedrock`.
- `server_ip`: Provide the IP address of the Minecraft server you want to check.
- `image_url`: (Optional) Add a URL to display a custom image in the embed (like your server logo).
- `connection_instructions`: (Optional) Add any instructions or a guide on how to connect to your Minecraft server.

#### Example:

- `/status <java> <play.projectmc.fun> [ https://example.com/logo.pnl] ["Use play.projectmc.fun to connect!"]`


This will return a beautiful embed with the server status, player count, server version, and any additional info or images you provide!

### Customizing the Embed

Stacy allows users to add a personal touch to the embed using an image and custom connection instructions. You can add your server's logo, a banner, or even instructions to help new players connect.

## 🔄 Automatic Status Refresh

To make sure your server's status stays up-to-date, Stacy refreshes the information every few minutes. You can customize the refresh interval in the bot's code by adjusting the scheduling logic.

## 🤝 Contributing

Want to add new features or fix bugs? Feel free to fork this repository, create a new branch, and submit a pull request! Contributions are highly appreciated. For major changes, please open an issue to discuss what you would like to add.

1. **Fork the repository**
2. **Create a branch**
3. **Submit a Pull Request**

## ❤️ Credits

- Developed by **oxyzox**
- Powered by the awesome **mcstatus.io API**

Enjoy the bot? Give it a ⭐ on GitHub to show your support!
