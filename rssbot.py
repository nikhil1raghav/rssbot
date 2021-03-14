import telebot
from feedfinder2 import find_feeds
from telebot import types
import feedparser
bot=telebot.TeleBot("API_KEY",parse_mode=None)




@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id,"type /add <your url here>to add a feed\nUrl can be any\n1.Website or personal blog\n2.Subreddit\n3.Youtube channel link\nThat you want to follow\nNOTE:Don't send feed links, I'll extract the links myself for you, just drop the url\ntype /show to look at the names of the feeds you have added so far\ntype /update to get all updates")


@bot.message_handler(commands=['add'])
def add_feed(message):
    cid=message.chat.id
    print(f"chatting with {cid}");
    msg=message.text
    url=msg[4:]
    url=url.strip()
    if "reddit.com" in url:
        if  url[-1]!='/':
            url=url+'/'
        feeds=[url+'.rss']
    else:
        feeds=find_feeds(url)
    ans=""
    if len(feeds)==0:
        ans="Oops! No feeds found, try another link"
    else:
        f=open(f"users/{cid}_feed","a")
        f.close()
        old_feeds=open(f"users/{cid}_feed").readlines()
        f=open(f"users/{cid}_feed","a")
        if f"{feeds[0]}\n" in old_feeds:
            ans=f"This feed already exists in your collection"
        else:
            ans=f"Feed {feeds[0]} added successfully"
            f.write(f"{feeds[0]}\n")
        f.close()
    bot.send_message(cid,ans)


@bot.message_handler(commands=['show'])
def show_feedfile(message):
    cid=message.chat.id
    f=open(f"users/{cid}_feed","a")
    f.close()
    feeds=open(f"users/{cid}_feed").readlines()
    ans=""
    if(len(feeds)==0):
        ans="No feeds to show, try adding some by /add <your url here> command"
    else:
        ans+=f"Total {len(feeds)}\n"
        for i in feeds:
            d=feedparser.parse(i)
            ans+=f"{d.feed.title}\n"
    
    bot.send_message(cid,ans)


@bot.message_handler(commands=['update'])
def update(message):
    cid=message.chat.id
    f=open(f"users/{cid}_feed","a")
    f.close()
    f=open(f"users/{cid}_msgs","a")
    f.close()
    feeds=open(f"users/{cid}_feed").readlines()
    oldmsgs=open(f"users/{cid}_msgs").readlines()
    oldmsgs=set(oldmsgs)
    oldfile=open(f"users/{cid}_msgs","a")
    ans=""
    if(len(feeds)==0):
        ans="No feeds to show, try adding some by /add <your url here> command"
        bot.send_message(cid, ans)
    else:
        for i in feeds:
            d=feedparser.parse(i)
            num=0
            sent=0
            for ent in d.entries:
                num+=1
                if(num>4):
                    break
                ans=""
                if f"{ent.link}\n" in oldmsgs:
                    break
                sent=1
                oldfile.write(f"{ent.link}\n")
                ans+=f"{d.feed.title}\n"
                if 'title' in ent:
                    ans+=f"{ent.title}\n"

                if 'link' in ent:
                    ans+=f"{ent.link}\n"


                bot.send_message(cid, ans)
            if sent==0:
                ans=f"No new updates in {d.feed.title}, check back later"
                bot.send_message(cid,ans)
    oldfile.close()



bot.polling()
