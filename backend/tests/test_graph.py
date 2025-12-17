import sys
from pathlib import Path
import warnings

# Suprimir warnings do langchain_tavily
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_tavily")

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from services.graph.graph import graph

thread = {"configurable": {"thread_id": "3"}}

def main():
    print("Assistente de Culinária iniciado!")
    print("Digite 'sair' para encerrar.\n")

    while True:
        msg = input("\nVocê: ")

        if msg.lower() in ['sair', 'exit', 'quit']:
            print("Até logo!")
            break

        if not msg.strip():
            continue

        for s in graph.stream({
            'user_input': msg,
        }, thread):
            print(s)

        # response = graph.invoke({'user_input':msg}, {"configurable": {"thread_id": 1}})
        #
        # print(response)

if __name__ == "__main__":
    main()