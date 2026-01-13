Feature: Cadastro de itens por Nota Fiscal
    Como um usuário do sistema
    Quero enviar uma foto da minha nota fiscal contendo pão e mortadela
    Para que os itens sejam cadastrados automaticamente no estoque

    Scenario: Processamento de Nota Fiscal Válida
        Given que a IA detectou "PAO FRANCES" e "MORTADELA CERATTI" na imagem
        When o usuário envia a foto para o endpoint de mensagem
        Then a resposta deve ser sucesso (200)
        And os itens devem ter sido criados no banco de dados com as quantidades corretas