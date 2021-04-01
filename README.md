<p align="center">
<img src="assets/githubfeedbot.png" width="60%">
</p>
<p align="center">
<strong>Follow RSS/Atom feeds on telegram <img src="assets/tellogo.png" width="20px" height="20px" alt="Telegram"></a></strong>
</p>
<h3 align="center">
<a href="#contributions">Contribute</a>
<span> · </span>
<a href="#documentation">Documentation</a>
<span>  · </span>
<a href="#todo">Todo</a>
</h3>
<p align="center"><b><a href="https://t.me/genrssbot">https://t.me/genrssbot</a></b></p>

---

## Documentation
Bot is built using [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). 

Currently bot supports 5 commands

- ```/start``` and ```/help``` : Prints out all available commands and what they do.

- ```/add``` : Gets a url from the user and finds if there is any rss/atom feed in that url. Distinction here is that bot doesn't ask for a feed directly, it finds the feed for you. You can just drop the youtube channel link, homepage of subreddit or a blog, if there is a valid rss/atom feed it'll be added to the file ```chat_id_feed```. It also checks if the feed is already stored to mitigate duplicacy.

- ```/show``` : Prints out a list of all the feeds added so far by the user. You can use this option to implement a  __```/delete```__  feature, so that user knows what all is there and can be deleted.

- ```/update``` : Checks for new updates in all the feeds added by a user and returns atmost 4 newest results per feed. Also notifies if there is no new update.
- ```/delete``` : Used with ```/show``` to delete a feed set by user from the records.

- Autoupdate is set to a custom interval of 1 hour

---
## Demo run

<p align="center">
<img src="assets/new-bot.gif" width="60%">
</p>

---

## Contributions

- Bot is open to contributions, but I recommend creating an issue or replying in comments to let me know what you are working on first. So
 that we don't overwrite each other.

 
### Setup or Selfhosting

- Clone the repo
```
git clone https://github.com/nikhil1raghav/rssbot.git
```

- You must have ```pip``` installed, it makes life easier while installing dependencies.

- Bot has following dependencies
	- feedparser
	- feedfinder2
	- pyTelegramBotAPI
	- sqlite3

- Install them manually by using package manager for your distribution, or if you have ```pip```, you can use
```
pip install -r requirements
```
- Chat with botfather to get an ```API_KEY```, replace it with text ```API_KEY``` in ```rssbot.py```

- Run the bot 

```
python rssbot.py
```
- NOTE : If you're on ubuntu you may have to write ```pip3``` instead of ```pip``` and ```python3``` instead of ```python```.



## Todo

There are some features that you can work on, list is not at all comprehensive.

- [x] Deleting feeds with `/delete`
- [x] managing everything in a database
- [x] Autoupdate feeds at a custom interval
- [ ] Keeping messages per user from blowing up
- [ ] An option to set custom update interval for every feed
- [ ] Encrypting feed urls stored on server for privacy

 

