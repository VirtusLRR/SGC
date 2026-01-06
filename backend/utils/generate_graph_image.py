import os
import sys

# Adiciona o diretório backend ao path para imports absolutos
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from services.graph.graph import graph
print("Grafo importado com sucesso!")
print("\n--- Gerando PNG do Grafo via Mermaid (Requer Playwright!) ---")

try:
    # Configurações de renderização para melhor organização visual
    draw_options = {
        "curve": "basis",  # Curvas suaves nas setas
        "wrap_label": True,  # Quebra labels longos
    }

    # Gera a imagem do grafo com configurações otimizadas
    try:
        # Tenta com as opções (algumas versões do LangGraph suportam)
        image_data = graph.get_graph().draw_mermaid_png(
            curve_style="basis",
            background_color="white",
            output_file_path=None
        )
    except TypeError:
        # Fallback para versão sem parâmetros
        image_data = graph.get_graph().draw_mermaid_png()

    # Define o caminho para salvar a imagem na pasta backend/assets
    assets_dir = os.path.join(backend_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    image_path = os.path.join(assets_dir, "graph.png")

    # Salva a imagem
    with open(image_path, "wb") as f:
        f.write(image_data)

    print(f"✓ Grafo PNG gerado e salvo com sucesso em: {image_path}")
    print(f"  Tamanho: {len(image_data) / 1024:.2f} KB")

except Exception as e:
    print(f"\n✗ Erro ao tentar gerar o PNG do grafo: {e}")
    print("\nIsso pode ocorrer por:")
    print("1. O método `.draw_mermaid_png()` não existe na sua versão do LangGraph.")
    print("2. Faltam dependências como 'playwright' ou seus drivers não foram instalados.")
    print("   Tente: pip install playwright && playwright install")
    print("3. Outro erro inesperado ao acessar o grafo ou renderizar.")

    print("\n--- Tentando gerar apenas o código Mermaid (Fallback) ---")
    try:
        mermaid_code = graph.get_graph().draw_mermaid()

        # Adiciona configurações de layout ao código Mermaid
        mermaid_enhanced = f"""%%{{init: {{'theme':'base', 'themeVariables': {{'primaryColor':'#e3f2fd','primaryTextColor':'#000','primaryBorderColor':'#1976d2','lineColor':'#1976d2','secondaryColor':'#fff3e0','tertiaryColor':'#f3e5f5'}},'flowchart':{{'curve':'basis','padding':20,'nodeSpacing':80,'rankSpacing':100}}}}}}%%
{mermaid_code}"""

        # Salva o código Mermaid em um arquivo na pasta backend/assets
        mermaid_path = os.path.join(backend_dir, "assets", "graph.mmd")
        with open(mermaid_path, "w", encoding="utf-8") as f:
            f.write(mermaid_enhanced)

        print(f"\n✓ Código Mermaid gerado e salvo em: {mermaid_path}")
        print("\n📋 Instruções para gerar PNG com melhor qualidade:")
        print("1. Acesse: https://mermaid.live/")
        print("2. Cole o conteúdo do arquivo graph.mmd")
        print("3. Ajuste o zoom e orientação conforme necessário")
        print("4. Clique em 'Export PNG' para baixar")
        print("\n💡 Dica: Use 'TB' (top-bottom) ou 'LR' (left-right) para mudar a direção")
        print("   Edite a primeira linha do .mmd de 'graph TD' para 'graph LR' se preferir horizontal")

    except Exception as e_mermaid:
        print(f"✗ Erro ao gerar código Mermaid: {e_mermaid}")
        print("Verifique se 'graph.get_graph()' está correto e acessível.")

