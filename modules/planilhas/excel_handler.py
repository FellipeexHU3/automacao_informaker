from modules.login.modulo_login import fazer_login
from modules.planilhas.modulo_planilhas import selecionar_planilha
from modules.planilhas.uploader import executar_sequencia_navegacao
from coordenadas import coordenadas
import time
from core.config import config


def automacao_completa():
    """Automação completa modularizada"""
    print("🤖 AUTOMAÇÃO COMPLETA - SISTEMA MODULAR")
    print("=" * 50)
    
    # 1. SELECIONAR PLANILHA
    print("📋 SELECIONANDO PLANILHA...")
    try:
        dados_planilha = selecionar_planilha()
    except Exception as e:
        print(f"Erro ao selecionar planilha: {e}")
        return

    
    if not dados_planilha:
        print("❌ Nenhuma planilha selecionada")
        return
    
    print(f"\n📊 DADOS DA {dados_planilha['tipo']}:")
    print(f"👥 Candidatos: {dados_planilha['quantidade']}")
    print(f"💰 Valor total: US$ {dados_planilha['valor_total']:,.2f}")

    # 2. FAZER LOGIN
    driver = fazer_login()
    if not driver:
        return
    
    # 3. EXECUTAR SEQUÊNCIA DE NAVEGAÇÃO
    executar_sequencia_navegacao(dados_planilha)
    if not dados_planilha:
        return
    # 6. FINALIZAR
    print("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"✅ Dados da {dados_planilha['tipo']} enviados")
    
    driver.quit()