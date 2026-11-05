from datetime import date, datetime

def formatar_moeda(valor):
    """Formata um número no padrão brasileiro. Ex.: 1234.5 -> 1.234,50"""
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def dias_ate(data_texto):
    """Quantos dias faltam até a data (dd/mm/aaaa). Negativo se já passou."""
    data = datetime.strptime(data_texto, "%d/%m/%Y").date()
    return (data - date.today()).days