import web
import model
import cgi
import datetime
# import cgitb; cgitb.enable()
from web import form

urls = (
    '/', 'index',
    '/bid/(\d+)', 'Bid',
    '/sell/', 'Sell',
    '/time/', 'Time',
)

render = web.template.render('templates/')
db = web.database(dbn='sqlite', db='./MiniEbay.db')


class index:
    def GET(self):
        categories = db.select('categories', what='name').list()
        items = model.get_items()
        return render.index(items, categories)

    def POST(self):
        categories = db.select('categories', what='name').list()
        data = web.input()
        try:
            data.Submit1
        except AttributeError:
            submit1 = None
        else:
            submit1 = data.Submit1
        if submit1 is not None:
            category = data.category
            title = data.title
            minprice = data.minprice
            maxprice = data.maxprice
            description = data.description
            isopen = data.isopen
            idnumber = data.idnumber
            item = model.get_select_item(idnumber, category, title, description, minprice, maxprice, isopen)
            return render.index(item, categories)


class Bid:
    def GET(self, idno):
        item = model.get_item(int(idno))
        bids = model.get_bids(int(idno))
        highestbid = model.get_highest_bid(int(idno))
        return render.bid(item, bids, idno, highestbid.price)

    def POST(self, idno):
        data = web.input()
        username = data.username
        bid = data.newbid
        highestbid = model.get_highest_bid(int(idno))
        itemis = model.get_item(int(idno))
        if itemis.open == 1 and float(highestbid.price) < float(bid):
            model.new_bid(idno, username, bid)
            model.update_current_bid(bid, idno, username)

        bids = model.get_bids(int(idno))
        item = model.get_item(int(idno))
        return render.bid(item, bids, idno, highestbid.price)

class Sell:
    def GET(self):
        categories = db.select('categories', what='name').list()
        return render.sell(categories)

    def POST(self):
        categories = db.select('categories', what='name').list()
        data = web.input()
        try:
            data.Submit2
        except AttributeError:
            submit2 = None
        else:
            submit2 = data.Submit2
        if submit2 is not None:
            categories = model.get_categories()
            category = data.category
            title = data.itemname
            description = data.description
            price = data.price
            categories_by_name = list(category_c.name for category_c in categories)
            if category not in categories_by_name:
                model.new_category(category)
            model.new_item(category, title, description, price)
            categories = model.get_categories()
            return render.sell(categories)

class Time:
    def __init__(self):
        pass

    def GET(self):
        currentTime = model.get_current_time()
        time = str(currentTime)
        return render.time(time)

    def POST(self):
        data = web.input();
        try: 
            submit1 = data.Submit1
        except AttributeError:
            submit1 = None 

        try: 
            submit2 = data.Submit2
        except AttributeError:
            submit2 = None

        if submit1 is not None:
            year = data.year
            month = data.month
            day = data.day
            hour = data.hour
            minute = data.minute
            second = data.second
            time = datetime.datetime(
                int(year), 
                int(month), 
                int(day),
                int(hour), 
                int(minute), 
                int(second)
            )
            model.set_time(time)
            return render.time(time)
        elif submit2 is not None:
            model.reset_time()
            time = model.get_current_time()
            return render.time(time)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
