# modules/nfe/nfe_teste_controlado.py
def teste_com_dados_controlados():
    """Teste específico para dados controlados que você vai criar"""
    from .nfe_core import NFE
    from .nfe_selecao import get_tipo_planilha
    
    print("🎯 TESTE COM DADOS CONTROLADOS")
    print("=" * 50)
    
    # Carregar planilha
    nfe = NFE()
    print(f"📊 Planilha {nfe.tipo_planilha} carregada")
    print(f"   Total de notas: {len(nfe.notas)}")
    print(f"   Pendentes: {len(nfe.notas_pendentes)}")
    
    # Mostrar todas as notas pendentes para você escolher
    print("\n📋 NOTAS PENDENTES DISPONÍVEIS:")
    for i, nota in enumerate(nfe.notas_pendentes):
        print(f"   {i+1}. Linha {nota['indice_planilha']}: {nota['dados'].get('Nome', 'N/A')} - R$ {nota['dados'].get('Valor', 'N/A')}")
    
    # Você escolhe qual linha testar
    try:
        opcao = int(input("\n🔢 Digite o número da nota para testar: ")) - 1
        if 0 <= opcao < len(nfe.notas_pendentes):
            nota_escolhida = nfe.notas_pendentes[opcao]
            return processar_nota_manual(nfe, nota_escolhida)
        else:
            print("❌ Opção inválida")
            return False
    except ValueError:
        print("❌ Digite um número válido")
        return False

def processar_nota_manual(nfe, nota):
    """Processa uma nota manualmente (para teste)"""
    from .nfe_core import NFE
    linha = nota['indice_planilha']
    dados = nota['dados']
    
    print(f"\n🎯 PROCESSANDO LINHA {linha}")
    print("=" * 30)
    print(f"📋 DADOS DA NOTA:")
    print(f"   Nome: {dados.get('Nome', 'N/A')}")
    print(f"   CPF: {dados.get('CPF', 'N/A')}")
    print(f"   Valor: R$ {dados.get('Valor', 'N/A')}")
    print(f"   Data: {dados.get('data_emissao', 'N/A')}")
    print(f"   Email: {dados.get('E-mail', 'N/A')}")
    
    # Pedir os dados que seriam capturados da automação
    print("\n📝 DIGITE OS DADOS DA NOTA GERADA:")
    nfse = input("Número da NFSe: ").strip()
    autenticidade = input("Código de Autenticidade: ").strip()
    
    if not nfse or not autenticidade:
        print("❌ Dados inválidos")
        return False
    
    # Confirmar
    print(f"\n✅ CONFIRMAÇÃO:")
    print(f"   NFSe: {nfse}")
    print(f"   Autenticidade: {autenticidade}")
    confirmar = input("Confirmar gravação? (s/n): ").lower().strip()
    
    if confirmar == 's':
        # Gravar na planilha
        sucesso = nfe.marcar_como_processada(nota['indice_array'], nfse, autenticidade)
        
        if sucesso:
            print("💾 Gravando na planilha...")
            if nfe.exportar_planilha_atualizada():
                print("✅ Dados gravados com sucesso!")
                
                # Verificar se realmente foi salvo
                print("\n🔍 VERIFICANDO GRAVAÇÃO:")
                nfe_verificacao = NFE(caminho_planilha=nfe.caminho_planilha)
                nota_verificada = nfe_verificacao.obter_nota_por_indice(nota['indice_array'])
                
                if nota_verificada:
                    nfse_salvo = nota_verificada.get('NFSe', 'N/A')
                    auth_salvo = nota_verificada.get('Autenticidade', 'N/A')
                    print(f"   NFSe salvo: {nfse_salvo}")
                    print(f"   Auth salvo: {auth_salvo}")
                    
                    if nfse_salvo == nfse and auth_salvo == autenticidade:
                        print("🎉 TESTE BEM-SUCEDIDO! Sistema funcionando perfeitamente!")
                        return True
                    else:
                        print("❌ Diferente do esperado - verifique a planilha manualmente")
                return True
            else:
                print("❌ Erro ao salvar planilha")
        else:
            print("❌ Erro ao gravar dados")
    else:
        print("❌ Gravação cancelada")
    
    return False