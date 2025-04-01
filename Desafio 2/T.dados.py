import tabula
import pandas as pd
import zipfile
import os

# 1. Configuração
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Corrigido __file__
csv_filename = os.path.join(SCRIPT_DIR, "Rol_Procedimentos_Completo.csv")
zip_filename = os.path.join(SCRIPT_DIR, "Teste_Rol_Procedimentos_Completo.zip")

# 2. Verificação do arquivo PDF
pdf_path = os.path.join(SCRIPT_DIR, r"C:\Users\ledea\Downloads\teste nivelamento_Leticia\Desafio 1\meus_pdfs\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")

if not os.path.exists(pdf_path):
    print(f"Erro: Arquivo PDF não encontrado em {pdf_path}")
    exit()

# 3. Extração das tabelas
try:
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True, lattice=True)
    if not tables:
        print("Erro: Nenhuma tabela encontrada no PDF.")
        exit()
except Exception as e:
    print(f"Erro ao extrair PDF: {e}")
    exit()

# 4. Processamento dos dados
try:
    df_combined = pd.concat(tables, ignore_index=True)
    if df_combined.empty:
        print("Erro: DataFrame está vazio. Nada para salvar.")
        exit()
except Exception as e:
    print(f"Erro ao processar tabelas: {e}")
    exit()

# 5. Geração do CSV
try:
    df_combined.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    if not os.path.exists(csv_filename):
        print("Erro: O arquivo CSV não foi criado corretamente.")
        exit()
    print(f"✓ CSV criado em: {csv_filename}")
    print(f"Tamanho do CSV: {os.path.getsize(csv_filename)} bytes")
except Exception as e:
    print(f"Erro ao criar CSV: {e}")
    exit()

# 6. Compactação do CSV para ZIP
try:
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_filename, arcname=os.path.basename(csv_filename))

    # Verificação do ZIP
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        file_list = zipf.namelist()
        print(f"✓ ZIP criado em: {zip_filename}")
        print(f"Conteúdo do ZIP: {file_list}")
        print(f"Tamanho do ZIP: {os.path.getsize(zip_filename)} bytes")

        if not file_list:
            print("AVISO: O ZIP está vazio!")
            os.remove(zip_filename)  # Remove ZIP inválido
except Exception as e:
    print(f"Erro ao criar ZIP: {e}")
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    