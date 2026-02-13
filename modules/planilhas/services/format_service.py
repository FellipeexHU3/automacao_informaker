class FormatService:
    """Serviço compartilhado para formatação"""
    
    @staticmethod
    def formatar_moeda_br(valor):
        """Formata valor como moeda brasileira"""
        if valor == 'N/A' or valor is None:
            return 'R$ N/A'
        try:
            if isinstance(valor, str):
                valor = float(valor.replace(',', '.'))
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return f"R$ {valor}"
    
    @staticmethod
    def formatar_data_br(data):
        """Formata data para padrão BR"""
        if hasattr(data, 'strftime'):
            return data.strftime('%d/%m/%Y')
        return str(data).split()[0] if ' ' in str(data) else str(data)