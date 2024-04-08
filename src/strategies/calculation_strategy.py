from datetime import timedelta

# Interface para a estratégia de cálculo
class CalculationStrategy:
    def calcular_tempo(self, incoming_time, outcoming_time):
        pass

# Implementação da estratégia para calcular o tempo decorrido entre duas horas no formato HH:MM
class TempoDecorridoStrategy(CalculationStrategy):
    def calcular_tempo(self, incoming_time, outcoming_time):
        inicio_hora, inicio_minuto = map(int, incoming_time.split(':'))
        fim_hora, fim_minuto = map(int, outcoming_time.split(':'))

        inicio_tempo = timedelta(hours=inicio_hora, minutes=inicio_minuto)
        fim_tempo = timedelta(hours=fim_hora, minutes=fim_minuto)

        tempo_decorrido = fim_tempo - inicio_tempo

        return tempo_decorrido.total_seconds() / 60  # Convertendo para minutos