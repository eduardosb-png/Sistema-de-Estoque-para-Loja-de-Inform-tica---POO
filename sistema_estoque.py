"""Sistema de estoque para uma loja de informática (Python orientado a objetos).
Os dados ficam apenas na memória enquanto o programa está aberto.
"""

from datetime import date, datetime, timedelta

def formatar_moeda(valor):
    """Formata um número no padrão brasileiro. Ex.: 1234.5 -> 1.234,50"""
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def dias_ate(data_texto):
    """Quantos dias faltam até a data (dd/mm/aaaa). Negativo se já passou."""
    data = datetime.strptime(data_texto, "%d/%m/%Y").date()
    return (data - date.today()).days

# Classes do sistema

class Fornecedor:
    """Quem fornece os produtos para a loja."""

    def __init__(self, nome, contato, prazo_entrega):
        self.nome = nome
        self.contato = contato
        self.prazo_entrega = prazo_entrega  # em dias

    def descricao(self):
        return (f"{self.nome} | Contato: {self.contato} | "
                f"Prazo de entrega: {self.prazo_entrega} dia(s)")


class Produto:
    """Classe base de tudo o que a loja vende."""

    def __init__(self, codigo, nome, categoria, preco, fornecedor):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.fornecedor = fornecedor  # associação com Fornecedor
        self.__preco = 0.0            # atributo privado
        self.__quantidade = 0         # atributo privado
        self.definir_preco(preco)     # já valida o preço inicial

    # --- métodos privados (só usados dentro da classe) ---
    def __validar_quantidade(self, qtd):
        if not isinstance(qtd, int) or qtd <= 0:
            raise ValueError("a quantidade deve ser um número inteiro maior que zero.")

    def __validar_preco(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("o preço deve ser maior que zero.")

    # --- preço ---
    def get_preco(self):
        return self.__preco

    def definir_preco(self, valor):
        self.__validar_preco(valor)
        self.__preco = float(valor)

    # --- quantidade ---
    def get_quantidade(self):
        return self.__quantidade

    def adicionar(self, qtd):
        self.__validar_quantidade(qtd)
        self.__quantidade += qtd

    def remover(self, qtd):
        self.__validar_quantidade(qtd)
        if qtd > self.__quantidade:
            raise ValueError(
                f"estoque insuficiente. Disponível: {self.__quantidade} unidade(s).")
        self.__quantidade -= qtd

    # --- métodos que as subclasses sobrescrevem (polimorfismo) ---
    def descricao(self):
        return (f"[{self.codigo}] {self.nome} | {self.categoria} | "
                f"R$ {formatar_moeda(self.__preco)}")

    def situacao(self):
        if self.__quantidade < 5:
            return "Estoque baixo"
        return "OK"


class Hardware(Produto):
    """Peças de computador (placas de vídeo, memórias, SSDs...)."""

    def __init__(self, codigo, nome, categoria, preco, fornecedor, garantia_meses):
        super().__init__(codigo, nome, categoria, preco, fornecedor)
        self.garantia_meses = garantia_meses

    def descricao(self):
        return super().descricao() + f" | Garantia: {self.garantia_meses} meses"

    def situacao(self):
        # peças são mais caras: o limite de estoque baixo é menor
        if self.get_quantidade() < 3:
            return "Estoque baixo"
        return "OK"


class Periferico(Produto):
    """Mouses, teclados, monitores e itens parecidos."""

    def __init__(self, codigo, nome, categoria, preco, fornecedor,
                 garantia_meses, conexao):
        super().__init__(codigo, nome, categoria, preco, fornecedor)
        self.garantia_meses = garantia_meses
        self.conexao = conexao

    def descricao(self):
        return (super().descricao() +
                f" | Garantia: {self.garantia_meses} meses | Conexão: {self.conexao}")

    def situacao(self):
        if self.get_quantidade() < 5:
            return "Estoque baixo"
        return "OK"


class Software(Produto):
    """Licenças de programas."""

    def __init__(self, codigo, nome, categoria, preco, fornecedor,
                 licenca, validade):
        super().__init__(codigo, nome, categoria, preco, fornecedor)
        try:
            dias_ate(validade)  # só para conferir se a data está no formato certo
        except ValueError:
            raise ValueError("validade inválida. Use o formato dd/mm/aaaa.")
        self.licenca = licenca
        self.validade = validade  # texto dd/mm/aaaa

    def licenca_vencendo(self):
        """True se a licença vence em até 30 dias (ou já venceu)."""
        return dias_ate(self.validade) <= 30

    def descricao(self):
        return (super().descricao() +
                f" | Licença: {self.licenca} | Validade: {self.validade}")

    def situacao(self):
        dias = dias_ate(self.validade)
        if dias < 0:
            return "Licença vencida"
        if self.licenca_vencendo():
            return f"Licença vence em {dias} dias"
        if self.get_quantidade() < 5:
            return "Estoque baixo"
        return "OK"


class Movimentacao:
    """Registro de uma entrada ou saída de mercadoria."""

    def __init__(self, tipo, produto, quantidade, data=None):
        self.tipo = tipo                  # "entrada" ou "saida"
        self.produto = produto            # associação com Produto
        self.quantidade = quantidade
        self.data = data or datetime.now().strftime("%d/%m/%Y")

    def resumo(self):
        tipo = "Entrada" if self.tipo == "entrada" else "Saída"
        return (f"{tipo} de {self.quantidade} un. de "
                f"{self.produto.nome} em {self.data}")


class Estoque:
    """Gerencia os produtos, os fornecedores e o histórico de movimentações."""

    def __init__(self):
        self.__produtos = []
        self.__fornecedores = []
        self.__movimentacoes = []

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


# ---------------------------------------------------------------------------
# Interface em terminal (menu)
# ---------------------------------------------------------------------------

def ler_texto(prompt):
    texto = input(prompt).strip()
    if not texto:
        raise ValueError("este campo não pode ficar vazio.")
    return texto


def ler_inteiro(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        raise ValueError("por favor digite um número inteiro.")


def ler_preco(prompt):
    try:
        return float(input(prompt).strip().replace(",", "."))
    except ValueError:
        raise ValueError("digite um valor numérico.")


def mostrar_menu():
    print("\n" + "=" * 38)
    print("   ESTOQUE - LOJA DE INFORMÁTICA")
    print("=" * 38)
    print("  1. Cadastrar produto")
    print("  2. Cadastrar fornecedor")
    print("  3. Listar produtos")
    print("  4. Buscar por categoria")
    print("  5. Registrar entrada")
    print("  6. Registrar saída")
    print("  7. Ver alertas")
    print("  8. Histórico de movimentações")
    print("  9. Relatório de valor em estoque")
    print("  0. Sair")
    print("-" * 38)


def mostrar_tabela(produtos):
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    print(f"{'Cód.':<7}{'Nome':<28}{'Categoria':<18}{'Preço (R$)':<13}{'Qtd':<6}Situação")
    for p in produtos:
        print(f"{p.codigo:<7}{p.nome:<28}{p.categoria:<18}"
              f"{formatar_moeda(p.get_preco()):<13}{p.get_quantidade():<6}{p.situacao()}")


def tela_cadastrar_produto(estoque):
    print("\n--- CADASTRAR PRODUTO ---")

    tipo = input("Tipo (1-Hardware  2-Periférico  3-Software): ").strip()

    if tipo not in ("1", "2", "3"):
        raise ValueError("tipo de produto inválido.")
    codigo = ler_texto("Código: ")

    if estoque.buscar_produto(codigo) is not None:
        raise ValueError(f"já existe um produto com o código {codigo}.")
    
    nome = ler_texto("Nome: ")
    categoria = ler_texto("Categoria: ")
    preco = ler_preco("Preço: ")
    fornecedor = estoque.buscar_fornecedor(ler_texto("Fornecedor (nome): "))

    if fornecedor is None:
        raise ValueError("fornecedor não encontrado. Cadastre-o primeiro (opção 2).")
 
    if tipo == "1":
        garantia = ler_inteiro("Garantia (meses): ")
        produto = Hardware(codigo, nome, categoria, preco, fornecedor, garantia)
    elif tipo == "2":
        garantia = ler_inteiro("Garantia (meses): ")
        conexao = ler_texto("Conexão (USB, Bluetooth, HDMI...): ")
        produto = Periferico(codigo, nome, categoria, preco, fornecedor, garantia, conexao)
    else:
        licenca = ler_texto("Tipo de licença (anual, vitalícia...): ")
        validade = ler_texto("Validade (dd/mm/aaaa): ")
        produto = Software(codigo, nome, categoria, preco, fornecedor, licenca, validade)

    estoque.cadastrar_produto(produto)
    print("\nProduto cadastrado com sucesso!")


def tela_cadastrar_fornecedor(estoque):
    print("\n--- CADASTRAR FORNECEDOR ---")
    nome = ler_texto("Nome: ")
    contato = ler_texto("Contato (telefone ou e-mail): ")
    prazo = ler_inteiro("Prazo de entrega (dias): ")
    estoque.cadastrar_fornecedor(Fornecedor(nome, contato, prazo))
    print("\nFornecedor cadastrado com sucesso!")


def tela_listar_produtos(estoque):
    print("\n--- PRODUTOS EM ESTOQUE ---")
    mostrar_tabela(estoque.listar_por_categoria())


def tela_buscar_categoria(estoque):
    print("\n--- BUSCAR POR CATEGORIA ---")
    categoria = ler_texto("Categoria: ")
    print()
    mostrar_tabela(estoque.listar_por_categoria(categoria))


def tela_entrada(estoque):
    print("\n--- REGISTRAR ENTRADA ---")

    codigo = ler_texto("Código do produto: ")
    produto = estoque.buscar_produto(codigo)

    if produto is None:
        raise ValueError(f"produto {codigo} não encontrado.")
    
    print(f"Produto: {produto.nome} (estoque atual: {produto.get_quantidade()})")

    qtd = ler_inteiro("Quantidade: ")
    estoque.registrar_entrada(codigo, qtd)

    print(f"\nEntrada registrada: {qtd} un. de {produto.nome}.")
    print(f"Estoque atual: {produto.get_quantidade()}")


def tela_saida(estoque):
    print("\n--- REGISTRAR SAÍDA ---")

    codigo = ler_texto("Código do produto: ")
    produto = estoque.buscar_produto(codigo)

    if produto is None:
        raise ValueError(f"produto {codigo} não encontrado.")
    
    print(f"Produto: {produto.nome} (estoque atual: {produto.get_quantidade()})")

    qtd = ler_inteiro("Quantidade: ")
    estoque.registrar_saida(codigo, qtd)

    print(f"\nSaída registrada: {qtd} un. de {produto.nome}.")
    print(f"Estoque atual: {produto.get_quantidade()}")


def tela_alertas(estoque):
    print("\n--- ALERTAS ---")
    mensagens = estoque.alertas()
    if not mensagens:
        print("Nenhum alerta no momento.")
        return
    for mensagem in mensagens:
        print(mensagem)
    print(f"\n{len(mensagens)} alerta(s) encontrado(s).")


def tela_historico(estoque):
    print("\n--- HISTÓRICO DE MOVIMENTAÇÕES ---")
    movimentacoes = estoque.historico()
    if not movimentacoes:
        print("Nenhuma movimentação registrada.")
        return
    for movimentacao in movimentacoes:
        print(movimentacao.resumo())


def tela_relatorio(estoque):
    print("\n--- VALOR EM ESTOQUE POR CATEGORIA ---")
    estoque.relatorio_valor_total()




def main():
    estoque = Estoque()

    acoes = {
        "1": tela_cadastrar_produto,
        "2": tela_cadastrar_fornecedor,
        "3": tela_listar_produtos,
        "4": tela_buscar_categoria,
        "5": tela_entrada,
        "6": tela_saida,
        "7": tela_alertas,
        "8": tela_historico,
        "9": tela_relatorio,
    }

    try:
        while True:
            mostrar_menu()
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "0":
                print("\nEncerrando o sistema. Até logo!")
                break
            acao = acoes.get(opcao)
            if acao is None:
                print("\nERRO: opção inválida.")
            else:
                try:
                    acao(estoque)
                except ValueError as erro:
                    print(f"\nERRO: {erro}")
            input("\nPressione Enter para voltar ao menu...")
    except (EOFError, KeyboardInterrupt):
        print("\n\nEncerrando o sistema.")


if __name__ == "__main__":
    main()
