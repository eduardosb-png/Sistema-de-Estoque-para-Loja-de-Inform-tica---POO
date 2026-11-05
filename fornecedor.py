#fornecedor, produto, movimentacao, estoque.
class Fornecedor:
    """Quem fornece os produtos para a loja."""

    def __init__(self, nome, contato, prazo_entrega):
        self.nome = nome
        self.contato = contato
        self.prazo_entrega = prazo_entrega  # em dias

    def descricao(self):
        return (f"{self.nome} | Contato: {self.contato} | "
                f"Prazo de entrega: {self.prazo_entrega} dia(s)")