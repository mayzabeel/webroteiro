# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_restful import Resource, Api
import json
from operator import itemgetter

app = Flask(__name__)
api = Api(app)

def calcula_custo(tempo_min, custo_hora):
	"""Calcula custo de uma tarefa.
	Argumentos:
	tempo_min -- Tempo em minutos da duração da tarefa
	custo_hora -- Custo por hora para execução da tarefa 
	"""
	return (tempo_min * custo_hora)/60

def calculaCustos(tarefas):
	"""Calcula o custo total de cada tarefa supondo que a 
	tarefa seja a primeira a ser executada, ignorando o seu próprio custo.
	Retorna dicionário ordenado no qual as chaves são os identificadores
	e os valores são os respectivos custos totais de cada tarefa.
	Argumentos:
	tarefas -- lista de tarefas a serem calculadas
	"""
	dict_custo_total = {}
	for tarefa in tarefas:
    		tarefa_id = tarefa['identificador']
		if not (dict_custo_total.has_key(tarefa_id)):
			dict_custo_total[tarefa_id] = 0
			for outra_tarefa in tarefas:
				if (outra_tarefa['identificador'] != tarefa_id):
					dict_custo_total[tarefa_id] += calcula_custo(tarefa['tempo_de_execucao'], outra_tarefa['custo_por_hora'])
	return sorted(dict_custo_total, key = dict_custo_total.get)

def ordenaTarefasCustoHora(tarefas, lista_de_execucao):
	""" Preenche ordenadamente a lista de execução e a retorna. Para isso calcula o custo
	das tarefas, remove a tarefa mais barata de ser executada primeiro a cada iteração 
	da lista de tarefas e adicina na lista de execução.
	Argumentos:
	tarefas -- lista de tarefas a serem ordenadas
	lista_de_execucao -- lista a ser preenchida com identificadores ordenados com base no custo
	size -- tamanho da lista de tarefas
	"""
	while (len(tarefas) > 0):
		custos_totais_ordenados = calculaCustos(tarefas)
		lista_de_execucao.append(custos_totais_ordenados[0])
		filter_iter = filter(lambda tarefa: tarefa['identificador'] == custos_totais_ordenados[0], tarefas)
		executada = filter_iter[0]
		indice = tarefas.index(executada)
		del tarefas[indice]
	return lista_de_execucao

def ordenaTarefasMenorTempoEspera(tarefas):
	"""Ordena tarefas com base no menor tempo de execução, executar as tarefas mais curtas
	primeiro, diminui os somatórios de tempo de espera."""
	tarefas_ordenadas = []
	for tarefa in sorted(tarefas, key = lambda i: i['tempo_de_execucao']):
		tarefas_ordenadas.append(tarefa['identificador'])
	return tarefas_ordenadas
	
class OrdenaTarefasHandler(Resource):
	"""Handler responsável por ordenar tarefas"""
	
	def post(self):
		tarefas_ordenadas = {}
		tarefas = request.get_json()['tarefas']
		tarefas_ordenadas['menor_tempo_espera'] = ordenaTarefasMenorTempoEspera(tarefas)
		tarefas_ordenadas['menor_custo_espera'] = ordenaTarefasCustoHora(tarefas, [])
		return tarefas_ordenadas

api.add_resource(OrdenaTarefasHandler, '/api/custo_por_hora')