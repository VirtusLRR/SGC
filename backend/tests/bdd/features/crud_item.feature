Feature: Cadastro de itens
  Como usuário comum,
  Quero poder cadastrar novos itens,
  Para que eu possa gerenciar meu estoque.

  Background:
    Given o usuário está autenticado no sistema
    And acessa a página de cadastro de itens

  Scenario: Cadastro bem-sucedido de um novo item
    When o usuário informa o nome "Maçã"
    And o preço "2.00"
    And a quantidade "10"
    And a validade "27/10"
    And confirma o cadastro
    Then o sistema deve retornar status 201
    And o sistema deve exibir a mensagem "Item cadastrado com sucesso"
    And o produto "Maçã" deve aparecer na lista de produtos

  Scenario: Tentativa de cadastro com campos obrigatórios vazios
    When o usuário deixa o campo nome em branco
    And o preço "199.90"
    And a quantidade "5"
    And a validade "27/10"
    And confirma o cadastro
    Then o sistema deve retornar status 400 ou 422
    And o sistema deve exibir a mensagem "Campo obrigatório vazio"

  Scenario: Tentativa de cadastro com preço inválido
    When o usuário informa o nome "Ovos"
    And o preço "-50"
    And a quantidade "3"
    And a validade "27/10"
    And confirma o cadastro
    Then o sistema deve retornar status 400
    And o sistema deve exibir a mensagem "O preço deve ser maior que zero"

  Scenario: Remoção bem-sucedida de um item
    Given que existe um item "Maçã" cadastrado com 10 unidades
    When o usuário clica no botão remover ao lado do item "Maçã"
    And confirma a remoção
    Then o sistema deve retornar status 200 ou 204

  Scenario: Tentativa de remoção de itens já esgotados
    Given que existe um item "Maçã" cadastrado com 0 unidades
    When o usuário clica no botão remover ao lado do item "Maçã"
    Then o sistema deve retornar status 204 ou 200