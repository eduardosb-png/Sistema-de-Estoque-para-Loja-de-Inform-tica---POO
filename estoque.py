from movimentacao import Movimentacao
from utilidades import formatar_moeda

class Estoque:
    """Gerenciamento dos produtos, dos fornecedores e do histórico de movimentações."""

    def __init__(self):
        self.__produtos = [] # lista de produtos cadastrados.
        self.__fornecedores = [] # lista de fornecedores cadastrados.
        self.__movimentacoes = [] # lista de movimentações registradas do programa.

    def cadastrar_produto(self, produto):
        if self.buscar_produto(produto.codigo) is not None:
            raise ValueError(f"já existe um produto com o código {produto.codigo}.")
        self.__produtos.append(produto)

    def cadastrar_fornecedor(self, fornecedor):
        if self.buscar_fornecedor(fornecedor.nome) is not None:
            raise ValueError(f"já existe um fornecedor chamado {fornecedor.nome}.")
        self.__fornecedores.append(fornecedor)

    def buscar_produto(self, codigo):
        for produto in self.__produtos:
            if produto.codigo.lower() == codigo.lower():
                return produto
        return None

    def buscar_fornecedor(self, nome):
        for fornecedor in self.__fornecedores:
            if fornecedor.nome.lower() == nome.lower():
                return fornecedor
        return None

    def listar_por_categoria(self, categoria=None):
        """Sem categoria, devolve todos os produtos."""
        if categoria is None:
            return list(self.__produtos)
        return [p for p in self.__produtos
                if p.categoria.lower() == categoria.lower()]

    def __produto_ou_erro(self, codigo):
        produto = self.buscar_produto(codigo)
        if produto is None:
            raise ValueError(f"produto {codigo} não encontrado.")
        return produto

    def registrar_entrada(self, codigo, qtd):
        produto = self.__produto_ou_erro(codigo)
        produto.adicionar(qtd)
        movimentacao = Movimentacao("entrada", produto, qtd)
        self.__movimentacoes.append(movimentacao)
        return movimentacao

    def registrar_saida(self, codigo, qtd):
        produto = self.__produto_ou_erro(codigo)
        produto.remover(qtd)
        movimentacao = Movimentacao("saida", produto, qtd)
        self.__movimentacoes.append(movimentacao)
        return movimentacao

    def historico(self):
        return list(self.__movimentacoes)

    def alertas(self):
        """Mensagens de estoque baixo e de licença perto de vencer."""
        mensagens = []
        for produto in self.__produtos:
            situacao = produto.situacao()
            if situacao != "OK":
                mensagens.append(f"{produto.codigo} - {produto.nome}: {situacao}")
        return mensagens

    def relatorio_valor_total(self):
        """Mostra o valor em estoque por categoria e devolve o total geral."""
        por_categoria = {}
        for produto in self.__produtos:
            valor = produto.get_preco() * produto.get_quantidade()
            por_categoria[produto.categoria] = por_categoria.get(produto.categoria, 0) + valor
        total = sum(por_categoria.values())

        print(f"{'Categoria':<20}{'Valor (R$)':>14}")
        for categoria, valor in por_categoria.items():
            print(f"{categoria:<20}{formatar_moeda(valor):>14}")
        print("-" * 34)
        print(f"{'TOTAL':<20}{formatar_moeda(total):>14}")
        return total
