# Cuenta

## get_balance() 
Obtén el saldo de tu cuenta

```python
I_want_money.get_balance()
```

## get_balance_v2() 
Obtén el saldo de tu cuenta con MÁS PRECISIÓN

```python
I_want_money.get_balance_v2()
```

## get_currency()
Comprobar que divisa utiliza tu cuenta (USD, EUR...)

```python
I_want_money.get_currency()
```

## reset_practice_balance()
Recargar el saldo de tu cuenta de práctica a $10000

```python
from iqoptionapi.stable_api import IQ_Option
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
print(I_want_money.reset_practice_balance())
```

## Cambiar tu cuenta entre los smodos Real/Práctica

MODE="PRACTICE"/"REAL"
```python
I_want_money.change_balance(MODE)
                        #MODE: "PRACTICE"/"REAL"
```

## obtener la Estratégia de Otra Gente

 
### Ejemplo
```python
from iqoptionapi.stable_api import IQ_Option
import logging
import time
 
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
while_run_time=10
 
#Para opciones digitales
name="live-deal-digital-option" #"live-deal-binary-option-placed"/"live-deal-digital-option"
active="EURUSD"
_type="PT1M"#"PT1M"/"PT5M"/"PT15M"
buffersize=10#
print("_____________subscribe_live_deal_______________")
I_want_money.subscribe_live_deal(name,active,_type,buffersize)

 
start_t=time.time()
while True:
    data=(I_want_money.get_live_deal(name,active,_type))
    print("__For_digital_option__ data size:"+str(len(data)))
    print(data)
    print("\n\n")
    time.sleep(1)
    if time.time()-start_t>while_run_time:
        break
print("_____________unscribe_live_deal_______________")
I_want_money.unscribe_live_deal(name,active,_type)


#Para opciones binariass
name="live-deal-binary-option-placed"
active="EURUSD"
_type="turbo"#"turbo"/"binary"
buffersize=10#
print("_____________subscribe_live_deal_______________")
I_want_money.subscribe_live_deal(name,active,_type,buffersize)

start_t=time.time()
while True:
    data=(I_want_money.get_live_deal(name,active,_type))
    print("__For_binary_option__ data size:"+str(len(data)))
    print(data)
    print("\n\n")
    time.sleep(1)
    if time.time()-start_t>while_run_time:
        break
print("_____________unscribe_live_deal_______________")
I_want_money.unscribe_live_deal(name,active,_type)
```

### subscribe_live_deal
Suscribirse a un acuerdo en vivo

```python
I_want_money.subscribe_live_deal(name,active,_type,buffersize)
```

### unscribe_live_deal
Cancelar suscripción al acuerdo en vivo

```python
I_want_money.unscribe_live_deal(name,active,_type)
```

### get_live_deal
Obtener el acuerdo en vivo

```python
I_want_money.get_live_deal(name,active,_type)
```
### pop_live_deal

```python
I_want_money.pop_live_deal(name,active,_type)
```
## get Other people detail
Obtener los detalles de otra gente

### Ejemplo 
```python
from iqoptionapi.stable_api import IQ_Option
import logging
import time
 
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
while_run_time=10
 
#Para opciones binarias
name="live-deal-binary-option-placed"
active="EURUSD"
_type="turbo"#"turbo"/"binary"
buffersize=10#
print("_____________subscribe_live_deal_______________")
print("\n\n")
I_want_money.subscribe_live_deal(name,active,_type,buffersize)

last_trade_data=I_want_money.get_live_deal(name,active,_type)[0]
 
user_id=last_trade_data["user_id"]
counutry_id=last_trade_data["country_id"]
print("_______get_user_profile_client__________")
print(I_want_money.get_user_profile_client(user_id))
pro_data=I_want_money.get_user_profile_client(user_id)
print("\n\n")

print("___________request_leaderboard_userinfo_deals_client______")
print(I_want_money.request_leaderboard_userinfo_deals_client(user_id,counutry_id))
user_data=I_want_money.request_leaderboard_userinfo_deals_client(user_id,counutry_id)
worldwide=user_data["result"]["entries_by_country"]["0"]["position"]
profit=user_data["result"]["entries_by_country"]["0"]["score"]
print("\n")
print("user_name:"+pro_data["user_name"])
print("Esta semana en todo el mundo: "+str(worldwide))
print("Esta semana beneficios en bruto: "+str(profit))
print("\n\n")

print("___________get_users_availability____________")
print(I_want_money.get_users_availability(user_id))
print("\n\n")
print("_____________unscribe_live_deal_______________")
I_want_money.unscribe_live_deal(name,active,_type)

```

### get_user_profile_client()
Obtener el nombre de usuario y imagen

```python
I_want_money.get_user_profile_client(user_id)
```

### request_leaderboard_userinfo_deals_client()
Obtener los detalles del cliente

```python
I_want_money.request_leaderboard_userinfo_deals_client(user_id,counutry_id)
```

### get_users_availability()

```python
I_want_money.get_users_availability(user_id)
```