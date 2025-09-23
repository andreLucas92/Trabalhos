import imagescan
import os
from PIL import Image

def scanner_com_numeracao_sequencial():
    """
    Programa de scanner que grava imagens em formato TIFF com numeração sequencial.
    """
    try:
        
        numero_inicial = int(input("Digite o número inicial para a sequência de arquivos: "))
        proximo_numero = numero_inicial

        
        diretorio_destino = input("Digite o caminho completo da pasta para salvar as imagens: ")

        
        if not os.path.exists(diretorio_destino):
            os.makedirs(diretorio_destino)
            print(f"Diretório '{diretorio_destino}' criado com sucesso.")

        
        scanners = imagescan.list_scanners()
        if not scanners:
            print("Nenhum scanner foi encontrado. Certifique-se de que os drivers estão instalados corretamente.")
            return

        print("\nScanners disponíveis:")
        for i, scanner in enumerate(scanners):
            print(f"{i}: {scanner}")

        
        try:
            indice_scanner = int(input("Selecione o número do scanner que deseja usar: "))
            scanner_selecionado = scanners[indice_scanner]
        except (ValueError, IndexError):
            print("Seleção de scanner inválida.")
            return

        print(f"\nUsando o scanner: {scanner_selecionado}")
        print("Prepare-se para digitalizar. Pressione Enter para iniciar a digitalização ou 's' para sair.")

        while True:
            comando = input()
            if comando.lower() == 's':
                break

            try:
              
                imagem_pil = imagescan.scan(scanner_selecionado)

              
                nome_arquivo = f"imagem_{proximo_numero:04d}.tif"
                caminho_completo = os.path.join(diretorio_destino, nome_arquivo)

              
                imagem_pil.save(caminho_completo, format='TIFF')

                print(f"Imagem salva com sucesso como: {caminho_completo}")

              
                proximo_numero += 1

                print("\nPressione Enter para a próxima digitalização ou 's' para sair.")

            except Exception as e:
                print(f"Ocorreu um erro durante a digitalização: {e}")
                print("Verifique se o scanner está conectado e pronto.")
                break

        print("Programa finalizado.")

    except ValueError:
        print("Por favor, digite um número válido para o início da sequência.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    scanner_com_numeracao_sequencial()