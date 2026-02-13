# modules/planilhas/handlers/planilha_factory.py
import pandas as pd
import os
import traceback

class PlanilhaFactory:
    @staticmethod
    def processar_planilha_completa(caminho_planilha, tipo_planilha):
        """
        Processa planilha usando o sistema de handlers
        """
        print(f"🔧 DEBUG: Iniciando processamento para {tipo_planilha}")
        print(f"🔧 DEBUG: Caminho: {caminho_planilha}")
        
        try:
            # 👇 ADICIONE ESTES IMPORTS COM DEBUG
            print("🔧 DEBUG: Tentando importar handlers...")
            
            try:
                from modules.planilhas.handlers.vue_handler import VuePlanilhaHandler
                print("✅ DEBUG: VueHandler importado")
            except ImportError as e:
                print(f"❌ DEBUG: Erro importando VueHandler: {e}")
                traceback.print_exc()
            
            try:
                from modules.planilhas.handlers.kryterion_handler import KryterionPlanilhaHandler
                print("✅ DEBUG: KryterionHandler importado")
            except ImportError as e:
                print(f"❌ DEBUG: Erro importando KryterionHandler: {e}")
                traceback.print_exc()
            
            try:
                from modules.planilhas.handlers.psi_handler import PsiPlanilhaHandler
                print("✅ DEBUG: PsiHandler importado")
            except ImportError as e:
                print(f"❌ DEBUG: Erro importando PsiHandler: {e}")
                traceback.print_exc()
            
            try:
                from modules.planilhas.handlers.scantron_handler import ScantronPlanilhaHandler
                print("✅ DEBUG: ScantronHandler importado")
            except ImportError as e:
                print(f"❌ DEBUG: Erro importando ScantronHandler: {e}")
                traceback.print_exc()
            
            # Mapeamento de handlers
            handlers = {
                'vue': VuePlanilhaHandler,
                'kryterion': KryterionPlanilhaHandler,
                'psi': PsiPlanilhaHandler,
                'scantron': ScantronPlanilhaHandler
            }
            
            print(f"🔧 DEBUG: Handlers mapeados: {list(handlers.keys())}")
            
            handler_class = handlers.get(tipo_planilha.lower())
            if not handler_class:
                print(f"❌ Handler não encontrado para: {tipo_planilha}")
                return None
            
            print(f"🔧 DEBUG: Handler class encontrado: {handler_class}")
            
            # Tenta criar instância e processar
            handler = handler_class()
            print(f"🔧 DEBUG: Handler instanciado: {handler}")
            
            print(f"🔧 DEBUG: Carregando planilha...")
            handler.carregar_planilha(caminho_planilha)
            print(f"🔧 DEBUG: Planilha carregada")
            
            # Valida estrutura
            valido, mensagem = handler.validar_estrutura()
            print(f"🔧 DEBUG: Validação: {valido} - {mensagem}")
            
            if not valido:
                print(f"❌ Estrutura inválida: {mensagem}")
                return None
            
            # Processa dados
            quantidade = handler.get_quantidade_candidatos()
            valor_total = handler.calcular_valor_total()
            
            print(f"🔧 DEBUG: Quantidade: {quantidade}, Valor: {valor_total}")
            
            resultado = {
                "tipo": tipo_planilha.upper(),
                "quantidade": quantidade,
                "valor_total": valor_total,
                "moeda": "US$"
            }
            
            print(f"✅ DEBUG: Resultado final: {resultado}")
            return resultado
            
        except Exception as e:
            print(f"❌ ERRO GERAL no handler {tipo_planilha}: {e}")
            traceback.print_exc()
            return None