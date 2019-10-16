"""
Freiar o carro em dada aproximacao

"""
import numpy as np
import skfuzzy as fuzz

# Generate universe variables
x_aproximacao = np.arange(31)
x_distancia = np.arange(201)
x_freio = np.arange(101)

# Generate fuzzy membership functions
aproximacaoLenta = fuzz.trapmf(x_aproximacao, [0, 0, 3, 5])
aproximacaoRapida = fuzz.trapmf(x_aproximacao, [4, 6, 8, 10])
aproximacaoMtoRapida = fuzz.trapmf(x_aproximacao, [9, 12, 30, 30])
freioZerado = fuzz.trapmf(x_freio, [0, 0, 0, 0])
freioFraco = fuzz.trapmf(x_freio, [0, 0, 10, 25])
freioMedio = fuzz.trapmf(x_freio, [20, 30, 60, 85])
freioForte = fuzz.trapmf(x_freio, [80, 90, 100, 100])
distanciaPerto = fuzz.trapmf(x_distancia, [0, 0, 8, 15])
distanciaLonge = fuzz.trapmf(x_distancia, [10, 50, 200, 200])

# Test values
aproximacaoValue = 30
distanciaValue = 20

# We need the activation of our fuzzy membership functions at these values.
aproximacaoLenta_level = fuzz.interp_membership(x_aproximacao, aproximacaoLenta, aproximacaoValue)
aproximacaoRapida_level = fuzz.interp_membership(x_aproximacao, aproximacaoRapida, aproximacaoValue)
aproximacaoMtoRapida_level = fuzz.interp_membership(x_aproximacao, aproximacaoMtoRapida, aproximacaoValue)
distanciaPerto_level = fuzz.interp_membership(x_distancia, distanciaPerto, distanciaValue)
distanciaLonge_level = fuzz.interp_membership(x_distancia, distanciaLonge, distanciaValue)

# Now we take our rules and apply them. Rule 1 concerns bad food OR service.
# The OR operator means we take the maximum of these two.
active_rule1 = np.fmin(aproximacaoRapida_level, distanciaPerto_level)
ativacaoFreio_medio = np.fmin(active_rule1, freioMedio)
active_rule2 = np.fmin(aproximacaoMtoRapida_level, distanciaPerto_level)
ativacaoFreio_forte = np.fmin(active_rule2, freioForte)
active_rule3 = np.fmin(aproximacaoRapida_level, distanciaLonge_level)
active_rule4 = np.fmin(aproximacaoMtoRapida_level, distanciaLonge_level)
active_rule5 = np.fmin(aproximacaoLenta_level, distanciaPerto_level)
ativacaoFreio_fraca = np.fmax(np.fmin(active_rule4, freioFraco), np.fmin(active_rule5, freioFraco))
active_rule6 = np.fmin(aproximacaoLenta_level, distanciaLonge_level)
ativacaoFreio_zerada = np.fmax(np.fmin(active_rule3, freioZerado), np.fmin(active_rule6, freioZerado))

# Aggregate all three output membership functions together
aggregated = np.fmax(ativacaoFreio_zerada,
                     np.fmax(ativacaoFreio_fraca, np.fmax(ativacaoFreio_medio, ativacaoFreio_forte)))

# Calculate defuzzified result
resultado = fuzz.defuzz(x_freio, aggregated, 'centroid')

if __name__ == '__main__':
    print(resultado)
