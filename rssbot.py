import telebot
import threading
from feedfinder2 import find_feeds
from telebot import types
import sqlite3
from sqlite3 import Error
import feedparser
bot=telebot.TeleBot("YOUR_API_KEY",parse_mode=None)
db=r"bot.db"




WAIT_SECONDS=3600
def auto_update():
    """Will work in a separate thread to auto_update feeds"""
    conn=sqlite3.connect(db)
    c=conn.cursor()
    
    c.execute("select id from allUsers;")
    users=c.fetchall()

    for user in users:
        cid=user[0]
        userfeed=f"feeds{cid}"
        sentfeed=f"sent{cid}"
        create_table_sent="""
        create table if not exists """+sentfeed+"""(
        id integer primary key,
        postlink text not null unique
        );
         """
        c.execute(create_table_sent)
        conn.commit()

        c.execute("select feedName from "+userfeed+";")
        allfeeds=c.fetchall()
        for feed in allfeeds:
            num=0
            feedlink=feed[0]
            d=feedparser.parse(feedlink)
            title=feedlink
            if 'title' in d.feed:
                title=d.feed.title
            for ent in d.entries:
                num+=1
                if(num>4):
                    break
                link=ent.link
                c.execute("select postlink from "+sentfeed+" where postlink='"+link+"' ;")
                exists=c.fetchall()
                if len(exists)>0:
                    break
                else:
                    ans=f"{title}\n{link}"
                    bot.send_message(cid,ans)
                    c.execute("insert into "+sentfeed+" (postlink) values(?)",(link,));
                    conn.commit()

    threading.Timer(WAIT_SECONDS, auto_update).start()


@bot.message_handler(commands=['start','help'])
def send_welcome(message):
        bot.send_message(message.chat.id,"type /add <your url here>to add a feed\nUrl can be any\n1.Website or personal blog\n2.Subreddit\n3.Youtube channel link\nThat you want to follow\nNOTE:No need to send feed links, I'll extract the links myself for you, just drop the url. In case you have a feed url, it'll also work\ntype /show to look at the names of the feeds you have added so far\ntype /update to get all updates\n/delete <feednumber> to delete a feed\n\n autoupdate is on, you'll receive updates every hour for all the feeds")


@bot.message_handler(commands=['add'])
def add_feed(message):
    cid=message.chat.id
    conn=sqlite3.connect(db)
    c=conn.cursor()
    userfeed=f"feeds{cid}"
    create_table="""
    create table if not exists """+userfeed+"""(
        id integer primary key,
        feedName text not null unique
    );
    """
    sentfeed=f"sent{cid}"
    create_table_sent="""
    create table if not exists """+sentfeed+"""(
        id integer primary key,
        postlink text not null unique
    );
    """
    c.execute(create_table_sent)
    conn.commit()




    c.execute(create_table);
    conn.commit()
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
        c.execute("select * from allUsers where id="+str(cid)+";")
        userexists=c.fetchall();
        c.execute("select * from "+userfeed+" where feedName='"+feeds[0]+"';")
        feedexists=c.fetchall();
        if len(userexists)==0:
            c.execute("insert into allUsers values(?)",(int(cid),))
        if len(feedexists)==0:
            c.execute("insert into "+userfeed+" (feedName) values(?)",(feeds[0],))
            ans=f"feed {feeds[0]} added successfully"
        else:
            ans=f"feed {feeds[0]} already added"
        conn.commit()
    conn.close()
    bot.send_message(cid,ans)


@bot.message_handler(commands=['delete'])
def delete_feed(message):
    cid=message.chat.id
    msg=message.text
    num=msg[7:]
    num=num.strip()
    if len(num)==0:
        bot.send_message(cid,"""1. type /show to find the number of the feed you want to delete\n
        2. After that type /delete <feed number> to delete the feed with that number\n""")
        return

    num=int(num)
    userfeed=f"feeds{cid}"
    create_table="""
    create table if not exists """+userfeed+"""(
        id integer primary key,
        feedName text not null unique
    );
    """

    conn=sqlite3.connect(db)
    c=conn.cursor()
    c.execute(create_table)
    c.execute("select * from allUsers where id="+str(cid)+";")
    userexists=c.fetchall()
    if len(userexists)==0:
        bot.send_message(cid,"You don't have any feeds to delete")
        return
    

    c.execute("select rowid,feedName from "+userfeed+" ;");
    results=c.fetchall()

    if len(results)==0:
        bot.send_message(cid,"You don't have any feeds, try adding some by /add <your url here>")
        return

    d={}
    cur=1
    for i in results:
        d[cur]=i[0]
        cur+=1

    l=len(results)

    if num>l or num<1:
        bot.send_message(cid,f"No feed with number {num}\ntype /show and look again")
        return
    c.execute("delete from "+userfeed+" where rowid="+str(d[num])+";")
    bot.send_message(cid, f"feed deleted successfully")
    conn.commit()
    conn.close()


@bot.message_handler(commands=['show'])
def show_feedfile(message):
    cid=message.chat.id
    userfeed=f"feeds{cid}"
    create_table="""
    create table if not exists """+userfeed+"""(
        id integer primary key,
        feedName text not null unique
    );
    """

    conn=sqlite3.connect(db)
    c=conn.cursor()
    
    c.execute(create_table)
    c.execute("select * from allUsers where id="+str(cid)+";")
    userexists=c.fetchall()
    if len(userexists)==0:
        bot.send_message(cid,"you don't have any feeds\ntry adding some by /add <your url here>")
        return

    c.execute("select feedName from "+userfeed+" ;");
    results=c.fetchall()



    ans=""
    if(len(results)==0):
        ans="No feeds to show, try adding some by /add <your url here> command"
    else:
        ans+=f"Total {len(results)}\n"
        cur=1
        for i in results:
            ans+=f"{cur}. {i[0]}\n"
            cur+=1
    conn.close()
    
    bot.send_message(cid,ans)



@bot.message_handler(commands=['update'])
def update(message):
    cid=message.chat.id
    userfeed=f"feeds{cid}"
    create_table="""
    create table if not exists """+userfeed+"""(
        id integer primary key,
        feedName text not null unique
    );
    """

    conn=sqlite3.connect(db)
    c=conn.cursor()
    
    c.execute(create_table)
    c.execute("select * from allUsers where id="+str(cid)+";")
    userexists=c.fetchall()
    if len(userexists)==0:
        bot.send_message(cid,"you don't have any feeds\ntry adding some by /add <your url here>")
        return
    

    c.execute("select feedName from "+userfeed+";")
    feeds=c.fetchall()

    if len(feeds)==0:
        bot.send_message(cid,"you don't have any feeds\ntry adding some by /add <your url here>")
        return

    sentfeed=f"sent{cid}"
    create_table_sent="""
    create table if not exists """+sentfeed+"""(
        id integer primary key,
        postlink text not null unique
    );
    """
    c.execute(create_table_sent)
    conn.commit()




    
    for i in feeds:
        feedlink=i[0]
        d=feedparser.parse(feedlink)
        title=i
        if 'title' in d.feed:
            title=d.feed.title
        sent=0
        num=0
        for ent in d.entries:
            num+=1
            if(num>4):
                break
            link=ent.link
            c.execute("select postlink from "+sentfeed+" where postlink='"+link+"' ;")
            exists=c.fetchall()
            if len(exists)>0:
                break
            else:
                ans=f"{title}\n{link}"
                bot.send_message(cid,ans)
                c.execute("insert into "+sentfeed+" (postlink) values(?)",(link,));
                conn.commit()
                sent=1
        if sent==0:
            bot.send_message(cid, f"No new updates in {title}")

    conn.close()




conn=sqlite3.connect(db)
c=conn.cursor()
create_user_table="""
    create table if not exists allUsers(
        id integer primary key
    );
    """
c.execute(create_user_table);
conn.commit();
conn.close()
auto_update()
bot.polling()
