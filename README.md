# Nandha-UserBot

**Nandha-UserBot** is a simple, lightweight, and efficient Telegram UserBot built using the **Pyrogram** framework. This repository is designed for personal use, allowing you to automate tasks, create custom commands, and enhance your Telegram experience. Whether you're a beginner or an experienced developer, you can easily customize this UserBot to suit your needs or contribute to its development.

---

## Features

- **Lightweight and Fast**: Built with Pyrogram, ensuring smooth performance and low resource usage.
- **Customizable**: Easily modify or extend the bot's functionality to fit your requirements.
- **Personal Use**: Designed for individual use, but can be adapted for group or channel management.
- **Open Source**: Feel free to contribute, fork, or modify the code as per your needs.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Telegram API ID and Hash from [my.telegram.org](https://my.telegram.org)
- Git (for cloning the repository)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/nandhaxd/nandhauserbot.git
   cd nandhauserbot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**:
   - Rename `config_sample.py` to `config.py`.
   - Open `config.py` and fill in your Telegram API ID, API Hash, and other required details.

4. **Run the UserBot**:
   ```bash
   python3 -m nandha
   ```

---

## Customization

You can easily customize the bot by adding new plugins or modifying existing ones. All plugins are located in the `plugins` directory. To create a new plugin:

1. Create a new Python file in the `plugins` directory.
2. Use the Pyrogram framework to define your commands or handlers.
3. Import your plugin in the main bot file to enable it.

Example Plugin:
```python
from pyrogram import filters
from nandha import app, HELP

HELP['hello'] = 'Just Say hello!'
@app.on_message(filters.command("hello"))
async def hello(client, message):
    await message.reply("Hello! How can I help you?")
```

---

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request with a detailed description of your changes.

---

## Support

For any questions, issues, or feature requests, feel free to reach out:

- **Telegram**: [@NandhaBots](https://t.me/nandhaBots)
- **GitHub Issues**: [Open an Issue](https://github.com/nandhaxd/nandhauserbot/issues)

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments

- **Pyrogram**: For providing an excellent framework to build Telegram bots.
- **Telegram**: For their robust API and platform.

---

Enjoy using **Nandha-UserBot**! If you find it useful, consider giving it a ⭐ on GitHub!
