# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Resource, Api

import json

from excecaoGenerica import ExcecaoGenerica
from utils import Utils

app = Flask(__name__)
api = Api(app)

def calcula_custo(tempo_min, custo_hora):
	"""Calcula custo de uma tarefa.
	Argumentos:
		tempo_min -- Tempo em minutos da duração da tarefa
		custo_hora -- Custo por hora para execução da tarefa 
	"""
	Utils._assert(tempo_min < 0 or custo_hora < 0,
                      "Dados inválidos", ExcecaoGenerica)
	return (tempo_min * custo_hora)/60

def get_tarefa_mais_barata(tarefas):
	"""Retorna tarefa mais barata de ser executada primeiro.
	Argumentos:
		tarefas -- lista de tarefas a serem calculadas
	"""
	dict_custo_total = {}
	tarefa_barata = {}
	for tarefa in tarefas:
    		tarefa_id = tarefa['identificador']
		if not (dict_custo_total.has_key(tarefa_id)):
			dict_custo_total[tarefa_id] = {'tarefa': tarefa, 'custo': 0}
			for outra_tarefa in tarefas:
				if (outra_tarefa['identificador'] != tarefa_id):
					dict_custo_total[tarefa_id]['custo'] += calcula_custo(tarefa['tempo_de_execucao'], outra_tarefa['custo_por_hora'])

		if (tarefa_barata == {} or (tarefa_barata['custo'] > dict_custo_total[tarefa_id]['custo'])):
			tarefa_barata = dict_custo_total[tarefa_id]

	return tarefa_barata['tarefa']

def ordenaTarefasCustoHora(tarefas, lista_de_execucao):
	""" Preenche ordenadamente a lista de execução e a retorna. Para isso calcula o custo
	das tarefas, remove a tarefa mais barata de ser executada primeiro a cada iteração 
	da lista de tarefas e adicina na lista de execução.
	Argumentos:
		tarefas -- lista de tarefas a serem ordenadas
		lista_de_execucao -- lista a ser preenchida com identificadores ordenados com base no custo
	"""
	while (len(tarefas) > 0):
		tarefa = get_tarefa_mais_barata(tarefas)
		lista_de_execucao.append(tarefa['identificador'])
		tarefas.remove(tarefa)
	return lista_de_execucao

def ordenaTarefasMenorTempoEspera(tarefas):
	"""Ordena tarefas com base no menor tempo de execução, executar as tarefas mais curtas
	primeiro, diminui os somatórios de tempo de espera."""
	tarefas_ordenadas_por_tempo = sorted(tarefas, key = lambda i: i['tempo_de_execucao'])
	identificadores_tarefas_ordenadas = [tarefa['identificador'] for tarefa in tarefas_ordenadas_por_tempo]
	return identificadores_tarefas_ordenadas
	
class OrdenaTarefasHandler(Resource):
	"""Handler responsável por ordenar tarefas"""
	
	def post(self):
		tarefas_ordenadas = {}
		
		tarefas = request.get_json()['tarefas']
		tarefas_ordenadas['menor_tempo_espera'] = ordenaTarefasMenorTempoEspera(tarefas)
		tarefas_ordenadas['menor_custo_espera'] = ordenaTarefasCustoHora(tarefas, [])
		return tarefas_ordenadas

api.add_resource(OrdenaTarefasHandler, '/api/custo')