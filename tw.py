import sys, getopt
import json
import urllib2
import time

# color def
GREEN = '\033[92m'
PINK = '\033[95m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
NOCOLOR = '\033[0m'

def main(argv):
   oldValue = -1
   currency = ""
   interval = 1

   # temporary not sure why getopt isnt detecting missing required args
   if len(argv) is 0:
      print 'Missing required arguments'
      print 'for help : python tw.py -h'
      sys.exit(2)

   try:
      opts, args = getopt.getopt(argv,"hc:i",["currency=", "interval="])
   except getopt.GetoptError:
      print 'Invalid arguments'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'python tw.py -c ltc_btc'
         print '  available feed : btc_usd, btc_rur, btc_eur, ltc_usd, lect_rur, ltc_eur, ltc_btc, nmc_btc, nmc_usd, nvm_btc, nvc_usd, usd_rur, eur_usd, trc_btc, ppc_btc, xpm_btc '
         sys.exit()
      elif opt in ("-c", "currency="):
         currency = arg.lower()
         # add error handling here
      elif opt in ("-i", "interval="):
         interval = arg
         # add error handling here

   # to add:
   # - different feed
   url = "https://btc-e.com/api/2/" + currency + "/ticker"

   while True:
      # make the request
      try:
         req = urllib2.Request(url)
         f = urllib2.urlopen(req)
         response = f.read()
         f.close()
      except:
         print 'Invalid feed. Exiting'
         sys.exit(2)

      # json formatting
      rep = json.loads(response)

      value = rep['ticker']['last']
      diff = float(oldValue) - float(value)
      diff = abs(diff)

      if value < oldValue:
         print currency.upper() + " " + YELLOW + ("-(%.5f)" % diff) + RED + " " + str(value) + NOCOLOR
      elif value == oldValue:
         continue
      else:
         print currency.upper() + " " + YELLOW + ("+(%.5f)" % diff) + GREEN + " " + str(value) + NOCOLOR

      oldValue = value
      time.sleep(interval)

if __name__ == "__main__":
   main(sys.argv[1:])
