'''
	BOT MHI v1
	- Analise em 1 minuto
	- Entradas para 1 minuto
	- Calcular as cores das velas de cada quadrado, ultimas 3 velas, minutos: 2, 3 e 4 / 7, 8 e 9
	- Entrar contra a maioria

'''

from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
import sys

print('''
----------------------------------   
   Simples MHI + MARTINGALE BOT
						AVENGERS
----------------------------------
''')

def martingale(tipo, valor, payout, lucro_esperado, perca):
	if tipo == 'simples':
		return valor * 2.2
	else:
		while True:
			if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
				return round(valor, 2)
				break
			valor += 0.01

def entrada(par, valor, direcao, timeframe, qtd_gale):
    status,id = API.buy_digital_spot(par, valor, dir, 1)
        
    if status:
        while True:
            status,lucro = API.check_win_digital_v2(id)
            
            if status:
                print('Resultado operação: ', end='')
                print('WIN /' if lucro > 0 else 'LOSS /' , round(valor, 2))

                if lucro < 0 and qtd_gale > 0:
                    valor_gale = martingale('simples', valor, 0, 0, 0)
                    print('Entrando no martingale com valor ', round(valor, 2))
                    entrada(par, valor_gale, direcao, timeframe, 0)
										
                break
    else:
        print('\nERRO AO REALIZAR OPERAÇÃO\n\n')

email = input('Email:')
senha = input('Senha:')
API =  IQ_Option(str(email), str(senha))

API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL

if API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	sys.exit()

par = input(' Indique uma paridade para operar: ')
valor_entrada = float(input(' Indique um valor para entrar: '))

while True:
	minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
	entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
	#print('Hora de entrar?',entrar,'/ Minutos:',minutos)

	if entrar:
		print('\n\nIniciando operação!')
		dir = False
		print('Verificando cores..', end='')
		velas = API.get_candles(par, 60, 3, time.time())
       
		velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
		velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
		velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
     
     # cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
		cores = velas[0]+velas[1]+velas[2]		
		
		print(cores)

		if cores == 'grg': dir = 'put'
		if cores == 'rgr': dir = 'call'

			# AJUSTE VERSAO 1.0.1 - ADICIONANDO NOVAS POSSIBILIDADE
		if cores == 'rrg': dir = 'call'
		if cores == 'rgg': dir = 'put'
		if cores == 'ggr': dir = 'put'
		if cores == 'grr': dir = 'call'
		





    # if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = 'put'
    # if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = 'call'
		if dir:
			print('Direção:',dir)
      
			entrada(par,valor_entrada,dir,1,2)
		else:
			print('Entrada fora do filtro')
            
                
	time.sleep(0.5)