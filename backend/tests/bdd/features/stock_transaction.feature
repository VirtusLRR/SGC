Feature: Estatísticas e Painel de Controle de Estoque
    Como um usuário comum
    Quero visualizar estatísticas de consumo e gastos
    Para gerenciar meu estoque e economizar futuramente

    Background:
        Given o usuário possui uma sessão ativa no sistema
        And existe o item "ARROZ" no banco de dados com ID 1

    Scenario: Visualização de resumo financeiro por período
        Given que existem transações de "entrada" totalizando R$ 500.00
        And existem transações de "saida" totalizando R$ 200.00
        When o usuário solicita o resumo de transações dos últimos 10 dias
        Then o saldo total (balance) deve ser de R$ 300.00
        And o número de entradas deve ser maior que zero

    Scenario: Atualização do histórico de gastos após nova compra
        Given o histórico de gastos mensais do mês atual é R$ 1000.00
        When o usuário cadastra uma nova transação de "entrada" do item 1 no valor de R$ 250.00
        And solicita a visualização de gastos mensais
        Then o gasto total do mês atual deve ser atualizado para R$ 1250.00

    Scenario: Ranking de itens mais consumidos
        Given que o item 1 teve 5 transações de "saida"
        When o usuário solicita o ranking de itens mais transacionados
        Then o item "ARROZ" deve aparecer no topo do ranking