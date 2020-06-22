from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time, configparser, threading
import sys

def tipoVela(vela): 
	return 'g' if vela['open'] < vela['close'] else 'r' if vela['open'] > vela['close'] else 'd'

def lerConfiguracao():
	arquivo = configparser.RawConfigParser()
	arquivo.read('config.txt')
	
	return {s:dict(arquivo.items(s)) for s in arquivo.sections()}

def definirConfigAdicionais():	
	config['GERAL']['banca_inicial'] = API.get_balance()
	config['GERAL']['moedas'] = config['GERAL']['moedas'].split(',')
	config['GERAL']['payout'] = float(config['GERAL']['payout'])
	config['GERAL']['valor_entrada'] = float(config['GERAL']['valor_entrada'])
	config['GERAL']['stop_win'] = float(config['GERAL']['stop_win'])
	config['GERAL']['stop_loss'] = float(config['GERAL']['stop_loss'])
	
	if config['GERAL']['tipo_entrada'] == 'P':
		config['GERAL']['valor_entrada'] = config['GERAL']['banca_inicial'] * config['GERAL']['valor_entrada'] / 100
		config['GERAL']['stop_win'] = config['GERAL']['banca_inicial'] * config['GERAL']['stop_win'] / 100
		config['GERAL']['stop_loss'] = config['GERAL']['banca_inicial'] * config['GERAL']['stop_loss'] / 100
	
	if config['GERAL']['moedas'][0] == 'ALL':
		config['GERAL']['moedas'] = []
		moedas = API.get_all_open_time()
		
		if config['GERAL']['operacao'] == 'binaria' or config['GERAL']['operacao'] == 'ALL':
			for par in moedas['binary']:
				if moedas['binary'][par]['open'] == True:
					config['GERAL']['moedas'].append(par)
					
		if config['GERAL']['operacao'] == 'digital' or config['GERAL']['operacao'] == 'ALL':
			for par in moedas['digital']:
				if moedas['digital'][par]['open'] == True:
					config['GERAL']['moedas'].append(par)
		
		config['GERAL']['moedas'] = set(config['GERAL']['moedas'])
					
def verificarPayout(par, timeframe):
	eh_binaria = True
	payout = 0
	
	if config['GERAL']['operacao'] == 'binaria' or config['GERAL']['operacao'] == 'ALL':
		a = API.get_all_profit()
		if a[par]['turbo'] != {}:
			payout = int(100 * a[par]['turbo'])

	if config['GERAL']['operacao'] == 'digital' or config['GERAL']['operacao'] == 'ALL':
		try:
			API.subscribe_strike_list(par, timeframe)
			while True:
				d = API.get_digital_current_profit(par, timeframe)
				if d != False:
					d = int(d)
					break
			API.unsubscribe_strike_list(par, timeframe)
			if d > payout:
				eh_binaria = False
				payout = d
		except:
			pass

	return eh_binaria, payout

def realizarEntrada(par, valor, direcao, timeframe, gale, str_log):
	eh_binaria, payout = verificarPayout(par, timeframe)
	status = False
	lucro = 0
	
	if payout >= config['GERAL']['payout']:
		if eh_binaria:
			status, id = API.buy(valor, par, direcao, timeframe)
		else:
			status, id = API.buy_digital_spot(par, valor, direcao, timeframe)

		if status:
			str_log += '\n   Gale ' + str(gale) + '/' + config['GALE']['niveis'] + ' | ' + ('BINARIA' if eh_binaria else 'DIGITAL') + ' | ' + str(id)
			while True:
				if eh_binaria:
					status, lucro = API.check_win_v3(id)
				else:
					status, lucro =  API.check_win_digital_v2(id)
				
				if status:
					str_log += ' | Resultado ' + ('WIN /' if lucro > 0 else 'LOSS /') + str(round(valor, 2))

					if lucro < 0 and config['GALE']['utiliza'] == 'S' and config['GALE']['tipo'] == 'V' and (gale < int(config['GALE']['niveis'])):
						valor = valor * float(config['GALE']['fator'])
						status, lucro, gale, str_log = realizarEntrada(par, valor, direcao, timeframe, gale + 1, str_log)

					break
		else:
			str_log += '\n   ERRO AO REALIZAR OPERAÇÃO'
		
	else:
		str_log += '\n   ENTRADA CANCELADA, PAYOUT BAIXO:' + str(payout)
		
	return status, lucro, gale, str_log

def MHIParidade(par, timeframe):
	valor_entrada = config['GERAL']['valor_entrada']
	gale = 0
	soro = 0
	while True:
		minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
		
		if timeframe == 1:
			entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
		else:
			entrar = True if (minutos >= 29.58 and minutos <= 30) or minutos >= 59.58 else False

		#try:
		if entrar:
			velas = API.get_candles(par, timeframe * 60, 12, time.time())
			if config['GERAL']['tipo'] == 'H':
				entrar = False
				i = -6 if timeframe == 1 else -7
				cores = tipoVela(velas[i - 2]) + ' ' + tipoVela(velas[i - 1]) + ' ' + tipoVela(velas[i])
				
				dir = 'd'
				if cores.count('g') > cores.count('r') and cores.count('d') == 0: 
					dir = 'r'
				if cores.count('r') > cores.count('g') and cores.count('d') == 0: 
					dir = 'g'
				
				q = int(config['GALE']['niveis']) if config['GALE']['utiliza'] == 'S' and config['GALE']['tipo'] == 'V' else 0
				for x in range(q + 1):
					if dir == 'd' or dir == tipoVela(velas[i + x]):
						entrar = False

			if entrar:
				dir = False					
				cores = tipoVela(velas[-3]) + ' ' + tipoVela(velas[-2]) + ' ' + tipoVela(velas[-1])
  
				if cores.count('g') > cores.count('r') and cores.count('d') == 0: 
					dir = 'put'
				if cores.count('r') > cores.count('g') and cores.count('d') == 0: 
					dir = 'call'
				
				if dir:
					str_log = '\n\nIniciando Operação Moeda: ' + par + ' | Cores: ' + cores + ' | Direção: ' + dir
					
					status, lucro, g, str_log = realizarEntrada(par, valor_entrada, dir, timeframe, gale, str_log)
					'''if status:
						if lucro < 0:
							if config['GALE']['utiliza'] == 'S':							
								if config['GALE']['tipo'] == 'P':
									valor_entrada = valor_entrada * float(config['GALE']['fator'])
									gale += 1
								elif config['GALE']['tipo'] == 'S':
									valor_entrada = valor_entrada * float(config['GALE']['fator'])
									gale += 1
								if gale > 
									valor_entrada = config['GERAL']['valor_entrada']
									gale = 0
							if gale > int(config['GALE']['niveis']):
								gale = 0
					'''
					print(str_log)
					time.sleep(timeframe * 60 * (4.2 - g))
		#except:
		#	pass

		time.sleep(0.1)

config = lerConfiguracao()
API =  IQ_Option(config['GERAL']['login'], config['GERAL']['senha'])
API.connect()

if API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	sys.exit()

API.change_balance(config['GERAL']['conta'])
definirConfigAdicionais()

for par in config['GERAL']['moedas']:
	if config['GERAL']['timeframe'] == '1' or config['GERAL']['timeframe'] ==  'ALL':
		t = threading.Thread(target=MHIParidade,args=(par, 1))
		t.daemon = True
		t.start()
	if config['GERAL']['timeframe'] == '5' or config['GERAL']['timeframe'] ==  'ALL':
		t = threading.Thread(target=MHIParidade,args=(par, 5))
		t.daemon = True
		t.start()
		
while True:
	time.sleep(3600)