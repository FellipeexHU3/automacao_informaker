# teste_imports.py
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(__file__))

print("🧪 TESTANDO IMPORTS...")

try:
    from modules.planilhas.core.base_planilha import BasePlanilhaHandler
    print("✅ BasePlanilhaHandler importado!")
except ImportError as e:
    print(f"❌ Erro BasePlanilhaHandler: {e}")

try:
    from modules.planilhas.handlers.vue_handler import VuePlanilhaHandler
    print("✅ VuePlanilhaHandler importado!")
except ImportError as e:
    print(f"❌ Erro VuePlanilhaHandler: {e}")

try:
    from modules.planilhas.handlers.planilha_factory import PlanilhaFactory
    print("✅ PlanilhaFactory importado!")
    
    # Teste criar handler
    handler = PlanilhaFactory.criar_handler('vue')
    print(f"✅ Handler criado: {handler.nome_planilha}")
    
except ImportError as e:
    print(f"❌ Erro PlanilhaFactory: {e}")