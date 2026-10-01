##################################################################################################################################################################
📌 **VISÃO GERAL**
O projeto foi projetado para contornar as limitações e bloqueios da API legada da Hotmart, conectando-se diretamente ao novo Course Consumption Gateway 
e ao player de distribuição HLS (vod-akm / cf-embed).
Além de realizar o mapeamento completo de módulos, aulas, descrições e anexos, o script implementa uma rotina de download resiliente no estilo Torrent 
(com arquivos temporários de staging .part e retomada automática) e um pipeline de compactação visualmente sem perdas via FFmpeg com monitoramento de 
progresso em tempo real.
##################################################################################################################################################################


##################################################################################################################################################################
🚀 **FUNCIONALIDADES**
**Compatibilidade Moderna (Gateway 2026)** 
* Comunicação direta com os endpoints api-club-course-consumption-gateway-ga e suporte a fluxos assinados Akamai/CloudFront (vod-akm.play.hotmart.com).

**Retomada Inteligente (Estilo Torrent):**
* Download utilizando arquivos de transição (.part.mp4 / .part).
* Verificação prévia de integridade: arquivos já concluídos e íntegros são pulados instantaneamente em milissegundos sem gastar requisições.
* Elimina riscos de arquivos corrompidos ou pela metade em quedas de energia/internet.

**Compactação Otimizada sem Perda Perceptível:**
* Aplicação de CRF 22 via codec libx264 (redução média de 40% a 60% do tamanho do arquivo).
* Preservação bit a bit do áudio original (-c:a copy) sem recodificação desnecessária.

**Barra de Progresso e Contagem Regressiva:**
* Exibição dinâmica em tempo real no terminal: porcentagem (0%... 100%), barra gráfica, tempo decorrido, contagem regressiva restante, volume de dados 
transferidos e velocidade.

**Suporte Amplo a Recursos da Aula:**
* Vídeos nativos (Hotmart Player / HLS master playlist).
* Vídeos externos embutidos (Vimeo e YouTube).
* Materiais complementares e anexos nativos (.pdf, .mp3, .gpx, .zip, etc.).
* Documentos do Google Drive incorporados em iframes (com bypass de alerta de verificação de vírus).
* Exportação do conteúdo textual/descrição da aula em descricao.html.
* Exportação de links úteis em links.txt.

**Compatibilidade Cross-Drive no Windows:**
* Gerenciamento seguro de I/O entre discos físicos/virtuais distintos (ex.: C:\ para Google Drive G:\).

**Autodetecção do FFmpeg:**
* Localiza o binário do FFmpeg automaticamente no PATH do sistema, via pacote Python imageio-ffmpeg, em pastas do Playwright ou na raiz do projeto.

**Renovação Interativa de Sessão:**
* Pausa e solicita atualização do Bearer Token caso a sessão expire durante execuções prolongadas sem abortar o processo.
##################################################################################################################################################################


##################################################################################################################################################################
🛠️ **PRÉ-REQUISITOS**
Python: Versão 3.10 ou superior.
FFmpeg: Instalado no sistema ou via pacote Python integrado.
Navegador Moderno: (Chrome, Edge, Brave, etc.) para capturar o token de autenticação.
##################################################################################################################################################################


##################################################################################################################################################################
📦 **INSTALAÇÃO**
**Clone o repositório:** 
git clone https://github.com/alexandrefortunati/downloader_hotmart.git

**Crie e ative um ambiente virtual:**
python -m venv .venv
.\.venv\Scripts\Activate.ps1

**Instale as dependências:**
pip install -r requirements.txt
##################################################################################################################################################################


##################################################################################################################################################################
⚙️ **CONFIGURAÇÕES**
Abra o arquivo principal (hotmark.py) e ajuste os parâmetros de execução no bloco inicial:

# Diretório de destino onde a estrutura será organizada
DIRETORIO_DESTINO = r"G:\Meu Drive\Fulano\Nome_Curso"

# Parâmetros de Compactação
COMPACTAR_VIDEO = True         # Ativa/desativa compressão via FFmpeg
CODEC_VIDEO = "libx264"        # "libx264" para compatibilidade ampla
CRF_QUALIDADE = 22             # 20-23: visualmente idêntico ao original
PRESET_VELOCIDADE = "faster"   # Balanço ideal entre tempo e compressão

# Identificadores do Produto
SLUG_CURSO = "descrição_curso"     

# Localização do curso
# Exemplo de URL: 
# https://hotmart.com/pt-BR/club/juniorrpado/products/180527/content/E4zW2ZL6el?track=g97BvkP7pG
# A descrição do curso fica entre /club e /products. Portanto, neste exemplo é juniorprado

PRODUCT_ID = "180527"

# Localização do ID do curso
# Usando o exemplo acima, o ID do curso fica após /products. Portanto, neste exemplo é 180527
##################################################################################################################################################################


##################################################################################################################################################################
🔑 **OBTENÇÃO DO TOKEN DE ACESSO**
Como a Hotmart implementa proteção contra bots em telas de login automatizado, o token deve ser obtido a partir de uma sessão ativa no seu navegador:

* Acesse o curso no seu navegador.
* Pressione F12 para abrir as Ferramentas do Desenvolvedor e selecione a aba Rede (Network).
* No campo de filtro, digite navigation e pressione F5 para atualizar a página.
* Clique com o botão direito na requisição navigation > Copiar (Copy) > Copiar como cURL (Copy as cURL).
* Copie o valor do cabeçalho authorization: Bearer e cole na constante TOKEN_INICIAL do script ou no prompt interativo do terminal.
##################################################################################################################################################################

##################################################################################################################################################################
💻 **EXECUÇÃO**
Com o ambiente virtual ativado, inicie o utilitário:

python hotmark.py

Obs.: O script realizará o mapeamento da grade e processará cada aula sequencialmente. Caso o download seja interrompido a qualquer momento (Ctrl + C ou queda de conexão), 
basta executar o comando novamente: os itens concluídos serão validados e pulados de forma imediata.
##################################################################################################################################################################

##################################################################################################################################################################
📂 **ESTRUTURA DE DIRETÓRIOS**
O curso é estruturado de forma hierárquica e padronizada, exemplo:

G:\Meu Drive\Fulano\Nome_Curso\
│
├── 01_modulo-iniciante\
│   ├── 01.apresentacao-do-modulo\
│   │   ├── aula-1.mp4
│   │   ├── descricao.html
│   │   └── Materiais\
│   │       ├── apostila-modulo-1.pdf
│   │       ├── exercicio.gp
│   │       └── links.txt
│   └── 02.exercicios-praticos\
│       ├── aula-1.mp4
│       └── descricao.html
│
└── log.txt
##################################################################################################################################################################

##################################################################################################################################################################
⚠️ Aviso Legal (Disclaimer)
Este projeto foi desenvolvido com finalidade estritamente educacional e de arquivamento pessoal para estudantes que já possuem acesso legítimo aos conteúdos 
adquiridos na plataforma Hotmart. O autor deste script não incentiva nem compactua com a pirataria ou distribuição não autorizada de materiais protegidos por 
direitos autorais. Certifique-se de respeitar os Termos de Serviço da plataforma.
##################################################################################################################################################################
