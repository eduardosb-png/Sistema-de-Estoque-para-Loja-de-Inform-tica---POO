from datetime import date, timedelta
from utilidades import formatar_moeda
from fornecedor import Fornecedor
from produto import Hardware, Periferico, Software
from estoque import Estoque

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

def criar_dados_exemplo(estoque):
    """Cria um fornecedor e alguns produtos para o sistema já abrir com dados."""
    fornecedor = Fornecedor("TechDistrib", "contato@techdistrib.com", 5)
    estoque.cadastrar_fornecedor(fornecedor)
 
    ssd = Hardware("H001", "SSD 480GB", "Armazenamento", 229.90, fornecedor, 12)
    placa = Hardware("H002", "Placa de vídeo RTX 4060", "Placas de vídeo", 2399.00, fornecedor, 12)
    mouse = Periferico("P001", "Mouse gamer", "Periféricos", 129.90, fornecedor, 12, "USB")
    validade = (date.today() + timedelta(days=12)).strftime("%d/%m/%Y")
    windows = Software("S001", "Windows 11 Pro", "Licenças", 899.00, fornecedor, "Anual", validade)
 
    for produto, qtd in [(ssd, 12), (placa, 2), (mouse, 8), (windows, 4)]:
        estoque.cadastrar_produto(produto)
        estoque.registrar_entrada(produto.codigo, qtd)
        

def main():
    estoque = Estoque()
    criar_dados_exemplo(estoque)

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
                print("\nEncerrando o sistema.")
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