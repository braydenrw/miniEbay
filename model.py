import web
import time
import datetime
from datetime import timedelta

db = web.database(dbn='sqlite', db='./MiniEbay.db')
time_format = '%Y-%m-%d %H:%M:%S'

def get_items():
    return db.select('item')


def get_select_item(idnumber, category, title, description, minprice, maxprice, isopen):
    if minprice == '' and maxprice == '':
        return db.select('item',
                         where='categories like \'%' + category + '%\' and description like \'%' + description + '%\'' +
                               ' and title like \'%' + title + '%\'' + ' and open like \'%' + isopen + '%\'' + ' and id like \'%' + idnumber + '%\'')
    elif minprice == '':
        return db.select('item',
                         where='categories like \'%' + category + '%\' and description like \'%' + description + '%\'' +
                               ' and title like \'%' + title + '%\'' + ' and open like \'%' + isopen + '%\'' +
                               ' and price <=' + maxprice + ' and id like \'%' + idnumber + '%\'')
    elif maxprice == '':
        return db.select('item',
                         where='categories like \'%' + category + '%\' and description like \'%' + description + '%\'' +
                               ' and title like \'%' + title + '%\'' + ' and open like \'%' + isopen + '%\'' +
                               'and price >=' + minprice + ' and id like \'%' + idnumber + '%\'')
    else:
        return db.select('item',
                         where='categories like \'%' + category + '%\' and description like \'%' + description + '%\'' +
                               ' and title like \'%' + title + '%\'' + ' and open like \'%' + isopen + '%\'' +
                               ' and price <=' + maxprice + ' and price >= ' + minprice + ' and id like \'%' + idnumber + '%\'')


def get_categories():
    try:
        return db.select('categories', what='name').list()
    except IndexError:
        return None


def get_item(idno):
    try:
        return db.select('item', where='id=$idno', vars=locals())[0]
    except IndexError:
        return None


def get_highest_bid(idno):
    try:
        return db.select('bid', where='id=$idno', vars=locals(), order='price DESC')[0]
    except IndexError:
        return db.select('item', where='id=$idno', vars=locals())[0]


def new_bid(idno, buyer, price):
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    db.insert('bid', id=idno, buyer=buyer, price=price, bid_time=date)


def update_current_bid(bid, idno, user_name):
    db.update('item', where='id=' + idno, price=bid, winner=user_name)


def new_category(category):
    db.insert('categories', name=category)

time_format = '%Y-%m-%d %H:%M:%S'
def new_item(category, title, description, price):
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    date_1 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    end_date = date_1 + datetime.timedelta(days=14)

    db.insert('item', categories=category, title=title, description=description, price=price,
              open=1, end_date=end_date)


def get_bids(idno):
    if get_item(idno) is None:
        return None
    else:
        return db.select('bid', where='id=$idno', vars=locals(), order='price DESC')


def set_time(setTime):
    db.update('time', where="1=1", current_time=setTime)

def get_current_time():
    time_string = db.select('time')[0].current_time
    return datetime.datetime.strptime(time_string, time_format)

def reset_time():
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    db.update('time', where="1=1", current_time=date)
