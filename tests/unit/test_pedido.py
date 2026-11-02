import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================



def test_bug1_subtotal_considera_quantidade(pedido_pequeno):
    # 6,00 x 1 + 4,50 x 2 = 15,00 (o código original soma só os preços: 10,50)
    assert pedido_pequeno.subtotal() == 15.0



def test_bug2_frete_gratis_com_exatamente_50():
    # limite: subtotal de R$ 50,00 inclusive tem frete grátis
    pedido = Pedido("Carla", [Item("Combo", 25.0, 2)])
    assert pedido.tem_frete_gratis() is True



def test_bug3_item_mais_barato_retorna_o_menor_preco(pedido_grande):
    # menor preço unitário: refrigerante (7,00)
    assert pedido_grande.item_mais_barato().nome == "Refrigerante"



def test_bug4_desconto_subtrai_do_subtotal():
    # R$ 100,00 com 10% de desconto = 90,00 (o original soma: 110,00)
    pedido = Pedido("Carla", [Item("Combo", 50.0, 2)])
    assert pedido.total_com_desconto(10) == 90.0



# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função

def _pedido_com_frete():
    return Pedido("Ana", [Item("Combo", 60.0, 1)])


def _pedido_sem_frete():
    return Pedido("Bruno", [Item("Café", 6.0, 1)])


def test_req1_todos_com_frete_gratis():
    pedidos = [_pedido_com_frete(), _pedido_com_frete(), _pedido_com_frete()]
    assert contar_frete_gratis(pedidos) == 3


def test_req1_nenhum_com_frete_gratis():
    pedidos = [_pedido_sem_frete(), _pedido_sem_frete()]
    assert contar_frete_gratis(pedidos) == 0


def test_req1_lista_mista():
    pedidos = [_pedido_com_frete(), _pedido_sem_frete(), _pedido_com_frete()]
    assert contar_frete_gratis(pedidos) == 2


def test_req1_lista_vazia_retorna_zero():
    assert contar_frete_gratis([]) == 0



# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método

def test_req2_mais_de_25_por_cento_indisponivel_cancela_mesmo_com_frete_gratis(pedido_grande):
    # 5 unidades, 2 indisponíveis = 40% (> 25%); subtotal 87,00 teria frete grátis
    assert pedido_grande.tem_frete_gratis() is True
    assert pedido_grande.situacao(2) == "Cancelado por falta de estoque"


def test_req2_tudo_disponivel_com_frete_gratis(pedido_grande):
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"


def test_req2_tudo_disponivel_sem_frete_gratis(pedido_pequeno):
    assert pedido_pequeno.situacao(0) == "Confirmado"


def test_req2_exatamente_25_por_cento_segue_para_regra_do_frete():
    # 4 unidades, 1 indisponível = exatamente 25% (não cancela)
    com_frete = Pedido("Ana", [Item("Combo", 15.0, 4)])
    sem_frete = Pedido("Bruno", [Item("Café", 6.0, 4)])
    assert com_frete.situacao(1) == "Confirmado com frete grátis"
    assert sem_frete.situacao(1) == "Confirmado"


def test_req2_pouco_acima_de_25_por_cento_cancela():
    # 7 unidades, 2 indisponíveis ≈ 28,6% (> 25%)
    pedido = Pedido("Ana", [Item("Combo", 10.0, 7)])
    assert pedido.situacao(2) == "Cancelado por falta de estoque"




# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método

def test_req3_abaixo_de_50_aciona_sms_com_cliente_e_valor_faltante(pedido_pequeno):
    sms = MagicMock()
    # subtotal 15,00 -> faltam 35,00
    pedido_pequeno.sugerir_frete_gratis(sms)
    sms.enviar.assert_called_once_with("Bruno", 35.0)


def test_req3_acima_de_50_nao_aciona_sms(pedido_grande):
    sms = MagicMock()
    pedido_grande.sugerir_frete_gratis(sms)
    sms.enviar.assert_not_called()


def test_req3_exatamente_50_nao_aciona_sms():
    sms = MagicMock()
    Pedido("Carla", [Item("Combo", 25.0, 2)]).sugerir_frete_gratis(sms)
    sms.enviar.assert_not_called()

