"""
Script para gerar variantes do grafo em PNG com diferentes orientações e estilos
"""
import os
import sys
import subprocess
import tempfile

# Adiciona o diretório backend ao path para imports absolutos
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

print("\n=== Gerando Variantes PNG do Grafo LangGraph ===\n")

try:
    from services.graph.graph import graph
    print("✓ Grafo importado com sucesso!\n")
except Exception as e:
    print("✗ Erro ao importar o grafo: %s" % str(e))
    exit(1)

assets_dir = os.path.join(backend_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)

# Primeiro, gera a imagem PNG padrão
print("📊 Gerando imagens PNG:\n")
try:
    print("  ⏳ Gerando graph.png (padrão)...")
    image_data = graph.get_graph().draw_mermaid_png()
    default_path = os.path.join(assets_dir, "graph.png")
    with open(default_path, "wb") as f:
        f.write(image_data)
    print("  ✓ graph.png - Gerado com sucesso (%.2f KB)" % (len(image_data) / 1024))
except Exception as e:
    print("  ✗ Erro ao gerar PNG: %s" % str(e))
    print("\n⚠️  Playwright pode não estar instalado.")
    print("     Execute: pip install playwright && playwright install")
    exit(1)

# Gera o código Mermaid base para as variantes
try:
    mermaid_base = graph.get_graph().draw_mermaid()
except Exception as e:
    print("✗ Erro ao gerar código Mermaid: %s" % str(e))
    exit(1)


# Configurações de variantes (apenas horizontal e compact além do padrão)
variants = {
    "horizontal": {
        "direction": "LR",
        "description": "Horizontal (→)"
    },
    "compact": {
        "direction": "TD",
        "description": "Compacto (↓)"
    }
}

print("\n  Tentando gerar variantes adicionais...\n")

# Para cada variante, modifica o código Mermaid e salva como .mmd temporário
# Infelizmente, o draw_mermaid_png() do LangGraph não aceita parâmetros de customização
# então vamos salvar os .mmd para o usuário converter manualmente
for variant_name, config in variants.items():
    mermaid_code = mermaid_base.replace("graph TD", "graph " + config['direction'])

    # Salva o .mmd
    mmd_path = os.path.join(assets_dir, "graph_" + variant_name + ".mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)

    print("  ℹ️  graph_%s.mmd - %s (para converter manualmente)" % (variant_name, config['description']))

print("\n✅ 1 imagem PNG + 2 arquivos .mmd gerados em: %s" % assets_dir)
print("\n📋 Para gerar PNGs das variantes:")
print("1. Acesse: https://mermaid.live/")
print("2. Cole o conteúdo dos arquivos .mmd")
print("3. Clique em 'Actions' → 'Export PNG'")
print("4. Salve como graph_horizontal.png ou graph_compact.png")
print("\n💡 Alternativa: Use o Mermaid CLI localmente")
print("   npm install -g @mermaid-js/mermaid-cli")
print("   mmdc -i graph_horizontal.mmd -o graph_horizontal.png")


