# Visualizações do Grafo LangGraph

Este diretório contém as visualizações do grafo de agentes do sistema.

## 📁 Arquivos

- **graph.png** - Imagem PNG do grafo gerada automaticamente
- **graph.mmd** - Código Mermaid com configurações otimizadas
- **graph_*.mmd** - Variantes com diferentes estilos e orientações

## 🔧 Como Gerar

### Gerar imagem PNG padrão:
```bash
# Dentro do container Docker
docker-compose exec backend python utils/generate_graph_image.py
```

### Gerar variantes com diferentes estilos:
```bash
# Dentro do container Docker
docker-compose exec backend python utils/generate_graph_variants.py
```

## 🎨 Variantes Disponíveis

### 1. **Default** (graph_default.mmd)
- Orientação: Vertical (Top-Down)
- Tema: Azul claro
- Melhor para: Visualização geral

### 2. **Horizontal** (graph_horizontal.mmd)
- Orientação: Horizontal (Left-Right)
- Tema: Verde
- Melhor para: Grafos largos, apresentações em widescreen

### 3. **Compact** (graph_compact.mmd)
- Orientação: Vertical
- Tema: Rosa
- Espaçamento reduzido
- Melhor para: Grafos densos com muitos nós

### 4. **Minimal** (graph_minimal.mmd)
- Orientação: Vertical
- Tema: Neutro (preto/branco)
- Melhor para: Documentação técnica, impressão

## 🌐 Visualizar Online

1. Acesse [Mermaid Live Editor](https://mermaid.live/)
2. Cole o conteúdo de qualquer arquivo `.mmd`
3. Ajuste zoom e configurações conforme necessário
4. Exporte como PNG de alta qualidade

## 🎯 Dicas de Personalização

### Mudar a direção do fluxo:
Edite a primeira linha do arquivo `.mmd`:
- `graph TD` - Top to Down (vertical, de cima para baixo)
- `graph LR` - Left to Right (horizontal, da esquerda para direita)
- `graph BT` - Bottom to Top (vertical, de baixo para cima)
- `graph RL` - Right to Left (horizontal, da direita para esquerda)

### Ajustar espaçamento:
No bloco `%%{init...`, modifique:
- `nodeSpacing` - Espaço entre nós no mesmo nível
- `rankSpacing` - Espaço entre níveis diferentes
- `padding` - Margem interna dos nós

### Alterar cores:
Modifique o objeto `themeVariables`:
- `primaryColor` - Cor de fundo dos nós principais
- `primaryBorderColor` - Cor da borda dos nós
- `lineColor` - Cor das setas/conexões

## 📊 Estrutura do Grafo

O grafo representa o fluxo de agentes do sistema:

1. **Orchestrator** - Ponto de entrada, roteia para agentes especializados
2. **SQL Orchestrator** - Gerencia operações de banco de dados
3. **Agentes Especializados**:
   - SQL Recipe (receitas)
   - SQL Item (itens/estoque)
   - SQL Transaction (transações)
4. **Revisor** - Valida e revisa respostas
5. **Web** - Busca informações externas quando necessário
6. **Trivial** - Responde perguntas simples diretamente

## 🔄 Atualização

Para atualizar as visualizações após mudanças no grafo, execute novamente os scripts de geração dentro do container Docker.

