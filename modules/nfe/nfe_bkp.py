import os
import shutil
from datetime import datetime
from openpyxl import load_workbook
import pandas as pd

def criar_backup_com_formato(caminho_original):
    """Cria backup que mantém TODA a formatação original"""
    if not os.path.exists(caminho_original):
        return caminho_original
    
    # Gerar nome do backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = os.path.basename(caminho_original)
    nome_base, extensao = os.path.splitext(nome_arquivo)
    
    caminho_backup = caminho_original.replace(
        nome_arquivo, 
        f"{nome_base}_BACKUP_{timestamp}{extensao}"
    )
    
    # 🔥 COPIAR MANTENDO FORMATAÇÃO COMPLETA
    shutil.copy2(caminho_original, caminho_backup)
    print(f"📦 Backup com formatação criado: {caminho_backup}")
    return caminho_backup

def exportar_com_formato(nfe, caminho_saida=None):
    """Exporta dados mantendo a formatação original da planilha"""
    try:
        if caminho_saida is None:
            caminho_saida = nfe.caminho_planilha
        
        # 🔥 CARREGAR COM OPENPYXL PARA MANTER FORMATAÇÃO
        book = load_workbook(nfe.caminho_planilha)
        writer = pd.ExcelWriter(caminho_saida, engine='openpyxl')
        writer.book = book
        writer.sheets = {ws.title: ws for ws in book.worksheets}
        
        # Localizar a aba ativa (onde estão os dados)
        sheet_name = book.active.title
        
        # Atualizar APENAS os dados, mantendo formatação
        df = pd.DataFrame(nfe.notas)
        
        # Limpar dados antigos (mas manter formatação)
        sheet = book[sheet_name]
        sheet.delete_rows(2, sheet.max_row)  # Mantém cabeçalho na linha 1
        
        # Escrever novos dados mantendo a estrutura
        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                sheet.cell(row=row_idx+2, column=col_idx+1, value=value)
        
        writer.save()
        print(f"💾 Planilha salva com formatação: {caminho_saida}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar com formatação: {e}")
        # Fallback: salvar normal
        return nfe.exportar_planilha_atualizada(caminho_saida)

def atualizar_apenas_celulas(nfe, caminho_planilha):
    """Atualiza APENAS as células necessárias, mantendo TODO o resto"""
    try:
        # Carregar workbook existente
        wb = load_workbook(caminho_planilha)
        ws = wb.active
        
        # Mapeamento de colunas
        colunas = list(nfe.notas[0].keys()) if nfe.notas else []
        
        # Atualizar APENAS as colunas de NFSe e Autenticidade
        for nota in nfe.notas_pendentes:
            linha_planilha = nota['indice_planilha']  # Ex: linha 480
            indice_array = nota['indice_array']
            
            # Encontrar colunas NFSe e Autenticidade
            for col_idx, col_name in enumerate(colunas, 1):
                if col_name == 'NFSe':
                    col_nfse = col_idx
                elif col_name == 'Autenticidade':
                    col_auth = col_idx
            
            # Atualizar APENAS essas células
            if 'col_nfse' in locals() and nfe.notas[indice_array].get('NFSe'):
                ws.cell(row=linha_planilha, column=col_nfse, value=nfe.notas[indice_array]['NFSe'])
            
            if 'col_auth' in locals() and nfe.notas[indice_array].get('Autenticidade'):
                ws.cell(row=linha_planilha, column=col_auth, value=nfe.notas[indice_array]['Autenticidade'])
        
        wb.save(caminho_planilha)
        print(f"🎨 Células atualizadas mantendo formatação: {caminho_planilha}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar células: {e}")
        return False