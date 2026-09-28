📊 Avaliador Inteligente de Testes A/B e Finanças (Gemini IA)Projeto desenvolvido como solução para o Lab "Construa Seu Assistente Virtual Com Inteligência Artificial" da Digital Innovation One (DIO). Trata-se de um agente autônomo focado em análise financeira e tomadas de decisão estratégica sobre testes A/B, processando dados em formato CSV, automatizando métricas de negócio e gerando relatórios executivos estruturados.🎯 Sobre o Projeto & ObjetivoA tomada de decisão baseada em testes A/B exige rapidez e precisão matemática. O Avaliador Inteligente atua como um Analista de Dados e Growth Sênior, automatizando o processamento de planilhas financeiras brutas, eliminando ruídos e respondendo à pergunta central:"Dado este teste, qual é a variante ou opção mais promissora para o negócio?"O assistente analisa volumes de vendas (GMV), comissões, custos de cashback, ticket médio e margem de lucro líquido para sugerir a melhor decisão estratégica.📁 Estrutura do RepositórioPlaintextassistente-virtual-ia/
├── data/                 # Arquivos CSV de entrada e dados para testes
├── docs/                 # Documentação do projeto e relatórios gerados
├── prompts/              # System Prompts e instruções da IA
│   └── prompt.py
|   └── chatbot.py
├── src/                  # Código-fonte da aplicação
│   ├── config.py         # Carregamento de variáveis de ambiente
│   ├── data_processor.py # Limpeza, flexibilização e agregação de CSVs
│   ├── ia_agent.py       # Integração com o Google GenAI SDK
│   └── sheets_integrador.py # Exportação e sincronização no Google Sheets
├── app.py                # Interface gráfica com Streamlit
├── Iniciar_dashboard via terminal.bat # Forma de iniciar via terminal
├── Iniciar_Dashboard via navegador.bat # Forma de iniciar via navegador
├── credentials.json.example # Exemplo de como criar um bot para inserir os resultados em uma planilha.
├── main.py               # Execução em linha de comando (Terminal)
├── .env.example          # Modelo para chaves de API
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação principal
🚀 Os 6 Passos do Projeto1. Documentação do AgentePersona: Analista de Dados e Growth Sênior atuando na área financeira.Tom de Voz: Executivo, direto, analítico e embasado em dados matemáticos.Comportamento: Processa e limpa dados financeiros, calcula margens reais, descarta alucinações e emite recomendações claras de negócio com análise de risco.2. Base de ConhecimentoO assistente consome arquivos CSV dinâmicos com schema financeiro resiliente:Campos Principais: Grupos de usuários (variante), compradores, comissão (R$), cashback (R$), vendas totais (GMV).Campos Secundários/Flexíveis: tipo, categoria, descricao, resumo.Mecanismo de Resiliência: O pré-processador (data_processor.py) limpa cifragens (R$, vírgulas, pontos) e tolera colunas faltantes ou inéditas de forma automatizada.3. Prompts do AgenteA inteligência do modelo é orientada pelo SYSTEM_PROMPT (localizado em prompts/prompt.py), estruturado para instruir a IA a calcular o Ticket Médio e o Lucro Líquido, retornando obrigatoriamente duas saídas distintas:[Primeira SAÍDA : RELATÓRIO EXECUTIVO]: Relatório Markdown completo contendo resumo, tabela comparativa, justificativa matemática, recomendações e análise de risco/oportunidade.[Segunda SAÍDA : DADOS PARA PLANILHA]: Uma única linha delimitada por pipes (|), pronta para automações e exportações no formato:Nome da Variante | Descrição resumida | Resumo da métrica vencedora | Variante mais promissora4. Aplicação FuncionalO assistente pode ser executado em duas interfaces:Interface Web (Streamlit): Painel visual com suporte a seleção individual de arquivos, lote ou upload manual de CSVs, gráficos interativos, relatórios sanfonados e sincronização com Google Sheets.Terminal CLI: Modo simplificado para execução rápida via linha de comando.5. Avaliação e MétricasO agente valida os dados calculando e comparando:Lucro Líquido Real: $\text{Comissão Total} - \text{Cashback Total}$Ticket Médio: $\frac{\text{Vendas Totais (GMV)}}{\text{Número de Compradores}}$Eficiência do Teste: Identificação do grupo com maior receita líquida mantendo volume saudável de usuários e GMV.6. Pitch & Valor de NegócioRedução do tempo de análise de testes A/B financeiros de horas para menos de 40 segundos, automatizando a padronização e o registro direto dos dados analisados em planilhas executivas do Google Sheets.🛠️ Tecnologias UtilizadasLinguagem: Python 3.10+LLM Engine: Google Gemini API (google-genai SDK)Interface: StreamlitAnálise de Dados: PandasIntegração: Google Sheets API (gspread / OAuth)⚙️ Como Executar o ProjetoPré-requisitosPython 3.10 ou superior instalado.Chave de API do Google Gemini (Obtenha sua chave aqui).1. Clonar o Repositório e Criar o AmbienteBashgit clone https://github.com/seu-usuario/assistente-virtual-ia.git
cd assistente-virtual-ia

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source .venv/bin/activate
2. Instalar DependênciasBashpip install -r requirements.txt
3. Configurar Variáveis de AmbienteCrie um arquivo .env na raiz do projeto com o seguinte conteúdo:Snippet de códigoGEMINI_API_KEY=SuaChaveApiAqui
GOOGLE_SHEET_ID=SeuIDDaPlanilhaAqui (Opcional)
4. Executar a AplicaçãoModo Web (Streamlit):Bashpython -m streamlit run app.py
Modo Terminal:Bashpython main.py
👨‍💻 AutorDesenvolvido por Ryan Kaique como parte do ecossistema de aprendizado da Digital Innovation One (DIO).
