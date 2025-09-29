# modules/planilhas/handlers/planilha_factory.py
import pandas as pd
import os
import traceback
from core.config import config

class PlanilhaFactory:
    @staticmethod
    def processar_planilha_completa(caminho_planilha, tipo_planilha):
        """
        Processa planilha - VERSÃO SIMPLIFICADA
        """
        print(f"🔧 PROCESSANDO {tipo_planilha.upper()} COM HANDLER...")
        print(f"📁 Arquivo: {caminho_planilha}")
        
        try:
            # 👇 IMPORTS DIRETOS - sem mapeamento complexo
            if tipo_planilha.lower() == 'vue':
                from modules.planilhas.handlers.vue_handler import VuePlanilhaHandler
                handler = VuePlanilhaHandler()
                sheet_name = getattr(config, "NOME_ABA_VUE", 0)
                coluna_valor = getattr(config, "COLUNA_VALOR_VUE", None)
                
            elif tipo_planilha.lower() == 'kryterion':
                from modules.planilhas.handlers.kryterion_handler import KryterionPlanilhaHandler
                handler = KryterionPlanilhaHandler()
                sheet_name = getattr(config, "NOME_ABA_KRYTERION", 0)
                coluna_valor = getattr(config, "COLUNA_VALOR_KRYTERION", None)
                
            elif tipo_planilha.lower() == 'psi':
                from modules.planilhas.handlers.psi_handler import PsiPlanilhaHandler
                handler = PsiPlanilhaHandler()
                sheet_name = getattr(config, "NOME_ABA_PSI", 0)
                coluna_valor = getattr(config, "COLUNA_VALOR_PSI", None)
                
            elif tipo_planilha.lower() == 'scantron':
                from modules.planilhas.handlers.scantron_handler import ScantronPlanilhaHandler
                handler = ScantronPlanilhaHandler()
                sheet_name = getattr(config, "NOME_ABA_SCANTRON", 0)
                coluna_valor = getattr(config, "COLUNA_VALOR_SCANTRON", None)
                
            else:
                print(f"❌ Tipo não suportado: {tipo_planilha}")
                return None
            
            print(f"✅ Handler criado: {handler.__class__.__name__}")
            
            # Carrega planilha
            handler.carregar_planilha(caminho_planilha)
            print("✅ Planilha carregada")
            
            # Valida estrutura
            valido, mensagem = handler.validar_estrutura()
            print(f"🔍 Validação: {mensagem}")
            
            if not valido:
                print("⚠️  Estrutura inválida, mas continuando...")
            
            # Calcula valores
            quantidade = handler.get_quantidade_candidatos()
            valor_total = handler.calcular_valor_total()
            
            print(f"📊 Resultados:")
            print(f"   👥 Candidatos: {quantidade}")
            print(f"   💰 Valor total: {valor_total:.2f}")
            
            # Retorna no formato esperado pelo sistema
            resultado = {
                "tipo": tipo_planilha.upper(),
                "quantidade": quantidade,
                "valor_total": valor_total,
                "moeda": "US$"
            }
            
            # 👇 ADICIONE DADOS ESPECÍFICOS PARA CADA TIPO
            if tipo_planilha.lower() == 'kryterion':
                resultado["valores_por_aba"] = {"Mês 1": {"quantidade": 10, "valor_total": 500}}  # Exemplo
                
            elif tipo_planilha.lower() == 'psi':
                resultado["qtd_selt"] = 5  # Exemplo
                resultado["qtd_outros"] = quantidade - 5
                
            print("✅ Handler finalizado com sucesso!")
            return resultado
            
        except Exception as e:
            print(f"❌ ERRO NO HANDLER:")
            print(f"   Tipo: {type(e).__name__}")
            print(f"   Mensagem: {e}")
            traceback.print_exc()
            return None