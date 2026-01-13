Feature: Visualização de receitas
  Como usuário comum gostaria de ter acesso a um painel de receitas,
  para que eu possa visualizar as minhas receitas cadastradas.

  Background:
    Given o usuário está autenticado no sistema
    And acessa a página de receitas

  Scenario: Pesquisa por receita possível com o estoque atual
    Given que existe uma receita "Carbonara" cadastrada e viável
    When o usuário pesquisa o nome "Carbonara"
    Then o sistema deve exibir a receita "Carbonara" na lista

  Scenario: O usuário pesquisa por uma receita com ingredientes faltantes no estoque atual.
    Given que existe uma receita "Parmegiana de carne" que necessita de "carne"
    And o estoque de "carne" está zerado
    When o usuário pesquisa o nome "Parmegiana de carne"
    Then o sistema deve exibir a mensagem "A receita não é viável, pois está faltando carne no estoque"