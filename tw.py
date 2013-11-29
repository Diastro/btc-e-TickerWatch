import sys, getopt
import json
import urllib2, urllib
import time

# color def
GREEN = '\033[92m'
PINK = '\033[95m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
NOCOLOR = '\033[0m'

# thanks to @t0pep0 (github) for this method
def __nonce():
   time.sleep(1)
   nonce = str(time.time()).split('.')[0]

def main(argv):
   key = ""
   sign = ""

   prevValue = -1
   currency = ""

   # temporary not sure why getopt isnt detecting missing required args
   # Needs refactoring
   if len(argv) < 1:
      print 'Missing required arguments'
      print 'for help : python tw.py -h'
      sys.exit(0)

   try:
      opts, args = getopt.getopt(argv,"hk:s:c:",["key=", "sign=", "currency="])
   except getopt.GetoptError:
      print 'Invalid arguments'
      sys.exit(0)
   for opt, arg in opts:
      if opt == '-h':
         print 'python tw.py -c ltc_btc -k _YourKey__ -s __YourSign__'
         print '  available feed : btc_usd, btc_rur, btc_eur, ltc_usd, lect_rur, ltc_eur, ltc_btc, nmc_btc, nmc_usd, nvm_btc, nvc_usd, usd_rur, eur_usd, trc_btc, ppc_btc, xpm_btc '
         sys.exit()
      elif opt in ("-c", "currency="):
         currency = arg.lower()
         # add error handling here
      elif opt in ("-k", "key="):
         key = arg
      elif opt in ("-s", "sign="):
         sign = arg
      else:
         print 'Invalid arguments'
         sys.exit(0)

   # quick fix for missing args
   if key == "" or sign == "":
	print 'Missing key/Sign'
	sys.exit(0)

   # request init
   url = "https://btc-e.com/api/2/" + currency + "/ticker"
   headers = {"Content-type" : "application/x-www-form-urlencoded",
                   "Key" : key,
                  "Sign" : sign }

   while True:
      # the equest
      try:
         nonce = __nonce()
         params = {"nonce" : str(nonce)}
         params = urllib.urlencode(params)
         req = urllib2.Request(url, params, headers)
         f = urllib2.urlopen(req)
         response = f.read()
         f.close()
      except:
         print 'Invalid feed. Exiting'
         sys.exit(2)

      # json formatting
      rep = json.loads(response)

      # updating values
      value = rep['ticker']['last']
      diff = float(prevValue) - float(value)
      diff = abs(diff)

      # console printing
      if value < prevValue:
         print currency.upper() + " " + YELLOW + ("-(%.5f)" % diff) + RED + " " + str(value) + NOCOLOR
      elif value == prevValue:
         continue
      else:
         print currency.upper() + " " + YELLOW + ("+(%.5f)" % diff) + GREEN + " " + str(value) + NOCOLOR

      prevValue = value

if __name__ == "__main__":
   main(sys.argv[1:])
