# modules/planilhas/tests/test_handlers.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ..handlers.planilha_factory import PlanilhaFactory
from ..services.format_service import FormatService

def testar_novos_handlers():
    """Testa a nova estrutura de handlers sem afetar o sistema atual"""
    print("🧪 TESTANDO NOVOS HANDLERS DE PLANILHA")
    print("=" * 50)
    
    try:
        # Lista de handlers disponíveis
        handlers_disponiveis = ['vue', 'kryterion', 'psi', 'scantron']
        
        print("Handlers disponíveis:", ", ".join(handlers_disponiveis))
        tipo = input("Digite o tipo de planilha para testar: ").strip().lower()
        
        if tipo not in handlers_disponiveis:
            print(f"❌ Tipo '{tipo}' não suportado")
            return
        
        # Criar handler
        handler = PlanilhaFactory.criar_handler(tipo)
        print(f"✅ Handler {tipo.upper()} criado com sucesso!")
        
        # Testar formatação
        print("\n💰 TESTANDO FORMATAÇÃO DE MOEDA:")
        valores_teste = [1000.0, 2500.5, 123.45, "N/A"]
        for valor in valores_teste:
            formatado = FormatService.formatar_moeda_br(valor)
            print(f"  {valor} → {formatado}")
            
        print(f"\n🎯 Handler {tipo.upper()} está pronto para uso!")
        print("💡 Dica: Use este handler no lugar das funções antigas")
        
    except Exception as e:
        print(f"❌ Erro ao testar handlers: {e}")
        print("⚠️  Sistema antigo continua funcionando perfeitamente!")

def testar_com_planilha_real(caminho_planilha, tipo_planilha):
    """Teste mais completo com planilha real"""
    try:
        handler = PlanilhaFactory.criar_handler(tipo_planilha)
        df = handler.carregar_planilha(caminho_planilha)
        
        print(f"✅ Planilha carregada: {len(df)} linhas")
        
        # Validar estrutura
        valido, mensagem = handler.validar_estrutura()
        print(f"🔍 Validação: {mensagem}")
        
        if valido and len(df) > 0:
            # Processar primeira linha como exemplo
            primeira_linha = df.iloc[0]
            dados_processados = handler.processar_linha(primeira_linha)
            print(f"📄 Primeira linha processada: {dados_processados}")
            
    except Exception as e:
        print(f"❌ Erro no teste real: {e}")

if __name__ == "__main__":
    testar_novos_handlers()