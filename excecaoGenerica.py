# -*- coding: utf-8 -*-
"""Exceção Genérica."""

class ExcecaoGenerica(Exception):
    """Exceção Genérica."""

    def __init__(self, msg=None):
        super(ExcecaoGenerica, self).__init__(
            msg or 'Entrada Inválida.')