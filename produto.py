from utilidades import formatar_moeda, dias_ate

class Produto:
    """Classe base do que a loja vende."""

    def __init__(self, codigo, nome, categoria, preco, fornecedor):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.fornecedor = fornecedor  # associação com Fornecedor
        self.__preco = 0.0            # atributo privado
        self.__quantidade = 0         # atributo privado
        self.definir_preco(preco)     # já valida o preço inicial

    # --- métodos privados só usados dentro da classe ---
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

    # --- métodos que as subclasses irão fazer a sobrescrita -polimorfismo- ---
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
        """Em Hardware você define a garantia em meses (ex.: 12, 24, 36) os outros valores ele ira usar o super()."""
        self.garantia_meses = garantia_meses

    def descricao(self):
        return super().descricao() + f" | Garantia: {self.garantia_meses} meses"

    def situacao(self):
        # peças normalmente são mais caras então: o limite de estoque baixo é menor
        if self.get_quantidade() < 3:
            return "Estoque baixo"
        return "OK"


class Periferico(Produto):
    """ Exemplos: Mouses, teclados, monitores e itens parecidos."""

    def __init__(self, codigo, nome, categoria, preco, fornecedor,
                 garantia_meses, conexao):
        super().__init__(codigo, nome, categoria, preco, fornecedor)
        """Em Periferico você define a garantia em meses (ex.: 12, 24, 36) e o tipo de conexão (ex.: USB, Bluetooth) os outros valores ele ira usar o super()."""
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
        """Em Software você define a licença (ex.: Windows 10, Adobe Photoshop) e a validade (ex.: 01/01/2024) os outros valores ele ira usar o super()."""
        try:
            dias_ate(validade)  # apenas para conferir se a data está no formato certo
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