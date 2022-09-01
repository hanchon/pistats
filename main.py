import time
import liquidcrystal_i2c
import requests

lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x3f, 1, numlines=4)
url = 'https://rest.bd.evmos.org:1317'
def get_missed_blocks(url:str, val:str = 'evmosvalcons1nsczfx3qr75f3anp4lklcanm585x7vwfuw3mt4'):
    try:
        endpoint = f'{url}/cosmos/slashing/v1beta1/signing_infos/{val}'
        res = requests.get(endpoint, timeout=2).json()
        return res['val_signing_info']['missed_blocks_counter']
    except Exception:
        return None

def get_height(url:str):
    try:
        endpoint = f'{url}/cosmos/base/tendermint/v1beta1/blocks/latest'
        res = requests.get(endpoint, timeout=2).json()
        return int(res['block']['header']['height'])
    except Exception:
        return None

def get_price(asset: str, vs_currency: str):
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?'
        resp = requests.get(f'{url}ids={asset}&vs_currencies={vs_currency}')
        return float(resp.json()[asset][vs_currency])
    except Exception:
        return None

running = True
def main():
    global running
    l1 = 'Evmos Price: 0.00'
    l2 = 'Height: 0000000'
    l3 = 'Hanchon.live'
    l4 = '0/90000 = 0%'
    while running:
        missed =  get_missed_blocks(url)
        if missed:
            l4 = f'{missed}/90000 = {"{:.2f}".format(float(missed)/90000*100)}%'

        height = get_height(url)
        if height:
            l2 = f'Height: {height}'

        price = get_price('evmos', 'usd')
        if price:
            l1 = f'Evmos Price: {price}'

        lcd.printline(0, l3)
        lcd.printline(1, l2)
        lcd.printline(2, l1)
        lcd.printline(3, l4)
        time.sleep(2)

    lcd.printline(0, '')
    lcd.printline(1, '')
    lcd.printline(2, '')
    lcd.printline(3, '')
    return 0

if __name__ == '__main__':
    SystemExit(main())
