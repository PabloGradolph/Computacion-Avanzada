#------------------------------------
# Clase del 20 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Derivación numérica.
#------------------------------------

# Función que calcula la derivada NUMÉRICA por el método de las diferencias centrales.
def diferencias_centrales(h: float, siguiente: float, anterior: float) -> float:
    return (siguiente - anterior)/(2*h)

# Función que calcula la derivada NUMÉRICA por el método de diferencia hacia adelante.
def diferencia_alante(h: float, siguiente: float, actual: float) -> float:
    return (siguiente - actual)/h

# Función que calcula la derivada NUMÉRICA por el método de diferencia hacia detrás.
def diferencias_atras(h: float, actual: float, anterior: float) -> float:
    return (actual - anterior)/h