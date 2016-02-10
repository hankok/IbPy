from time import sleep, strftime, localtime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import datetime

new_symbolinput = ['SPY']  # ,'GLD','SLV'
newDataList = []
dataDownload = []


def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg


def historical_data_handler(msg):
    global newDataList
    #print msg.reqId, msg.date, msg.open, msg.high, msg.low, msg.close, msg.volume
    if ('finished' in str(msg.date)) == False:
        new_symbol = new_symbolinput[msg.reqId]

        # print (datetime.datetime.fromtimestamp(
        #      int(msg.date)).strftime('%Y-%m-%d %H:%M:%S'))

        dataStr = '%s, %s, %s, %s, %s, %s, %s' % (
        new_symbol, strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date))), msg.open, msg.high, msg.low, msg.close,
        msg.volume)
        newDataList = newDataList + [dataStr]
    else:
        '''
        new_symbol = new_symbolinput[msg.reqId]
        filename = 'minutetrades' + new_symbol + '.csv'
        csvfile = open('csv_day_test/' + filename, 'wb')
        for item in newDataList:
            csvfile.write('%s \n' % item)
        csvfile.close()
        newDataList = []
        global dataDownload
        dataDownload.append(new_symbol)
        '''
        print newDataList

con = ibConnection()
con.register(error_handler, 'Error')
con.register(historical_data_handler, message.historicalData)
con.connect()

symbol_id = 0
for i in new_symbolinput:
    print i
    qqq = Contract()
    qqq.m_symbol = i
    qqq.m_secType = 'STK'
    qqq.m_exchange = 'SMART'
    qqq.m_currency = 'USD'
    # https://www.interactivebrokers.com/en/software/api/apiguide/java/reqhistoricaldata.htm
    con.reqHistoricalData(symbol_id, qqq, '20160204 09:20:00 CST', '900 S', '5 mins', 'TRADES', 1, 2)

    symbol_id = symbol_id + 1
    sleep(10)

#print dataDownload

'''
filename = 'downloaded_symbols.csv'
csvfile = open('csv_day_test/' + filename, 'wb')
for item in dataDownload:
    csvfile.write('%s \n' % item)
csvfile.close()
'''