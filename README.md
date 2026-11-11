# Be Bot

`Be Bot` or `Бе Бот` is a customizable Telegram bot 
that sends a specific image in response to any message containing at least one of the words 
specified in the settings. 
The default configuration includes only `бе`, `be`, and `бэ`, all of which trigger the same image.

Currently available only in Russian.
Licensed under MIT.

Official bot: https://t.me/FufubekBot

## Installing

1. Clone the repository:
```bash
git clone https://github.com/cocoalabs-project/BeBot
cd BeBot
```

2. Install the library:
```bash
pip install aiogram
```

3. Rename `config.json.example` to `config.json` and edit the settings in that file
(or leave it as is)


4. Run the main.py:
```bash
BEBOT_TOKEN="token" python3 ./main.py 
# You can also use the `BEBOT_CONFIG_PATH` variable to specify the path to the configuration file
```

**Please note that it is recommended to set up the bot as a service in your init system 
(if using systemd, it is preferable to use systemd credentials to store the token in a separate file).**
