# Hub de Impressão de Etiquetas (Integração RESULTH) 🏷️💲

Um sistema web leve, rápido e responsivo desenvolvido em Python (Flask) para a geração, gerenciamento de fila e impressão de etiquetas térmicas. O projeto conta com layouts otimizados para impressoras térmicas (como Zebra, Argox, Elgin) e atende fluxos de automação comercial e controle de estoque.

## 🎯 Contextualização e Integração

Este projeto foi originalmente construído para operar de forma totalmente integrada ao sistema **RESULTH - ATS INFORMATICA**. Ele consome as informações do banco de dados local do sistema para alimentar os dados dos produtos em tempo real na interface web.

> **💡 Adaptabilidade para outros ERPs:** Embora esteja configurado para o RESULTH, o sistema é altamente modular. Para utilizá-lo com qualquer outro ERP de banco de dados local (Firebird, MariaDB, PostgreSQL, SQL Server), basta alterar a DLL/driver de conexão no arquivo de rotas (Back-end) e ajustar a instrução SQL (`SELECT`) conforme a estrutura das tabelas do novo sistema.

## 🚀 Funcionalidades Principais

* **Busca Ágil e Otimizada:** Consulta produtos pelo nome, código interno ou código de barras.
* **Integração com Leitor Óptico:** Sistema preparado para receber "bips" de leitores de código de barras. Ao bipar a referência exata, o sistema automatiza a seleção e foca no campo numérico para ganho de agilidade.
* **Navegação por Teclado:** Controle completo da interface (Busca, Setas Direcionais, Enter, Qtd e Cópias) sem a necessidade de uso do mouse.
* **Fila de Impressão (Spooler Web):** Permite adicionar múltiplos itens distintos, definir quantidades fracionadas e número de cópias físicas antes de enviar o pacote único para a impressora.
* **Dois Modelos de Etiquetas Embutidos:**
    1.  **Etiqueta Padrão (59x40mm):** Focada em controle de retalhos/fracionados. Gera código de barras dinâmico (JsBarcode) cruzando a quantidade digitada com o código do produto.
    2.  **Etiqueta de Gôndola (75x40mm):** Focada na exposição em prateleiras. Layout limpo com preço em grande destaque, código de barras e margens de segurança rigorosas para o corte/picote do papel térmico.

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python, Flask.
* **Front-end:** HTML5, CSS Flexbox, JavaScript puro (Vanilla).
* **Estilização e Ícones:** Bootstrap 5 e Bootstrap Icons.
* **Geração de Código de Barras:** JsBarcode.

## ⚙️ Instalação e Execução

1. Clone o repositório: `git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git`
2. Instale as dependências do Python: `pip install flask fdb` *(ajuste o conector de banco conforme sua necessidade)*.
3. Execute a aplicação: `python app.py`
4. Acesse no navegador local: `http://localhost:5000`