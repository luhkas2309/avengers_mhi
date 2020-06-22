# Digital


## Cerca del modo strike
![](image/near.png)
### Ejemplo

```python
from iqoptionapi.stable_api import IQ_Option
import time
import random
I_want_money=IQ_Option("email","password")
I_want_money.connect()#conectar a iqoption
ACTIVES="EURUSD"
duration=1#minuto 1 or 5
amount=1
I_want_money.subscribe_strike_list(ACTIVES,duration)
#get strike_list
data=I_want_money.get_realtime_strike_list(ACTIVES, duration)
print("get strike data")
print(data)
"""data
{'1.127100': 
    {  'call': 
            {   'profit': None, 
                'id': 'doEURUSD201811120649PT1MC11271'
            },   
        'put': 
            {   'profit': 566.6666666666666, 
                'id': 'doEURUSD201811120649PT1MP11271'
            }	
    }............
} 
"""
#Obtener la lista de precios
price_list=list(data.keys())
#Elegir una estratégia aleatoria
choose_price=price_list[random.randint(0,len(price_list)-1)]
#Obtener instrument_id
instrument_id=data[choose_price]["call"]["id"]
#Obtener profit
profit=data[choose_price]["call"]["profit"]
print("Elegir que quiere commprar")
print("precio:",choose_price,"side:call","instrument_id:",instrument_id,"profit:",profit)
#Escojer instrument_id para abrir operación
buy_check,id=I_want_money.buy_digital(amount,instrument_id)
polling_time=5
if buy_check:
    print("Esperar para comprobar win")
    #comprobar win
    while True:
        check_close,win_money=I_want_money.check_win_digital_v2(id,polling_time)
        if check_close:
            if float(win_money)>0:
                win_money=("%.2f" % (win_money))
                print("Tu has ganado",win_money,"dinero")
            else:
                print("Sin beneficioss")
            break
    I_want_money.unsubscribe_strike_list(ACTIVES,duration)
else:
    print("Fallo al comprar, porfavor prueba otra vez")
```

### Obtener toda la lissta de datos de todos los strike

Ejemplo 
```python
from iqoptionapi.stable_api import IQ_Option
import time
I_want_money=IQ_Option("email","password")
I_want_money.connect()#conecta a iqoption
ACTIVES="EURUSD"
duration=1#minuto 1 or 5
I_want_money.subscribe_strike_list(ACTIVES,duration)
while True:
    data=I_want_money.get_realtime_strike_list(ACTIVES, duration)
    for price in data:
        print("precio",price,data[price])
    time.sleep(5)
I_want_money.unsubscribe_strike_list(ACTIVES,duration)
```
#### subscribe_strike_list()

```python
I_want_money.subscribe_strike_list(ACTIVES,duration)
```

#### get_realtime_strike_list

Tu necesitas llamar a subscribe_strike_list() antes de get_realtime_strike_list()
```python
I_want_money.get_realtime_strike_list(ACTIVES,duration)
```

#### unsubscribe_strike_list()
```python
I_want_money.unsubscribe_strike_list(ACTIVES,duration)
```
### buy_digital()

```python
buy_check,id=I_want_money.buy_digital(amount,instrument_id)
#obtener el instrument_id de I_want_money.get_realtime_strike_list
```

## Modo actual del precio

![](image/spot.png)



### buy_digital_spot
Comprar el dígito en el precio actual

Devuelve check y id

```python
from iqoptionapi.stable_api import IQ_Option
 
I_want_money=IQ_Option("email","password")
I_want_money.connect()#conectar a iqoption
ACTIVES="EURUSD"
duration=1#minuto 1 or 5
amount=1
action="call"#put
print(I_want_money.buy_digital_spot(ACTIVES,amount,action,duration))
```

### get_digital_spot_profit_after_sale()

Obtener Profit después de la Venta(P/L)

![](image/profit_after_sale.png)

Ejemplo 

```python
from iqoptionapi.stable_api import IQ_Option 
I_want_money=IQ_Option("email","passord")
ACTIVES="EURUSD"
duration=1#minute 1 or 5
amount=100
action="put"#put
 
I_want_money.subscribe_strike_list(ACTIVES,duration)
_,id=I_want_money.buy_digital_spot(ACTIVES,amount,action,duration) 
 
while True:
    PL=I_want_money.get_digital_spot_profit_after_sale(id)
    if PL!=None:
        print(PL)
```

### get_digital_current_profit()

```python
from iqoptionapi.stable_api import IQ_Option
import time
import logging
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#conectar a iqoption
ACTIVES="EURUSD"
duration=1#minuto 1 or 5
I_want_money.subscribe_strike_list(ACTIVES,duration)
while True:
    data=I_want_money.get_digital_current_profit(ACTIVES, duration)
    print(data)# La primera impresión puede ser falsa, sólo espera un segundo puedes obtener el beneficio
    time.sleep(1)
I_want_money.unsubscribe_strike_list(ACTIVES,duration)
```

## check win for digital

### check_win_digital()

Esta api esta implementada por get_digital_position()

Esta función esta encuestando, necesitas escojet el tiempo de encuesta

```python
I_want_money.check_win_digital(id,polling_time)#obtener el id de I_want_money.buy_digital
```
### check_win_digital_v2()

Esta api es asíncrona, obtiene el id de los datos. Solo puede obtener el id de los datos antess de que puedass comprar la opción. 
Si reinicias el programa, no se puede obtener otra vez la id de los datos de manera asíncrona otra vez. 
De esta forma no se puede trabajar con check_win_digital_v2, asi tu necesitas usar check_win_digital.

```python
 I_want_money.check_win_digital_v2(id)#obtener el id deI_want_money.buy_digital
#return:check_close,win_money
#return sample
#if you loose:Ture,o
#if you win:True,1232.3
#if trade not clode yet:False,None
```

Ejemplo de código 

```python
from iqoptionapi.stable_api import IQ_Option
import logging
import random
import time
import datetime
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
ACTIVES="EURUSD"
duration=1#minuto 1 or 5
amount=1
action="call"#put
_,id=(I_want_money.buy_digital_spot(ACTIVES,amount,action,duration))
print(id)
if id !="error":
    while True:
        check,win=I_want_money.check_win_digital_v2(id)
        if check==True:
            break
    if win<0:
        print("Has perdido "+str(win)+"$")
    else:
        print("Has ganado "+str(win)+"$")
else:
    print("Porfavor prueba otra vez")
```

## close_digital_option()

```python
I_want_money.close_digital_option(id)
```

## Obtener datos de opciones digitaless

Ejemplo 1
```python
from iqoptionapi.stable_api import IQ_Option
import logging
import time
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#conectar a iqoption
ACTIVES="EURUSD-OTC"
duration=1#minuto 1 or 5
amount=1
action="call"#put
from datetime import datetime
 
_,id=I_want_money.buy_digital_spot(ACTIVES,amount,action,duration) 

while True:
    check,_=I_want_money.check_win_digital(id)
    if check:
        break
print(I_want_money.get_digital_position(id))
print(I_want_money.check_win_digital(id))
```

Ejemplo 2

```python
print(I_want_money.get_positions("digital-option"))
print(I_want_money.get_digital_position(2323433))#Comprobar por id
print(I_want_money.get_position_history("digital-option"))
```