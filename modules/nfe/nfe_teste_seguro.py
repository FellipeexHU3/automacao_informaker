def teste_super_seguro_com_cores():
    """Teste que mantém cores e formatação"""
    from .nfe_core import NFE
    from .nfe_selecao import get_caminho_planilha
    from .nfe_bkp import criar_backup_com_formato, atualizar_apenas_celulas
    import os
    print("🎨 TESTE SUPER SEGURO COM FORMATAÇÃO")
    print("=" * 50)
    
    caminho_original = get_caminho_planilha()
    caminho_backup = criar_backup_com_formato(caminho_original)
    
    # Carregar planilha de backup
    nfe = NFE(caminho_planilha=caminho_backup)
    
    print(f"📊 Trabalhando em: {os.path.basename(caminho_backup)}")
    print(f"🎨 Cores e formatação preservadas!")
    print(f"🔒 Original protegida: {os.path.basename(caminho_original)}")
    
    if not nfe.notas_pendentes:
        print("❌ Nenhuma nota pendente")
        return False
    
    # Mostrar opções
    print("\n📋 NOTAS PENDENTES (com cores originais):")
    for i, nota in enumerate(nfe.notas_pendentes[:5]):
        status = "🟡 AMARELO" if nota['dados'].get('NFSe') is None else "⚪ CINZA"
        print(f"   {i+1}. Linha {nota['indice_planilha']}: {nota['dados'].get('Nome', 'N/A')} - {status}")
    
    try:
        opcao = int(input("\n🔢 Digite o número da nota: ")) - 1
        if 0 <= opcao < len(nfe.notas_pendentes):
            nota = nfe.notas_pendentes[opcao]
            return processar_com_cores(nfe, nota, caminho_original)
        else:
            print("❌ Opção inválida")
            return False
    except ValueError:
        print("❌ Digite um número válido")
        return False

def processar_com_cores(nfe, nota, caminho_original):
    """Processa mantendo as cores do supervisor"""
    linha = nota['indice_planilha']
    
    print(f"\n🎯 PROCESSANDO LINHA {linha}")
    print("=" * 40)
    print(f"   Cliente: {nota['dados'].get('Nome', 'N/A')}")
    print(f"   🎨 Esta linha ficará AMARELA após processamento")
    print(f"   📁 Backup: {os.path.basename(nfe.caminho_planilha)}")
    
    nfse = input("\n📝 NFSe: ").strip()
    auth = input("📝 Autenticidade: ").strip()
    
    if not nfse or not auth:
        print("❌ Dados inválidos")
        return False
    
    # Gravar na planilha de backup
    sucesso = nfe.marcar_como_processada(nota['indice_array'], nfse, auth)
    
    if sucesso:
        # 🔥 SALVAR MANTENDO FORMATAÇÃO
        if atualizar_apenas_celulas(nfe, nfe.caminho_planilha):
            print("💾 Salvo com SUCESSO! Formatação preservada!")
            print("🎨 A linha agora está AMARELA no backup")
            print("🔒 Original permanece CINZA e intacta!")
            
            # Oferecer para abrir
            abrir = input("📂 Abrir backup para ver cores? (s/n): ").lower()
            if abrir == 's':
                os.startfile(nfe.caminho_planilha)
            
            return True
    else:
        print("❌ Erro ao gravar")
    
    return False