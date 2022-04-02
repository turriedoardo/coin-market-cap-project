# importo le librerie
import requests
from pprint import pprint
import time

class Bot: # definisco la calsse bot
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' # definisco gli attributi della classe Bot

        self.params = {
                       'start' : '1', 
                       'limit' : '100', 
                       'convert':'USD'
                       }

        self.headers = {
                        'Accepts' : 'application/json',
                        'X-CMC_PRO_API_KEY': '3144b56f-524a-4539-858a-1424dbbfbc44'
                        }
        
    def fetchCurrenciesData(self): # creo il metodo 
        r = requests.get(url = self.url, params = self.params, headers= self.headers).json() # invio richiesta a API di cmc per ottenere un file json
        return r['data'] # seleziono la lista data dal file json


while True:

    impact_bot = Bot() # creo un'istanza impact_bot
    currencies = impact_bot.fetchCurrenciesData() # applico il metodo sull'istanza
    highest_volume = None # valore del maggior volume di scambi nelle ultime 24 ore
    highest_volume_currency = None # nome della valuta col maggior volume di scambi
    top_10_cryptos = {} # migliori 10 valute per incremento % nelle ultime 24 ore e rispettivo incremento
    worst_10_cryptos = {} # peggiori 10 valute per incremento % e relativa perdita
    unit_cost_top_ranked = {} # costo di una unità di ciascuna delle prime 20 valute
    money_quantity_76 = 0 # denaro per acquistare tutte le valute con volume superiore a 76 mln
    money_quantity_top_ranked = 0 # denaro per acquistare tutte le prime 20 valute
    total_price_yd = 0 # somma cumulata del costo di una unità delle prime 20 valute IERI
    total_earnings = 0 # somma cumulata dei guadagni comprando una unità delle prime 20 valute IERI

    for currency in currencies: # itero sulle valute in data
        name = currency['name'] # attribuisco le informazioni utili a delle variabili locali
        volume = currency['quote']['USD']['volume_24h']
        percent_change = currency['quote']['USD']['percent_change_24h']
        price = currency['quote']['USD']['price'] 

        if highest_volume == None: # se il valore più alto non c'è, allora lo diventa il primo valore
            highest_volume = volume
            highest_volume_currency = name

        elif volume > highest_volume: # se il volume è più alto di highest volume, gli attribuisco il nuovo valore
            highest_volume = volume
            highest_volume_currency = name # nome della valuta col più alto volume di scambi


        top_10_cryptos[name] = percent_change # creo una lista con le variazioni %

        if len(top_10_cryptos) > 10: # se la lista ha più di 10 elementi, elimino il minore
            min_pair = min(top_10_cryptos.items(), key= lambda x : x[1])
            del top_10_cryptos[min_pair[0]]
        
        worst_10_cryptos[name] = percent_change # creo una lista con le variazioni %

        if len(worst_10_cryptos) > 10: # se la lista ha più di 10 elementi, elimino il maggiore
            max_pair = max(worst_10_cryptos.items(), key= lambda x : x[1])
            del worst_10_cryptos[max_pair[0]]

        if currency['cmc_rank'] <= 20: # seleziono le prime 20 criptovalute
            unit_cost_top_ranked[name] = price # aggiungo al dizionario il prezzo di ciascuna
            price_yd = price/(1 + (percent_change/100)) # calcolo il prezzo di una unità della valuta IERI
            earnings = price_yd * percent_change/100 # calcolo il guadagno se avessi comprato una unità della valuta IERI
            total_price_yd += price_yd # aggiungo il prezzo di ieri alla somma cumulata dei prezzi
            total_earnings += earnings # aggiungo il guadagno di ieri alla somma cumulata dei guadagni
            money_quantity_top_ranked += price # aggiungo il prezzo alla quantità di denaro per comprare tutte le prime 20 valute


        if volume > 76000000: # seleziono le valute con volume superiore a 76 mln nelle ultime 24 ore
            money_quantity_76 += price # sommo la quantità necessaria per comprare una unità di ogni valuta

    sorted_worst_cryptos = sorted(worst_10_cryptos.items(), key= lambda x : x[1]) # ordino le liste
    sorted_top_cryptos = sorted(top_10_cryptos.items(), key = lambda x : x[1], reverse = True)
    earnings_percentage = total_earnings/ total_price_yd # calcolo il guadagno percentuale

    # overview
    print(f'{highest_volume_currency} è la criptovaluta con il maggior volume nelle ultime 24 ore: {highest_volume}')
    
    print('\nLe migliori dieci criptovalute nelle ultime 24 ore e i loro incrementi percentuali sono:')
    pprint(sorted_top_cryptos)
    
    print('\nLe peggiori dieci criptovalute nelle ultime 24 ore e le loro variazioni percentuali sono:')
    pprint(sorted_worst_cryptos)

    print(f'\nLa quantità di denaro per acquistare una unità di tutte le criptovalute con volume superiore a 76 mln nelle ultime 24 ore è {money_quantity_76}')

    print('\nLa quantità di denaro per acquistare una unità di ciascuna delle prime 20 criptovalute è:')
    pprint(unit_cost_top_ranked)

    print(f'\nLa quantità di denaro per acquistare una unità di tutte le prime 20 criptovalute è: {money_quantity_top_ranked}')
    
    print(f'\nLa percentuale di guadagno che avresti ottenuto se ieri avessi comprato una unità di ciascuna delle prime 20 criptovalute è: {earnings_percentage} %')

    # routine
    seconds = 60 * 60 * 24
    time.sleep(seconds) # stampo il resoconto una volta al giorno


        
