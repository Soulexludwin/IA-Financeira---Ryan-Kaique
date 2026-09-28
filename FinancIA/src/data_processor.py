import pandas as pd
import logging
import re

logging.basicConfig(level=logging.INFO)

def limpar_cifras(valor_str):
    """
    Remove símbolos de moeda e converte para float.
    """
    if pd.isna(valor_str):
        return 0.0
    
    if isinstance(valor_str, (int, float)):
        return float(valor_str)
        
    valor_limpo = str(valor_str).replace('R$', '').replace(' ', '')
    valor_limpo = valor_limpo.replace('.', '') 
    valor_limpo = valor_limpo.replace(',', '.') 
    
    try:
        return float(valor_limpo)
    except ValueError:
        return 0.0

def _normalizar_nome_coluna(nome):
    """Auxiliar para comparar nomes de colunas ignorando maiúsculas e espaços extras."""
    return re.sub(r'\s+', ' ', str(nome).strip().lower())

def processar_csv(caminho_arquivo):
    """
    Processa o arquivo CSV de forma flexível, tratando colunas ausentes, 
    colunas novas e variações no nome da coluna de grupo.
    """
    logging.info(f"Lendo dados do arquivo: {caminho_arquivo}")
    
    try:
        df = pd.read_csv(caminho_arquivo)
        
        if df.empty:
            logging.warning("O arquivo CSV está vazio.")
            return "O arquivo enviado está vazio."

        # Mapeamento de colunas existentes
        colunas_originais = list(df.columns)
        mapa_colunas = {_normalizar_nome_coluna(c): c for c in colunas_originais}

        # 1. Identificar a coluna de Agrupamento/Variante
        col_grupo = None
        possiveis_nomes_grupo = ['grupos de usuarios', 'grupo de usuarios', 'grupo', 'variante', 'variant', 'group']
        
        for nome_pos in possiveis_nomes_grupo:
            if nome_pos in mapa_colunas:
                col_grupo = mapa_colunas[nome_pos]
                break

        if not col_grupo:
            # Caso não encontre por nome, usa a primeira coluna como grupo
            col_grupo = colunas_originais[0]
            logging.warning(f"Coluna de grupo não identificada. Utilizando '{col_grupo}' como grupo.")

        # 2. Mapear e garantir presença das colunas padrão esperadas
        colunas_padrao = {
            'compradores': ('sum', 0),
            'comissão': ('sum', 0.0),
            'cashback': ('sum', 0.0),
            'vendas totais': ('sum', 0.0),
            'parceiro': ('first', 'Não informado')
        }

        # Dicionário de agregações para o groupby
        agg_rules = {}

        for nome_padrao, (operacao, valor_padrao) in colunas_padrao.items():
            if nome_padrao in mapa_colunas:
                col_real = mapa_colunas[nome_padrao]
            else:
                # Se a coluna estiver faltando, cria com valor padrão
                col_real = nome_padrao.title() if nome_padrao != 'vendas totais' else 'Vendas Totais'
                df[col_real] = valor_padrao
                logging.warning(f"A coluna '{nome_padrao}' não foi encontrada. Foi criada automaticamente com valor padrão.")
            
            agg_rules[col_real] = operacao

        # 3. Tratar colunas NOVAS/EXTRAS que vieram no CSV
        for col_orig in colunas_originais:
            if col_orig == col_grupo or col_orig in agg_rules:
                continue
            
            # Se a coluna nova for numérica, faz a soma; senão, pega o primeiro valor
            if pd.api.types.is_numeric_dtype(df[col_orig]):
                agg_rules[col_orig] = 'sum'
            else:
                # Tenta converter para número se for texto numérico/moeda
                amostra = df[col_orig].dropna().astype(str).head(10)
                eh_moeda_ou_num = amostra.str.contains(r'R\$|\d+,\d+|\d+\.\d+', regex=True).any()
                if eh_moeda_ou_num:
                    agg_rules[col_orig] = 'sum'
                else:
                    agg_rules[col_orig] = 'first'
            
            logging.info(f"Nova coluna detectada '{col_orig}'. Regra de agregação: {agg_rules[col_orig]}")

        # 4. Limpeza de valores monetários/numéricos em colunas numéricas
        for col, regra in agg_rules.items():
            if regra == 'sum' and col in df.columns:
                df[col] = df[col].apply(limpar_cifras)

        # 5. Agregação dos dados pelo Grupo
        df_agrupado = df.groupby(col_grupo).agg(agg_rules).reset_index()

        logging.info("Dados limpos e agregados com sucesso.")
        
        resumo_texto = df_agrupado.to_markdown(index=False)
        return resumo_texto
    
    except Exception as e:
        logging.error(f"Erro ao processar o CSV: {e}")
        raise e