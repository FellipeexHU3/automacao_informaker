from .ponto_core import PontoAutomacao
from .config import COORDENADAS_PADRAO, TIPOS_PONTO, NOMES_PONTO, SEGUNDOS_ANTECEDENCIA
from modules.login.modulo_login import fazer_login 
import time
from datetime import datetime, timedelta

def automacao_ponto():
    print("🤖 AUTOMAÇÃO DE PONTO")
    print("=" * 50)

    # Escolher tipo de ponto
    print("\nEscolha o tipo de ponto:")
    print("1 - Entrada")
    print("2 - Almoço")
    print("3 - Volta do Almoço")
    print("4 - Saída")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao not in TIPOS_PONTO:
        print("❌ Opção inválida")
        return
    
    tipo_ponto = TIPOS_PONTO[opcao]
    
    # Opção de horário personalizado
    print(f"\n⏰ Horário para {NOMES_PONTO[tipo_ponto]}:")
    print("1 - Agora (imediatamente)")
    print("2 - Horário específico")
    
    opcao_horario = input("Digite sua opção: ")
    
    horario_alvo = None
    tempo_espera = 0
    
    if opcao_horario == "2":
        horario_input = input("Digite o horário (HH:MM): ")
        try:
            # Converter para objeto datetime
            hoje = datetime.now().date()
            horario_alvo = datetime.strptime(horario_input, "%H:%M").replace(
                year=hoje.year, month=hoje.month, day=hoje.day
            )
            
            # Calcular tempo de espera (7 segundos antes)
            agora = datetime.now()
            tempo_espera = (horario_alvo - timedelta(seconds=SEGUNDOS_ANTECEDENCIA)) - agora
            
            if tempo_espera.total_seconds() > 0:
                print(f"⏰ Ponto agendado para: {horario_alvo.strftime('%H:%M:%S')}")
                print(f"⏳ Executando em {tempo_espera.total_seconds():.0f} segundos...")
            else:
                print("⚠️ Horário já passou, executando agora...")
                tempo_espera = 0
                
        except ValueError:
            print("❌ Formato de horário inválido! Use HH:MM")
            return
    
    # Se for execução imediata ou horário já passou
    if opcao_horario == "1" or tempo_espera.total_seconds() <= 0:
        # Fazer login imediatamente
        driver = fazer_login()
        if not driver:
            print("❌ Falha no login")
            return
        
        try:
            # Inicializar sistema de ponto
            ponto = PontoAutomacao(COORDENADAS_PADRAO)
            
            # Bater ponto imediatamente
            sucesso = ponto.bater_ponto(tipo_ponto)
            
            if sucesso:
                print(f"✅ {NOMES_PONTO[tipo_ponto]} registrado com sucesso!")
            else:
                print("❌ Falha ao registrar ponto")
                
        finally:
            input("Pressione Enter para fechar...")
            driver.quit()
            print("🎉 Processo finalizado")
    
    else:
        # Modo agendado - esperar primeiro, depois fazer login
        print(f"\n⏳ Aguardando {tempo_espera.total_seconds():.0f} segundos...")
        print("💡 O login será feito automaticamente pouco antes do horário")
        print("⚠️ Mantenha o computador ligado e não feche este programa")
        
        # Contador regressivo
        segundos_totais = int(tempo_espera.total_seconds())
        for i in range(segundos_totais, 0, -1):
            if i % 60 == 0 or i <= 10:  # Mostrar a cada minuto ou últimos 10 segundos
                minutos = i // 60
                segundos = i % 60
                print(f"⏰ Faltam {minutos:02d}:{segundos:02d}...")
            time.sleep(1)
        
        print("🚀 Hora de bater o ponto! Fazendo login...")
        
        # AGORA fazer o login
        driver = fazer_login()
        if not driver:
            print("❌ Falha no login")
            return
        
        try:
            # Inicializar sistema de ponto
            ponto = PontoAutomacao(COORDENADAS_PADRAO)
            
            # Bater ponto
            sucesso = ponto.bater_ponto(tipo_ponto)
            
            if sucesso:
                print(f"✅ {NOMES_PONTO[tipo_ponto]} registrado com sucesso!")
            else:
                print("❌ Falha ao registrar ponto")
                
        finally:
            input("Pressione Enter para fechar...")
            driver.quit()
            print("🎉 Processo finalizado")

def menu_principal():
    print("\n" + "=" * 50)
    print("🤖 SISTEMA DE AUTOMAÇÃO - MENU PRINCIPAL")
    print("=" * 50)
    
    print("1 - Executar automação de ponto")
    print("2 - Testar coordenadas")
    print("3 - Só fazer login")
    print("4 - Sair")
    
    opcao = input("\nDigite sua opção: ")
    
    if opcao == "1":
        automacao_ponto()
    elif opcao == "2":
        testar_coordenadas()
    elif opcao == "3":
        driver = fazer_login()
        if driver:
            input("Pressione Enter para fechar...")
            driver.quit()
    elif opcao == "4":
        print("👋 Até mais!")
        return False
    else:
        print("❌ Opção inválida")
    
    return True

def testar_coordenadas():
    """Testa as coordenadas configuradas"""
    ponto = PontoAutomacao(COORDENADAS_PADRAO)
    ponto.testar_coordenadas()
    input("Pressione Enter para continuar...")