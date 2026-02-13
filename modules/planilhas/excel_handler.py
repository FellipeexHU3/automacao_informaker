from modules.login.modulo_login import fazer_login
from modules.planilhas.modulo_planilhas import selecionar_planilha
from modules.planilhas.uploader import executar_sequencia_navegacao
from coordenadas import coordenadas
import time
from core.config import config


# modules/planilhas/excel_handler.py (VERSÃO ATUALIZADA)

def automacao_completa(usar_handlers=False):
    """Automação completa - agora com opção de usar handlers"""
    print("🤖 AUTOMAÇÃO COMPLETA")
    print("=" * 50)
    
    # 1. SELECIONAR PLANILHA (antigo ou novo)
    print("📋 SELECIONANDO PLANILHA...")
    try:
        from modules.planilhas.modulo_planilhas import selecionar_planilha
        
        dados_planilha = selecionar_planilha()
        
    except Exception as e:
        print(f"❌ Erro ao selecionar planilha: {e}")
        return
    
    if not dados_planilha:
        print("❌ Nenhuma planilha selecionada")
        return
    
    print(f"\n📊 DADOS DA {dados_planilha['tipo']}:")
    print(f"👥 Candidatos: {dados_planilha['quantidade']}")
    print(f"💰 Valor total: {dados_planilha.get('moeda', 'US$')} {dados_planilha['valor_total']:,.2f}")

    # 2. FAZER LOGIN (mantém igual)
    from modules.login.modulo_login import fazer_login
    driver = fazer_login()
    if not driver:
        return
    
    # 3. EXECUTAR SEQUÊNCIA DE NAVEGAÇÃO (mantém igual)
    from modules.planilhas.uploader import executar_sequencia_navegacao
    executar_sequencia_navegacao(dados_planilha)
    
    # 4. FINALIZAR
    print("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"✅ Dados da {dados_planilha['tipo']} enviados")
    
    driver.quit()