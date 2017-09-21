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

import hashlib, hmac, time # for bitcoinaverage API
import config # this file contains secret API key(s), and so it is in .gitignore

BLOCKEXPLORER_URL = 'http://chainz.cryptoid.info/pnd/api.dws?q=getbalance&a='
BTCAVERAGE_URL = 'https://api.bitcoinaverage.com/ticker/' # used for BTC / (EUR, GBP, CNY, AUD)
TRADING_PAIR_URL_CRYPTOPIA = 'https://www.cryptopia.co.nz/api/GetMarket/'

TIMEOUT_DEADLINE = 12 # seconds

def bitcoinaverage_ticker(currency):
  timestamp = int(time.time())
  payload = '{}.{}'.format(timestamp, config.bitcoinaverage_public_key)
  hex_hash = hmac.new(config.bitcoinaverage_secret_key.encode(), msg=payload.encode(), digestmod=hashlib.sha256).hexdigest()
  signature = '{}.{}'.format(payload, hex_hash)

  url = 'https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC' + currency
  headers = {'X-Signature': signature}
  return urlfetch.fetch(url, headers=headers, deadline=TIMEOUT_DEADLINE)

def cryptopia_ticker(currency1, currency2):
  url = TRADING_PAIR_URL_CRYPTOPIA + currency1 + '_' + currency2
  return urlfetch.fetch(url, deadline=TIMEOUT_DEADLINE)

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

  url = BLOCKEXPLORER_URL + address + '&key=' + config.cryptoid_api_key

  data = urlfetch.fetch(url, deadline=TIMEOUT_DEADLINE)
  if (not data or not data.content or data.status_code != 200):
    logging.error('No content returned! URL: ' + url)

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
  pndLtc = json.loads(memcache.get('trading_PND_LTC'))
  if (not pndLtc):
    logging.warn("No data found in memcache for trading_PND_LTC")
    return mReturn

  ltcBtc = json.loads(memcache.get('trading_LTC_BTC'))
  if (not ltcBtc and currency != 'LTC'):
    logging.warn("No data found in memcache for trading_LTC_BTC")
    return mReturn

  # PND -> LTC -> BTC
  pnd_btc_price = '%.12f' % (Decimal(pndLtc['price']) * Decimal(ltcBtc['price']))

  if (currency == 'BTC'):
    # PND -> LTC -> BTC
    mReturn = pnd_btc_price
  elif (currency == 'LTC'):
    mReturn = pndLtc['price']
  else:
    btcCurrency = json.loads(memcache.get('trading_BTC_' + currency))
    if (not btcCurrency):
      logging.warn("No data found in memcache for trading_BTC_" + currency)
      return mReturn
    mReturn = '%.12f' % (Decimal(pnd_btc_price) * Decimal(btcCurrency['price']))

  query = request.query.decode()
  if (len(query) > 0):
    mReturn = query['callback'] + '({price:' + str(mReturn) + '})'

  logging.info("tradingPND(" + currency + "): " + str(mReturn))
  return str(mReturn)

def pullTradingPair(currency1='PND', currency2='LTC'):
  if currency2 in ['CNY', 'EUR', 'GBP', 'USD', 'AUD']:
    data = bitcoinaverage_ticker(currency2)
    if (not data or not data.content or data.status_code != 200):
      logging.error('No content returned for trading pair ' + currency1 + '_' + currency2)
    else:
      dataDict = json.loads(data.content)
      dataDict['price'] = dataDict['last']
  else:
    data = cryptopia_ticker(currency1, currency2)
    if (not data or not data.content or data.status_code != 200):
      logging.error('No content returned for trading pair ' + currency1 + '_' + currency2)
    else:
      dataDict = json.loads(data.content)
      dataDict['price'] = '%.12f' % Decimal(dataDict['Data']['LastPrice'])

  tradingData = json.dumps(dataDict).strip('"')
  memcache.set('trading_' + currency1 + '_' + currency2, tradingData)
  logging.info('Stored in memcache for key trading_' + currency1 + '_' + currency2 + ': ' + tradingData)

@bottle.route('/tasks/pull-cryptocoincharts-data')
def pullCryptocoinchartsData():
    pullTradingPair('PND', 'LTC')
    pullTradingPair('LTC', 'BTC')
    pullTradingPair('BTC', 'USD')
    pullTradingPair('BTC', 'CNY')
    pullTradingPair('BTC', 'EUR')
    pullTradingPair('BTC', 'GBP')
    return "Done"

@bottle.error(404)
def error_404(error):
  """Return a custom 404 error."""
  return 'Sorry, Nothing at this URL.'
