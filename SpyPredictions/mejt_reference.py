from time import sleep, strftime, localtime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import datetime
import numpy as np
from bitmap import BitMap

new_symbolinput = ['SPY']
newDataList = []
dataDownload = []


def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg


def historical_data_handler(msg):
    global newDataList
    if ('finished' in str(msg.date)) == False:
        new_symbol = new_symbolinput[msg.reqId]
        data = []
        data.append(new_symbol)
        data.append(strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date))))
        data.append(msg.open)
        data.append(msg.high)
        data.append(msg.low)
        data.append(msg.close)
        data.append(msg.volume)
        newDataList.append(data)
        print data
    else:
        # find if gaps exits between the lowest and highest points
        arrayList = np.array(newDataList)

        highs = arrayList[:, 3].astype(np.float)
        lows = arrayList[:, 4].astype(np.float)
        highest = max(highs)
        lowest = min(lows)
        num_slots = (highest - lowest) / 0.001
        bm = BitMap(num_slots)
        print bm.tostring()

        gap_exits = None
        for i in range(0, len(arrayList)):
            for i in range((lows[i] - lowest) * 1000, (highs[i] - lowest) * 1000 + 1):
                bm.set(i)

        if bm.count() < len(bm.tostring()):
            gap_exits = True
            print("INVALIDATED: Gap exits before MEJT AM sequence, no prediction given!")

        # 1. Determine the MEJT reference bar
        am_o = newDataList[-3][2]
        am_h = newDataList[-3][3]
        am_l = newDataList[-3][4]
        am_c = newDataList[-3][5]

        am1_o = newDataList[-2][2]
        am1_h = newDataList[-2][3]
        am1_l = newDataList[-2][4]
        am1_c = newDataList[-2][5]

        am2_o = newDataList[-1][2]
        am2_h = newDataList[-1][3]
        am2_l = newDataList[-1][4]
        am2_c = newDataList[-1][5]

        # The default reference line is am0, but if am1 or am2 has a lower low and higher high
        # then it is the RL
        reference_line = 0
        if am1_l < am_l and am1_h > am_h:
            reference_line = 1

        if (am2_l < am_l and am2_h > am_h and am2_l < am1_l and am2_h > am1_h):
            reference_line = 2
        print("Reference line is AM+" + reference_line + "  Time: " + newDataList[reference_line - 3][1])

        # 2. Determine the Trend up/down?


        # 3. Calculate the Required and Optional Targets based on MEJT's high or low



        # 4. Rate the strength of this trend


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
    con.reqHistoricalData(symbol_id, qqq, '20160204 09:20:00 CST', '23100 S', '5 mins', 'TRADES', 1,
                          2)  # 900 S for 3 bars
    symbol_id = symbol_id + 1
    sleep(10)
