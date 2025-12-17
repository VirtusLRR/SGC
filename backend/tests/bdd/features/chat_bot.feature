Feature: Sugestão de Receitas Alternativas
    Como usuário comum, quero que o sistema me sugira
    receitas alternativas, caso alguma receita fique indisponível
    para que eu possa realizar outra receita com base nos itens
    que tenho no estoque.

    Scenario:
        Given que o usuário comum está autenticado no sistema
        And o banco de dados está populado com receitas e ingredientes
        And existem receitas com ingredientes disponíveis no estoque
        And existe uma receita "risoto de camarão" com ingredientes indisponíveis

    Scenario: Exibição de sugestão por substituibilidade
        When o usuário comum visualizar uma receita que está indisponível
        Then o sistema deve exibir, ao lado desta, uma sugestão de receita contendo produtos disponíveis no estoque
        And deve apresentar um breve texto explicando a substituibilidade

