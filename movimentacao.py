from datetime import datetime

class Movimentacao:
    """Registro de uma entrada ou saída de mercadoria no estoque sobre os produtos."""

    def __init__(self, tipo, produto, quantidade, data=None):
        self.tipo = tipo                  # "entrada" ou "saida"
        self.produto = produto            # associação com Produto
        self.quantidade = quantidade
        self.data = data or datetime.now().strftime("%d/%m/%Y")

    def resumo(self):
        tipo = "Entrada" if self.tipo == "entrada" else "Saída"
        return (f"{tipo} de {self.quantidade} un. de "
                f"{self.produto.nome} em {self.data}")