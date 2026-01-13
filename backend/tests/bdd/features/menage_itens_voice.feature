Feature: Gerenciamento de itens por comando de voz
    Como usuário comum
    Quero poder cadastrar e remover itens rapidamente via voz
    Para gerenciar meu estoque de forma ágil

    Background:
        Given o usuário possui uma sessão ativa no sistema

    Scenario: Cadastro bem-sucedido via voz
        Given que o áudio contém a descrição "Cadastrar 5 bananas"
        When o usuário envia o comando de voz para cadastro
        Then o sistema deve transcrever e interpretar com sucesso
        And o item "BANANA" deve constar no banco de dados com quantidade 5

    Scenario: Remoção bem-sucedida via voz
        Given que o item "LEITE" existe no estoque com quantidade 10
        And o áudio contém a descrição "Remover 2 litros de leite"
        When o usuário envia o comando de voz para remoção
        Then o sistema deve subtrair a quantidade corretamente
        And o estoque de "LEITE" deve ser atualizado para 8

    Scenario: Áudio não transcrito ou inválido
        When o usuário envia um áudio sem conteúdo perceptível
        Then o sistema deve retornar um erro de áudio inválido
        And informar "Não entendi direito o áudio, pode reenviar por favor?"