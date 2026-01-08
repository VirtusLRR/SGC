# Testes do Sistema Multi-Agente - Gestão de Estoque e Receitas

Este documento contém casos de teste para validar o funcionamento completo do sistema multi-agente com a nova arquitetura.

---

## Índice de Testes

1. [Testes do Agente TRIVIAL](#1-testes-do-agente-trivial)
2. [Testes do SQL_ORCHESTRATOR](#2-testes-do-sql_orchestrator)
3. [Testes do RECIPE_READER](#3-testes-do-recipe_reader)
4. [Testes do ITEM_READER](#4-testes-do-item_reader)
5. [Testes do TRANSACTION_READER](#5-testes-do-transaction_reader)
6. [Testes do STRUCTURER_RECIPE + RECIPE_WRITER](#6-testes-do-structurer_recipe--recipe_writer)
7. [Testes do STRUCTURER_ITEM + ITEM_WRITER + TRANSACTION_WRITER](#7-testes-do-structurer_item--item_writer--transaction_writer)
8. [Testes do ITEM_WRITER (UPDATE/DELETE)](#8-testes-do-item_writer-updatedelete)
9. [Testes do REVISOR](#9-testes-do-revisor)
10. [Testes do Agente WEB](#10-testes-do-agente-web)
11. [Testes de Fluxo Completo](#11-testes-de-fluxo-completo)
12. [Testes de Casos Extremos](#12-testes-de-casos-extremos)

---

## 1. Testes do Agente TRIVIAL

### Teste 1.1 - Saudação Simples - OK
**Entrada:** `Oi, tudo bem?`

**Fluxo Esperado:** Orchestrator → TRIVIAL

**Resposta Esperada:**
```
Olá! Tudo ótimo, obrigado! 😊 Sou seu assistente de estoque e receitas. 
Como posso te ajudar hoje?
```

---

### Teste 1.2 - Perguntas sobre Funcionalidades - OK
**Entrada:** `O que você pode fazer?`

**Fluxo Esperado:** Orchestrator → TRIVIAL

**Resposta Esperada:**
```
Posso te ajudar com várias coisas! 

- Consultar quantidades e preços de produtos no estoque
- Buscar receitas culinárias (tanto no banco quanto na internet)
- Verificar se você tem os ingredientes para uma receita
- Adicionar, atualizar e remover itens do estoque
- Salvar novas receitas no sistema
- Ver histórico de transações (compras, vendas, uso)

Experimente perguntar: 'Quantas bananas tenho?' ou 'Posso fazer torta banoffee?'
```

---

### Teste 1.3 - Bom dia - OK
**Entrada:** `Bom dia!`

**Fluxo Esperado:** Orchestrator → TRIVIAL

**Resposta Esperada:**
```
Bom dia! Como posso ajudar você hoje? 😊
```

---

## 2. Testes do SQL_ORCHESTRATOR

### Teste 2.1 - Roteamento para SQL_RECIPE - OK
**Entrada:** `Quais receitas tenho cadastradas?` 

**Fluxo Esperado:** 
- Orchestrator → SQL_ORCHESTRATOR
- SQL_ORCHESTRATOR → SQL_RECIPE
- SQL_RECIPE → RECIPE_READER

**Justificativa:** Pergunta sobre receitas cadastradas

---

### Teste 2.2 - Roteamento para SQL_ITEM - OK
**Entrada:** `Quantas bananas tenho?` 

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR
- SQL_ORCHESTRATOR → SQL_ITEM
- SQL_ITEM → ITEM_READER

**Justificativa:** Pergunta sobre quantidade de item no estoque

---

### Teste 2.3 - Roteamento para SQL_TRANSACTION - OK
**Entrada:** `Mostre o histórico de compras` 

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR
- SQL_ORCHESTRATOR → SQL_TRANSACTION
- SQL_TRANSACTION → TRANSACTION_READER

**Justificativa:** Pergunta sobre histórico de transações

---

## 3. Testes do RECIPE_READER

### Teste 3.1 - Listar Todas as Receitas - OK
**Entrada:** `Quais receitas você tem cadastradas?` 

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER

**Resposta Esperada:**
```
📚 Receitas cadastradas (4):

1. Torta Banoffee - torta clássica inglesa com banana e doce de leite
2. Pavê de Banana com Doce de Leite - sobremesa cremosa em camadas
3. Brigadeiro de Banana com Doce de Leite - brigadeiro cremoso
4. Risoto de Camarão - risoto cremoso com camarões frescos

Total: 4 receitas
```

---

### Teste 3.2 - Buscar Receita Específica - OK
**Entrada:** `Como fazer torta banoffee?` 

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER

**Resposta Esperada:**
```
📖 **Torta Banoffee**

Descrição: torta clássica inglesa com banana e doce de leite

Modo de Preparo:
1. Em uma tigela, misture o biscoito triturado com a manteiga derretida até formar uma farofa úmida.
2. Forre o fundo e as laterais de uma forma de fundo removível (cerca de 22 cm de diâmetro), pressionando bem. Leve à geladeira por 30 minutos.
3. Espalhe o doce de leite de maneira uniforme sobre a base de biscoito já firme.
4. Distribua as rodelas de banana sobre o doce de leite, cobrindo toda a superfície.
5. Na batedeira, bata o creme de leite fresco com o açúcar até atingir o ponto de chantilly (picos firmes).
6. Cubra a torta com o chantilly. Decore com raspas de chocolate ou polvilhe cacau em pó.
7. Mantenha na geladeira até a hora de servir.
```

---

### Teste 3.3 - Ver Ingredientes de Uma Receita - OK
**Entrada:** `Quais ingredientes tem na torta banoffee?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER

**Resposta Esperada:**
```
Ingredientes da Torta Banoffee:

- 4 unidades de banana nanica
- 400g de doce de leite
- 200g de biscoito maisena
- 100g de manteiga
- 500ml de creme de leite
- 80g de açúcar
- 30g de chocolate em pó
```

---

### Teste 3.4 - Verificar Disponibilidade (Tool check_recipe_availability) - OK
**Entrada:** `Consigo fazer torta banoffee?`

**Fluxo Esperado:** 
- Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER
- RECIPE_READER usa tool `check_recipe_availability`

**Resposta Esperada:**
```
SIM! Você pode fazer 'torta banoffee'!

Ingredientes disponíveis:
4unidade de banana nanica, 400grama de doce de leite, 200grama de biscoito maisena, 100grama de manteiga, 500mililitro de creme de leite, 80grama de açúcar, 30grama de chocolate em pó
```

---

### Teste 3.5 - Verificar Disponibilidade com Falta de Ingredientes - OK
**Entrada:** `Posso fazer risoto de camarão?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER

**Resposta Esperada:**
```
Infelizmente NÃO é possível fazer 'risoto de camarão' no momento.

Faltam os seguintes ingredientes:
  - arroz arbóreo: necessário 300grama, disponível 0grama
  - camarão: necessário 400grama, disponível 0grama
  - vinho branco: necessário 150mililitro, disponível 0mililitro
  - caldo de legumes: necessário 1000mililitro, disponível 0mililitro
  - queijo parmesão: necessário 50grama, disponível 0grama

Mas posso sugerir estas receitas alternativas que você PODE fazer com os ingredientes disponíveis:

1. Torta Banoffee - torta clássica inglesa com banana e doce de leite
2. Pavê de Banana com Doce de Leite - sobremesa cremosa em camadas
3. Brigadeiro de Banana com Doce de Leite - brigadeiro cremoso

Gostaria de saber mais sobre alguma dessas receitas?
```

---

### Teste 3.6 - Buscar Receitas com Ingrediente Específico - OK
**Entrada:** `Quais receitas usam banana?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER

**Resposta Esperada:**
```
Receitas que contêm banana:

1. Torta Banoffee - torta clássica inglesa com banana e doce de leite
2. Pavê de Banana com Doce de Leite - sobremesa cremosa em camadas
3. Brigadeiro de Banana com Doce de Leite - brigadeiro cremoso
```

---

### Teste 3.7 - Receita Não Encontrada - OK
**Entrada:** `Como fazer bolo de chocolate?`

**Fluxo Esperado:** 
- Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER
- RECIPE_READER não encontra
- REVISOR → decide ir para WEB

**Resposta SQL:** `Receita 'bolo de chocolate' não encontrada no banco de dados.`

---

## 4. Testes do ITEM_READER

### Teste 4.1 - Consulta Simples de Quantidade - OK
**Entrada:** `Quantas bananas tenho?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
📦 Temos 12 unidades de banana nanica no estoque.
```

---

### Teste 4.2 - Consulta de Preço - OK
**Entrada:** `Qual o preço da banana?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
Banana nanica: R$ 0,50 por unidade
```

---

### Teste 4.3 - Listar Todos os Itens - OK
**Entrada:** `Liste tudo do estoque`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
📦 Itens no estoque (22):

1. amido de milho: 500grama (R$8,00)
2. arroz arbóreo: 0grama (R$12,00)
3. açúcar: 2000grama (R$4,50)
4. banana nanica: 12unidade (R$0,50)
5. biscoito champanhe: 300grama (R$20,00)
6. biscoito maisena: 400grama (R$10,00)
...
```

---

### Teste 4.4 - Itens com Estoque Baixo - OK
**Entrada:** `Quais itens têm menos de 5 unidades?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
⚠️ Itens com estoque baixo (menos de 5):

- arroz arbóreo: 0grama
- camarão: 0grama
- caldo de legumes: 0mililitro
- queijo parmesão: 0grama
- vinho branco: 0mililitro
```

---

### Teste 4.5 - Itens Próximos do Vencimento - OK
**Entrada:** `Mostre itens que vencem nos próximos 7 dias`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
⏰ Itens próximos do vencimento (próximos 7 dias):

- banana nanica: 12 unidades (vence em 5 dias - DD/MM/YYYY)
- gema de ovo: 12 unidades (vence em 7 dias - DD/MM/YYYY)
- leite: 2000mililitro (vence em 7 dias - DD/MM/YYYY)
- limão: 5 unidades (vence em 7 dias - DD/MM/YYYY)
```

---

### Teste 4.6 - Itens Vencidos
**Entrada:** `Tem algum item vencido?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRADOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
Nenhum item vencido no estoque.
```
(Ou lista de itens vencidos se houver)

---

### Teste 4.7 - Valor Total do Estoque - OK
**Entrada:** `Quanto vale meu estoque?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
💰 Valor total do estoque: R$ X.XXX,XX
```

---

### Teste 4.8 - Item Não Encontrado
**Entrada:** `Quantos abacaxis tenho?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
Item 'abacaxi' não encontrado no estoque.
```

---

### Teste 4.9 - Detalhes Completos de Um Item
**Entrada:** `Me dê informações sobre o leite`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_READER

**Resposta Esperada:**
```
📦 **leite**
   Quantidade: 2000 mililitro
   Preço: R$5,00 por litro
   Descrição: leite integral
   Validade: DD/MM/YYYY (daqui a 7 dias)
```

---

## 5. Testes do TRANSACTION_READER - OK

### Teste 5.1 - Histórico de Um Item Específico
**Entrada:** `Mostre o histórico da banana`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_TRANSACTION → TRANSACTION_READER

**Resposta Esperada:**
```
📊 Histórico de banana nanica:

DD/MM/YYYY - ENTRADA: compra inicial de estoque
   Quantidade: +20 unidades
   Valor: R$0,50

DD/MM/YYYY - SAÍDA: uso em receita: torta banoffee
   Quantidade: -4 unidades

DD/MM/YYYY - SAÍDA: uso em receita: pavê de banana
   Quantidade: -4 unidades
```

---

### Teste 5.2 - Últimas N Transações
**Entrada:** `Mostre as últimas 10 transações`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_TRANSACTION → TRANSACTION_READER

**Resposta Esperada:**
```
📊 Histórico de Transações (últimas 10):

📅 DD/MM/YYYY
   SAÍDA: consumo direto
   Item: leite
   Quantidade: -520 mililitro

📅 DD/MM/YYYY
   SAÍDA: uso em receita: pavê de banana
   Item: leite
   Quantidade: -480 mililitro
   
...
```

---

### Teste 5.3 - Total Gasto em Compras - OK
**Entrada:** `Quanto gastei em compras este mês?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_TRANSACTION → TRANSACTION_READER

**Resposta Esperada:**
```
💰 Total gasto em compras este mês: R$ XXX,XX

Detalhamento:
- XX transações de compra
- Total de itens: XX
```

---

### Teste 5.4 - Itens Mais Usados - OK
**Entrada:** `Quais ingredientes mais uso?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_TRANSACTION → TRANSACTION_READER

**Resposta Esperada:**
```
📊 Itens mais usados (por quantidade):

1. açúcar - 3000g (em 1 transação)
2. chocolate em pó - 600g (em 2 transações)
3. leite - 1000ml (em 2 transações)
4. banana nanica - 12 unidades (em 3 transações)
...
```

---

### Teste 5.5 - Perdas do Mês
**Entrada:** `Quais itens perdi este mês?`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_TRANSACTION → TRANSACTION_READER

**Resposta Esperada:**
```
Nenhuma perda registrada este mês.
```
(Ou lista de perdas se houver transações do tipo "perda")

---

### Teste 5.6 - Balanço de Entradas e Saídas
**Entrada:** `Me mostre o balanço do estoque da manteiga`

**Fluxo Esperado:** Orchestrator → SQL_ORCHESTRATOR → SQL_TRANSACTION → TRANSACTION_READER

**Resposta Esperada:**
```
📊 Balanço de manteiga:

Total de entradas: +500g
Total de saídas: -300g
Saldo: +200g
Estoque atual: 200g
```

---

## 6. Testes do STRUCTURER_RECIPE + RECIPE_WRITER

### Teste 6.1 - Salvar Receita Simples
**Entrada:** `Salve essa receita: Vitamina de Banana. Ingredientes: 2 bananas, 1 copo de leite, 1 colher de açúcar. Modo de preparo: Bata tudo no liquidificador e sirva gelado.`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → STRUCTURER_RECIPE
- STRUCTURER_RECIPE → estrutura dados
- RECIPE_WRITER → usa add_recipe_tool

**Resposta Esperada:**
```
Sucesso! A receita 'Vitamina de Banana' foi salva no banco de dados com seus ingredientes.
```

---

### Teste 6.2 - Salvar Receita da Web
**Contexto:** Usuário buscou "receita de bolo de chocolate" na web e recebeu a receita completa

**Entrada:** `Sim, quero salvar a receita de bolo de chocolate`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → STRUCTURER_RECIPE
- STRUCTURER analisa histórico da conversa
- Extrai a receita mencionada anteriormente
- RECIPE_WRITER → insere no banco

**Resposta Esperada:**
```
Sucesso! A receita 'Bolo de Chocolate' foi salva no banco de dados com seus ingredientes.
```

---

### Teste 6.3 - Salvar Múltiplas Receitas
**Entrada:** `Salve essas receitas: 1) Suco Verde - ingredientes: couve, limão, água. Preparo: bata tudo. 2) Smoothie de Banana - ingredientes: banana, leite, mel. Preparo: bata e sirva.`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → STRUCTURER_RECIPE
- STRUCTURER → estrutura 2 receitas
- RECIPE_WRITER → insere ambas

**Resposta Esperada:**
```
Sucesso! 2 receitas foram salvas no banco de dados.
```

---

## 7. Testes do STRUCTURER_ITEM + ITEM_WRITER + TRANSACTION_WRITER

### Teste 7.1 - Adicionar Item Simples
**Entrada:** `Adicione 500g de café ao estoque pelo preço de R$15`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → STRUCTURER_ITEM
- STRUCTURER_ITEM → estrutura: `{item_data: {...}, transaction_data: {...}}`
- ITEM_WRITER → usa add_item_tool → retorna item_id
- TRANSACTION_WRITER (paralelo) → registra transação de compra

**Resposta Esperada:**
```
Sucesso! Item 'café' adicionado ao estoque: 500grama.
✓ Transação registrada: Compra de café - 500grama por R$15,00
```

---

### Teste 7.2 - Adicionar Item com Validade
**Entrada:** `Adicione 2 litros de leite, validade 15/01/2026, preço R$4 o litro`

**Fluxo Esperado:** 
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → STRUCTURER_ITEM
- STRUCTURER → converte data para formato ISO
- ITEM_WRITER + TRANSACTION_WRITER

**Resposta Esperada:**
```
Sucesso! Item 'leite' adicionado ao estoque: 2litro.
✓ Transação registrada: Compra de leite - 2litro por R$4,00
```

---

### Teste 7.3 - Adicionar Múltiplos Itens
**Entrada:** `Comprei: 5kg de arroz por R$25, 1kg de feijão por R$8, e 12 ovos por R$6`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → STRUCTURER_ITEM
- STRUCTURER → estrutura 3 itens
- ITEM_WRITER → insere os 3
- TRANSACTION_WRITER → registra 3 transações

**Resposta Esperada:**
```
Sucesso! 3 itens foram adicionados ao estoque.
✓ Transação registrada: Compra de arroz - 5kg por R$25,00
✓ Transação registrada: Compra de feijão - 1kg por R$8,00
✓ Transação registrada: Compra de ovos - 12unidade por R$6,00
```

---

### Teste 7.4 - Adicionar Item Sem Preço
**Entrada:** `Adicione 3 tomates ao estoque`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → STRUCTURER_ITEM
- STRUCTURER → price=0, price em transaction_data=null
- ITEM_WRITER + TRANSACTION_WRITER

**Resposta Esperada:**
```
Sucesso! Item 'tomate' adicionado ao estoque: 3unidade.
✓ Transação registrada: Compra de tomate - 3unidade
```

---

## 8. Testes do ITEM_WRITER (UPDATE/DELETE)

### Teste 8.1 - Usar Ingrediente (UPDATE tipo uso)
**Entrada:** `Usei 200g de farinha`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_WRITER (direto, sem STRUCTURER)
- ITEM_WRITER → usa update_item_tool
- Tool retorna dados de transação
- TRANSACTION_WRITER → registra uso

**Resposta Esperada:**
```
Sucesso! farinha de trigo atualizado: 800grama (usou 200grama).
✓ Transação registrada: Uso de farinha de trigo - 200grama
```

---

### Teste 8.2 - Vender Item (UPDATE tipo venda)
**Entrada:** `Vendi 5 bananas por R$2,50`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_WRITER
- ITEM_WRITER → update_item_tool
- TRANSACTION_WRITER → registra venda

**Resposta Esperada:**
```
Sucesso! banana nanica atualizado: 7unidade (vendeu 5unidade).
✓ Transação registrada: Venda de banana nanica - 5unidade por R$2,50
```

---

### Teste 8.3 - Ajustar Estoque (UPDATE tipo ajuste)
**Entrada:** `Corrija a quantidade de açúcar para 3kg`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_WRITER
- ITEM_WRITER → update_item_tool com new_amount=3000
- TRANSACTION_WRITER → registra ajuste

**Resposta Esperada:**
```
Sucesso! açúcar ajustado: 3000grama (+1000grama).
✓ Transação registrada: Ajuste de estoque de açúcar: de 2000grama para 3000grama (+1000grama)
```

---

### Teste 8.4 - Deletar Item Vencido (DELETE tipo perda)
**Entrada:** `Remova o leite vencido do estoque`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_WRITER
- ITEM_WRITER → delete_item_tool com reason="perda"
- TRANSACTION_WRITER → registra perda

**Resposta Esperada:**
```
Sucesso! Item 'leite' removido do estoque (2000mililitro).
✓ Transação registrada: Remoção de leite do estoque - 2000mililitro
```

---

### Teste 8.5 - Atualizar Preço
**Entrada:** `Atualize o preço da banana para R$0,80`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_WRITER
- ITEM_WRITER → update_item_tool com new_price=0.80
- TRANSACTION_WRITER → NÃO registra (só mudou preço, não quantidade)

**Resposta Esperada:**
```
Sucesso! banana nanica atualizado (preço/validade).
```

---

### Teste 8.6 - Tentar Usar Mais do Que Tem (Validação)
**Entrada:** `Usei 200g de farinha`

**Fluxo Esperado:**
- Orchestrator → SQL_ORCHESTRATOR → SQL_ITEM → ITEM_WRITER
- ITEM_WRITER → update_item_tool valida quantidade
- Retorna erro

**Resposta Esperada:**
```
Operação resultaria em quantidade negativa. Quantidade atual: 1000grama.
```

---

## 9. Testes do REVISOR

### Teste 9.1 - Finalizar com Resposta Completa
**Contexto:**
- Pergunta: "Quantas bananas tenho?"
- Resposta SQL: "📦 Temos 12 unidades de banana nanica no estoque."

**Decisão Esperada:** `nextAgent: FINALIZAR`

**Justificativa:** Resposta completa e satisfatória

---

### Teste 9.2 - Ir para WEB (Receita Não Encontrada)
**Contexto:**
- Pergunta: "Como fazer bolo de chocolate?"
- Resposta SQL: "Receita 'bolo de chocolate' não encontrada no banco de dados."

**Decisão Esperada:** `nextAgent: WEB`
**Query Web:** `"receita bolo de chocolate com ingredientes"`

**Justificativa:** Receita não cadastrada, precisa buscar na web

---

### Teste 9.3 - Finalizar com Alternativas (Receita Indisponível)
**Contexto:**
- Pergunta: "Posso fazer risoto de camarão?"
- Resposta SQL: "Infelizmente NÃO é possível... Faltam: X, Y, Z... Mas posso sugerir: 1. Torta Banoffee 2. Pavê..."

**Decisão Esperada:** `nextAgent: FINALIZAR`

**Justificativa:** Resposta COMPLETA (informou falta + deu alternativas)

---

### Teste 9.4 - Finalizar com Operação Bem-Sucedida
**Contexto:**
- Pergunta: "Adicione café ao estoque"
- Resposta SQL: "Sucesso! Item 'café' adicionado. Transação registrada."

**Decisão Esperada:** `nextAgent: FINALIZAR`

**Justificativa:** Operação concluída com sucesso

---

## 10. Testes do Agente WEB

### Teste 10.1 - Buscar Receita Não Cadastrada
**Entrada:** `Como fazer bolo de chocolate?`

**Fluxo Esperado:**
1. Orchestrator → SQL_ORCHESTRATOR → SQL_RECIPE → RECIPE_READER
2. Não encontra
3. REVISOR → WEB
4. WEB → busca receita

**Resposta Esperada:**
```
**Bolo de Chocolate**

**Ingredientes:**
- 2 xícaras de farinha de trigo
- 2 xícaras de açúcar
- 3/4 xícara de chocolate em pó
- 2 ovos
- 1 xícara de leite
- 1/2 xícara de óleo
- 1 colher de sopa de fermento

**Modo de Preparo:**
1. Misture os ingredientes secos
2. Adicione os líquidos e mexa bem
3. Despeje em forma untada
4. Asse a 180°C por 40 minutos

**Tempo de Preparo:** 50 minutos
**Dificuldade:** Fácil

Gostaria de salvar alguma receita no banco de dados? Se sim, qual?
```

---

### Teste 10.2 - Buscar Receita Específica
**Entrada:** `Busque receita de lasanha vegetariana`

**Fluxo Esperado:** Orchestrator → SQL → Revisor → WEB

**Resposta Final:** Receita completa + pergunta sobre salvar

---

## 11. Testes de Fluxo Completo

### Teste 11.1 - Fluxo: Buscar → Salvar → Verificar
**Sequência:**

1. **Entrada:** `Busque uma receita de panqueca americana`
   - **Fluxo:** Orchestrator → SQL → Revisor → WEB
   - **Resposta:** Receita completa + "Gostaria de salvar?"

2. **Entrada:** `Sim, salve a receita de panqueca`
   - **Fluxo:** Orchestrator → SQL → SQL_RECIPE → STRUCTURER_RECIPE → RECIPE_WRITER
   - **Resposta:** "Sucesso! A receita 'Panqueca Americana' foi salva."

3. **Entrada:** `Consigo fazer panqueca americana?`
   - **Fluxo:** Orchestrator → SQL → SQL_RECIPE → RECIPE_READER (check_recipe_availability)
   - **Resposta:** Lista ingredientes + verificação de disponibilidade

---

### Teste 11.2 - Fluxo: Comprar → Usar → Ver Histórico
**Sequência:**

1. **Entrada:** `Adicione 1kg de café ao estoque, R$35`
   - **Fluxo:** Orchestrator → SQL → SQL_ITEM → STRUCTURER_ITEM → ITEM_WRITER + TRANSACTION_WRITER
   - **Resposta:** "Item adicionado" + "Transação registrada"

2. **Entrada:** `Usei 200g de café`
   - **Fluxo:** Orchestrator → SQL → SQL_ITEM → ITEM_WRITER + TRANSACTION_WRITER
   - **Resposta:** "café atualizado: 800g (usou 200g). Transação registrada."

3. **Entrada:** `Mostre o histórico do café`
   - **Fluxo:** Orchestrator → SQL → SQL_TRANSACTION → TRANSACTION_READER
   - **Resposta:** Lista com compra + uso

---

### Teste 11.3 - Fluxo: Verificar Disponibilidade → Adicionar Faltantes → Fazer Receita
**Sequência:**

1. **Entrada:** `Posso fazer risoto de camarão?`
   - **Resposta:** "Não, faltam: arroz arbóreo, camarão, vinho..."

2. **Entrada:** `Adicione 500g de arroz arbóreo, 600g de camarão, 200ml de vinho branco`
   - **Resposta:** "3 itens adicionados. 3 transações registradas."

3. **Entrada:** `Agora consigo fazer risoto de camarão?`
   - **Resposta:** "SIM! Você pode fazer 'risoto de camarão'!"

---

## 12. Testes de Casos Extremos

### Teste 12.1 - Pergunta Ambígua
**Entrada:** `Tem chocolate?`

**Resposta Esperada:**
```
📦 **chocolate em pó**
   Quantidade: 400 grama
   Preço: R$40,00 por kg
   Descrição: chocolate em pó ou cacau
```

---

### Teste 12.2 - Múltiplos Itens com Nome Similar
**Entrada:** `Quantos biscoitos tenho?`

**Resposta Esperada:**
```
Encontrei 2 itens relacionados a "biscoito":

📦 biscoito maisena: 400grama
📦 biscoito champanhe: 300grama
```

---

### Teste 12.3 - Erro de Digitação
**Entrada:** `Quantas bananass tenho?`

**Resposta Esperada:**
```
📦 Temos 12 unidades de banana nanica no estoque.
```
(Sistema tolera erros usando LIKE)

---

### Teste 12.4 - Contexto de Conversa
**Sequência:**

1. **Entrada:** `Quantas bananas tenho?`
   - **Resposta:** "12 unidades"

2. **Entrada:** `E o preço?`
   - **Resposta:** "R$ 0,50 por unidade"
   - (Sistema deve entender que "preço" se refere a banana do contexto)

---

### Teste 12.5 - Item Já Existente
**Entrada:** `Adicione banana nanica ao estoque`

**Resposta Esperada:**
```
Item 'banana nanica' já existe no estoque. Use update para modificar a quantidade.
```

---

## 13. Checklist de Validação

Após executar todos os testes, verifique:

### Roteamento:
- [ ] Orchestrator roteia corretamente: TRIVIAL, WEB, SQL_ORCHESTRATOR
- [ ] SQL_ORCHESTRATOR roteia: SQL_RECIPE, SQL_ITEM, SQL_TRANSACTION
- [ ] SQL_RECIPE roteia: RECIPE_READER, STRUCTURER_RECIPE, RECIPE_WRITER
- [ ] SQL_ITEM roteia: ITEM_READER, STRUCTURER_ITEM, ITEM_WRITER
- [ ] SQL_TRANSACTION sempre vai para TRANSACTION_READER

### Agentes READER:
- [ ] RECIPE_READER executa queries SQL corretamente
- [ ] RECIPE_READER usa check_recipe_availability quando apropriado
- [ ] ITEM_READER consulta itens com LIKE corretamente
- [ ] ITEM_READER formata respostas com unidades e preços
- [ ] TRANSACTION_READER mostra histórico formatado

### Agentes STRUCTURER + WRITER:
- [ ] STRUCTURER_RECIPE extrai receitas do histórico
- [ ] STRUCTURER_RECIPE formata ingredientes corretamente
- [ ] RECIPE_WRITER usa add_recipe_tool
- [ ] STRUCTURER_ITEM separa item_data e transaction_data
- [ ] ITEM_WRITER usa add_item_tool para INSERT
- [ ] ITEM_WRITER usa update_item_tool para UPDATE
- [ ] ITEM_WRITER usa delete_item_tool para DELETE
- [ ] TRANSACTION_WRITER registra transações em paralelo

### Revisor:
- [ ] Decide FINALIZAR quando resposta está completa
- [ ] Decide WEB quando receita não encontrada
- [ ] Decide FINALIZAR mesmo com alternativas sugeridas
- [ ] Decide FINALIZAR para operações bem-sucedidas

### Fluxos Gerais:
- [ ] Sistema mantém contexto entre mensagens
- [ ] Transações são registradas corretamente
- [ ] Validações funcionam (quantidade negativa, item já existe)
- [ ] Erros são tratados adequadamente
- [ ] Mensagens são claras e bem formatadas
- [ ] Emojis são usados apropriadamente

---

**Data dos Testes:** ____/____/________

**Testado por:** _______________________