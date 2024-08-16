# SAE - Sistematização da Assistência de Enfermagem

## Descrição

O projeto SAE (Sistematização da Assistência de Enfermagem) foi desenvolvido como uma resposta a um desafio proposto pela Secretaria de Saúde da Prefeitura de São José dos Campos, voltado para as unidades de Pronto Atendimento 24 Horas. O sistema visa digitalizar o processo de anotações manuais, exigido pelo Conselho Federal de Enfermagem (COFEN), que é atualmente realizado em cinco fichas distintas.

O aplicativo foi desenvolvido como um protótipo na linguagem Python, utilizando o framework PyQt6 para a interface gráfica e SQLite para o banco de dados. Ele permite a entrada, visualização, impressão e armazenamento de dados de pacientes de forma digital, facilitando o processo de assistência de enfermagem.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

projeto/
├── database.py # Gerenciamento do banco de dados SQLite
├── dist.py # Script para gerar o executável do projeto
├── gui.py # Interface gráfica do usuário utilizando PyQt6
├── importer.py # Importação de dados para o sistema
├── main.py # Arquivo principal que inicializa o aplicativo
├── print.py # Função para imprimir dados em PDF ou enviar para uma impressora
├── update.py # Atualização dos dados do sistema
├── _pages/ # Páginas HTML que compõem a interface do sistema
│ ├── form1.html
│ ├── form2.html
│ ├── form3.html
├── _css/ # Estilos CSS para a interface do sistema
│ ├── button_styles.css
│ ├── styles_form1.css
│ ├── styles_form2.css
│ ├── styles_form3.css
│ ├── styles_form1_print.css
│ ├── styles_form2_print.css
├── _image/ # Imagens utilizadas no projeto
│ └── logo.png
├── _scripts/ # Scripts JavaScript para a interatividade das páginas HTML
│ ├── scripts_form1.js
│ ├── scripts_form2.js
│ ├── scripts_form3.js
├── _models_print/ # Modelos para impressão dos formulários
│ ├── form1_print.js
│ ├── form2_print.js
├── _dist/ # Diretório para o executável e outros arquivos necessários
│ ├── main.exe
│ ├── _css
│ ├── _image
│ ├── _models_print
│ ├── _pages
│ ├── _scripts
├── build # Arquivos gerados durante o build
├── anotacoes # Anotações e outros arquivos auxiliares
├── pycache # Arquivos compilados do Python


## Funcionalidades

- **Cadastro de Pacientes**: Interface para entrada de dados dos pacientes.
- **Exame Físico**: Registro detalhado do exame físico do paciente.
- **Diagnóstico de Enfermagem**: Registro e acompanhamento do diagnóstico de enfermagem.
- **Evolução da Enfermagem**: Acompanhamento contínuo do estado do paciente.
- **Impressão de Relatórios**: Opção para imprimir os registros diretamente ou salvar em PDF.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do desenvolvimento.
- **PyQt6**: Utilizado para a interface gráfica.
- **SQLite**: Banco de dados leve e portável para armazenamento de dados.
- **HTML/CSS/JavaScript**: Para a estruturação e estilo das páginas do sistema.

## Como Executar

1. Clone o repositório:
git clone https://github.com/hadelrachid/projeto_sistema_enfermagem.git

2. Navegue até o diretório do projeto:
cd projeto_sistema_enfermagem

3. Instale as dependências necessárias:
pip install -r requirements.txt

4. Execute o projeto:
python main.py

## Contribuições

Contribuições são bem-vindas! Se você tem alguma sugestão ou encontrou um problema, por favor, abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).


