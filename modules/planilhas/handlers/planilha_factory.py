# modules/planilhas/handlers/planilha_factory.py
import pandas as pd
import os
import traceback
from core.config import config

class PlanilhaFactory:
    @staticmethod
    def processar_planilha_completa(caminho_planilha, tipo_planilha):
        """
        Processa planilha - VERSÃO CORRIGIDA COM CONFIG
        """
        print(f"🔧 PROCESSANDO {tipo_planilha.upper()} COM HANDLER...")
        print(f"📁 Arquivo: {caminho_planilha}")
        
        try:
            # 👇 IMPORTS CORRIGIDOS
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
            print(f"📊 Coluna de valor: {coluna_valor}")
            
            # Carrega planilha com sheet_name correto
            handler.carregar_planilha(caminho_planilha)
            print("✅ Planilha carregada")
            
            # Valida estrutura
            valido, mensagem = handler.validar_estrutura()
            print(f"🔍 Validação: {mensagem}")
            
            # 👇 CALCULA VALOR USANDO A COLUNA ESPECÍFICA DO CONFIG
            quantidade = handler.get_quantidade_candidatos()
            
            # Calcula valor total da coluna específica
            valor_total = 0.0
            if coluna_valor and handler.df is not None and coluna_valor in handler.df.columns:
                valor_total = handler.df[coluna_valor].sum()
                print(f"💰 3 da coluna '{coluna_valor}': {valor_total:.2f}")
            else:
                # Fallback para método do handler
                valor_total = handler.calcular_valor_total()
                print(f"💰 Valor total (fallback): {valor_total:.2f}")
            
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
            
            # 👇 DADOS ESPECÍFICOS PARA CADA TIPO
            if tipo_planilha.lower() == 'kryterion':
                # Lógica específica do Kryterion com múltiplas abas
                resultado = PlanilhaFactory._processar_kryterion_especial(caminho_planilha, coluna_valor)
                
            elif tipo_planilha.lower() == 'psi':
                # Lógica específica do PSI (SELT vs outros)
                resultado = PlanilhaFactory._processar_psi_especial(handler.df, resultado, coluna_valor)
                
            elif tipo_planilha.lower() == 'vue':
                # Lógica específica do VUE (por cliente)
                resultado = PlanilhaFactory._processar_vue_especial(handler.df, resultado)
            
            print("✅ Handler finalizado com sucesso!")
            return resultado
            
        except Exception as e:
            print(f"❌ ERRO NO HANDLER:")
            print(f"   Tipo: {type(e).__name__}")
            print(f"   Mensagem: {e}")
            traceback.print_exc()
            return None
    
    @staticmethod
    def _processar_vue_especial(df, resultado_base):
        """Lógica específica para VUE - análise por cliente"""
        if df is not None and 'Cliente ' in df.columns:
            clientes_validos = df["Cliente "].dropna().astype(str)
            contagem_clientes = clientes_validos.value_counts()
            
            relatorio_detalhado = []
            for cliente, quantidade in contagem_clientes.items():
                percentual = (quantidade / resultado_base['quantidade']) * 100
                relatorio_detalhado.append({
                    'cliente': cliente,
                    'quantidade': quantidade,
                    'percentual': percentual
                })
            
            resultado_base['relatorio_detalhado'] = relatorio_detalhado
        
        return resultado_base
    
    @staticmethod
    def _processar_psi_especial(df, resultado_base, coluna_valor):
        """Lógica específica para PSI - SELT vs outros"""
        if df is not None and 'Cliente ' in df.columns:
            clientes_validos = df["Cliente "].dropna().astype(str)
            qtd_selt = clientes_validos.str.contains("selt", case=False, na=False).sum()
            qtd_outros = len(clientes_validos) - qtd_selt
            
            resultado_base['qtd_selt'] = int(qtd_selt)
            resultado_base['qtd_outros'] = int(qtd_outros)
        
        return resultado_base
    
    @staticmethod
    def _processar_kryterion_especial(caminho_planilha, coluna_valor):
        """Lógica específica para Kryterion - múltiplas abas"""
        try:
            excel_file = pd.ExcelFile(caminho_planilha)
            abas_alvo = ["Mês 1", "Mês 2", "Mês 3"]
            total_geral = 0
            valor_total_geral = 0.0
            valores_por_aba = {}
            
            for aba in abas_alvo:
                if aba in excel_file.sheet_names:
                    df_aba = pd.read_excel(caminho_planilha, sheet_name=aba, header=1)
                    
                    if coluna_valor and coluna_valor in df_aba.columns:
                        valores_validos = df_aba[coluna_valor].notna().sum()
                        valor_aba = df_aba[coluna_valor].sum()
                        
                        total_geral += valores_validos
                        valor_total_geral += valor_aba
                        
                        valores_por_aba[aba] = {
                            "quantidade": int(valores_validos),
                            "valor_total": float(valor_aba)
                        }
            
            return {
                "tipo": "KRYTERION",
                "quantidade": int(total_geral),
                "valor_total": float(valor_total_geral),
                "valores_por_aba": valores_por_aba,
                "moeda": "US$"
            }
            
        except Exception as e:
            print(f"❌ Erro processamento Kryterion: {e}")
            return None