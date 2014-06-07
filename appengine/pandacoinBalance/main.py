"""Main.py is the top level script.

Loads the Bottle framework and mounts controllers.  Also adds a custom error
handler.
"""

from google.appengine.api import memcache, urlfetch

# import the Bottle framework
from server.lib.bottle import Bottle, request, response, template

import json, logging, StringIO, urllib2, sys
from decimal import *

# TODO: name and list your controllers here so their routes become accessible.
from server.controllers import RESOURCE_NAME_controller

BLOCKEXPLORER_URL = 'http://pandachain.net/chain/PandaCoin/q/addressbalance/'
BLOCKEXPLORER_URL_BACKUP = 'http://pnd.showed.us/chain/PandaCoin/q/addressbalance/'
TRADING_PAIR_URL = 'http://www.cryptocoincharts.info/v2/api/tradingPair/'
TIMEOUT_DEADLINE = 10 # seconds

# Run the Bottle wsgi application. We don't need to call run() since our
# application is embedded within an App Engine WSGI application server.
bottle = Bottle()

# Mount a new instance of bottle for each controller and URL prefix.
# TODO: Change 'RESOURCE_NAME' and add new controller references
bottle.mount("/RESOURCE_NAME", RESOURCE_NAME_controller.bottle)

@bottle.route('/')
def home():
  """Return project name at application root URL"""
  return "Pandacoin PND Balance"

@bottle.route('/api/balance/<address:re:[a-zA-Z0-9]+>')
def getBalance(address=''):
    response.content_type = 'application/json; charset=utf-8'

    url = BLOCKEXPLORER_URL + address
    data = None
    useBackupUrl = False
    try:
        data = urlfetch.fetch(url, deadline=TIMEOUT_DEADLINE)
        if (not data or not data.content):
            logging.warn('No content returned from ' + url)
            useBackupUrl = True
    except:
        e = sys.exc_info()[0]
        logging.warn('Error: ' + str(e) + ' when fetching ' + url)
        useBackupUrl = True

    if (useBackupUrl):
        backupUrl = BLOCKEXPLORER_URL_BACKUP + address
        logging.warn('Now trying ' + backupUrl)
        data = urlfetch.fetch(backupUrl, deadline=TIMEOUT_DEADLINE)

    dataDict = json.loads(data.content)
    balance = json.dumps(dataDict)
    mReturn = balance

    query = request.query.decode()
    if (len(query) > 0):
        mReturn = query['callback'] + '({balance:' + balance + '})'

    logging.info("getBalance(" + address + "): " + mReturn)
    return mReturn

@bottle.route('/api/trading-pnd')
@bottle.route('/api/trading-pnd/')
@bottle.route('/api/trading-pnd/<currency:re:[A-Z][A-Z][A-Z]>')
def tradingPND(currency='BTC'):
    response.content_type = 'application/json; charset=utf-8'

    mReturn = '{}'
    pndBtc = json.loads(memcache.get('trading_PND_BTC'))
    if (not pndBtc):
        logging.warn("No data found in memcache for trading_PND_BTC")
        return mReturn

    if (currency == 'BTC'):
        mReturn = pndBtc['price']
    elif (currency == 'LTC'):
        pndLtc = json.loads(memcache.get('trading_PND_LTC'))
        if (not pndLtc):
            logging.warn("No data found in memcache for trading_PND_LTC")
            return mReturn
        mReturn = pndLtc['price']
    else:
        btcCurrency = json.loads(memcache.get('trading_BTC_' + currency))
        if (not btcCurrency):
            logging.warn("No data found in memcache for trading_BTC_" + currency)
            return mReturn
        mReturn = Decimal(pndBtc['price']) * Decimal(btcCurrency['price'])

    query = request.query.decode()
    if (len(query) > 0):
        mReturn = query['callback'] + '({price:' + str(mReturn) + '})'

    logging.info("tradingPND(" + currency + "): " + str(mReturn))
    return str(mReturn)

def pullTradingPair(currency1='PND', currency2='BTC'):
    url = TRADING_PAIR_URL + currency1 + '_' + currency2
    data = urlfetch.fetch(url, deadline=TIMEOUT_DEADLINE)

    dataDict = json.loads(data.content)
    tradingData = json.dumps(dataDict)

    memcache.set('trading_' + currency1 + '_' + currency2, tradingData)
    logging.info('Stored in memcache for key trading_' + currency1 + '_' + currency2 + ': ' + tradingData)

@bottle.route('/tasks/pull-cryptocoincharts-data')
def pullCryptocoinchartsData():
    pullTradingPair('PND', 'BTC')
    pullTradingPair('PND', 'LTC')
    pullTradingPair('BTC', 'CNY')
    pullTradingPair('BTC', 'EUR')
    pullTradingPair('BTC', 'USD')
    return "Done"

@bottle.error(404)
def error_404(error):
  """Return a custom 404 error."""
  return 'Sorry, Nothing at this URL.'
