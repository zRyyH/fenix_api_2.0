from datetime import datetime, timedelta


def extrair_data(data_str):
    """
    Função para extrair a data de uma string no formato ISO 8601.
    """
    try:
        try:
            data = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S")
        except:
            data = datetime.strptime(data_str, "%Y-%m-%d")

        return {
            "ano_mes": data.strftime("%Y-%m"),
            "data": data,
            "ano": data.year,
            "mes": data.month,
            "dia": data.day,
        }

    except ValueError:
        raise ValueError("Formato de data inválido. Use o formato ISO 8601.")


def gerar_intervalo_mes(data_str):
    data = datetime.strptime(data_str, "%Y-%m-%d")

    # Primeiro dia do mês atual
    inicio = data.replace(day=1)

    # Primeiro dia do mês seguinte
    if data.month == 12:
        fim = data.replace(year=data.year + 1, month=1, day=1)
    else:
        fim = data.replace(month=data.month + 1, day=1)

    return f"{inicio.date()},{fim.date()}"
