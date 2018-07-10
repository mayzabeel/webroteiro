# -*- coding: utf-8 -*-
"""Utils."""

class Utils():
    
    @staticmethod
    def _assert(condition, msg, exception):
        """Checa condição, se for true, lança exceção genérica."""
        if condition:
            raise exception(msg)