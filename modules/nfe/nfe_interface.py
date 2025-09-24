import sys
import os
from datetime import datetime
from modules.nfe.nfe_core import NFE
from modules.nfe.nfe_config import CONFIG_NFE
from modules.nfe.nfe_automacao import AutomacaoNFE
from .nfe_utils import gerar_relatorio_processamento, validar_dados_nota
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def menu_nfe():
    """Menu principal do módulo NFE"""
    print("\n" + "=" * 60)
    print("📄 SISTEMA DE AUTOMAÇÃO NFE - NOTA FISCAL ELETRÔNICA")
    print("=" * 60)
    
    print("1 - Carregar planilha")
    print("2 - Ver notas pendentes")
    print("3 - Ver notas processadas")
    print("4 - Processar próxima nota (Automático)")
    print("5 - Processar todas pendentes (Automático)")
    print("6 - Exportar planilha atualizada")
    print("7 - Ver credenciais do sistema")
    print("8 - Voltar ao menu principal")
    
    opcao = input("\nDigite sua opção: ")
    return opcao

def automacao_nfe():
    """Função principal de automação NFE"""
    nfe = None
    automacao = None
    
    while True:
        opcao = menu_nfe()
        
        if opcao == "1":
            try:
                nfe = NFE()
                automacao = AutomacaoNFE(nfe)
                print(f"✅ Planilha {nfe.tipo_planilha} carregada com {len(nfe.notas)} notas")
            except Exception as e:
                print(f"❌ Erro ao carregar planilha: {e}")
                
        elif opcao == "2":
            if nfe:
                pendentes = nfe.listar_notas_pendentes()
                print(f"\n📋 Notas Pendentes ({len(pendentes)}):")
                for nota in pendentes:
                    print(f"  Linha {nota['linha_planilha']}: {nota['data']} - {nota['cliente']} - R$ {nota['valor']}")
            else:
                print("❌ Nenhuma planilha carregada")
        
        elif opcao == "3":
            if nfe:
                processadas = nfe.listar_notas_processadas()
                print(f"\n✅ Notas Processadas ({len(processadas)}):")
                for nota in processadas:
                    print(f"  Linha {nota['linha_planilha']}: {nota['cliente']} - NFS-e: {nota['nfse']}")
            else:
                print("❌ Nenhuma planilha carregada")
        
        elif opcao == "4":
            if nfe and automacao:
                processar_proxima_nota_automatico(nfe, automacao)
            else:
                print("❌ Nenhuma planilha carregada ou automação não inicializada")
        
        elif opcao == "5":
            if nfe and automacao:
                processar_todas_notas_automatico(nfe, automacao)
            else:
                print("❌ Nenhuma planilha carregada ou automação não inicializada")
        
        elif opcao == "6":
            if nfe:
                caminho = input("Caminho para salvar (Enter para sobrescrever): ").strip()
                if nfe.exportar_planilha_atualizada(caminho or None):
                    print("✅ Planilha exportada com sucesso!")
                else:
                    print("❌ Erro ao exportar planilha")
            else:
                print("❌ Nenhuma planilha carregada")
        
        elif opcao == "7":
            if nfe:
                credenciais = nfe.get_credenciais()
                print("\n🔐 Credenciais do Sistema NFE:")
                for key, value in credenciais.items():
                    print(f"  {key}: {value}")
            else:
                print("❌ Nenhuma planilha carregada")
        
        elif opcao == "8":
            if automacao:
                automacao.finalizar()
            break
        
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

def processar_proxima_nota_automatico(nfe: NFE, automacao: AutomacaoNFE):
    """Processa a próxima nota pendente automaticamente"""
    proxima = nfe.obter_proxima_nota_pendente()
    
    if not proxima:
        print("✅ Todas as notas já foram processadas!")
        return
    
    print(f"\n🔄 Processando nota linha {proxima['linha_planilha']}:")
    print(f"   Data: {proxima['dados'].get('103', 'N/A')}")
    print(f"   Cliente: {proxima['dados'].get('Nome', 'N/A')}")
    print(f"   Valor: R$ {proxima['dados'].get('Valor', 'N/A')}")
    print(f"   CPF: {proxima['dados'].get('CPF', 'N/A')}")
    
    # Validar dados obrigatórios
    if not validar_dados_nota(proxima['dados'], CONFIG_NFE['campos_obrigatorios']):
        print("❌ Dados da nota incompletos, pulando...")
        return
    
    # Iniciar navegador e processar
    print("🌐 Iniciando navegador...")
    if not automacao.iniciar_navegador():
        print("❌ Falha ao iniciar navegador")
        return
    
    try:
        print("📝 Processando nota no sistema...")
        sucesso = automacao.processar_nota(proxima)
        
        if sucesso:
            print("✅ Nota processada com sucesso!")
        else:
            print("❌ Falha ao processar nota")
    
    finally:
        automacao.finalizar()

def processar_todas_notas_automatico(nfe: NFE, automacao: AutomacaoNFE):
    """Processa todas as notas pendentes automaticamente"""
    total = len(nfe.notas_pendentes)
    
    if total == 0:
        print("✅ Todas as notas já foram processadas!")
        return
    
    print(f"🔃 Processando {total} notas pendentes automaticamente...")
    
    for i in range(total):
        processar_proxima_nota_automatico(nfe, automacao)
        
        if i < total - 1:  # Não pergunta após a última nota
            continuar = input("\nProcessar próxima nota? (s/n): ").lower()
            if continuar != 's':
                break
    
    print(gerar_relatorio_processamento(nfe))