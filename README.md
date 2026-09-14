<div align="center">
  
  <h1>Agenda Lash Mobile 🌸</h1>
  <p><strong>Sistema de Gestão e Agendamento para Estúdios de Beleza e Lash Designers</strong></p>

  <p>
    <img src="https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React Native" />
    <img src="https://img.shields.io/badge/Expo-000020?style=for-the-badge&logo=expo&logoColor=white" alt="Expo" />
    <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  </p>
</div>

---

## 📖 Sobre o Projeto

O **Agenda Lash** é um aplicativo mobile completo concebido especificamente para simplificar e profissionalizar a rotina operacional de estúdios de extensão de cílios e beleza. 

Desenvolvido com **React Native (Expo)** e integrado a uma API RESTful em **Python (Flask + SQLite)**, o aplicativo oferece agendamento inteligente com detecção de conflitos de horários, controle de clientes, catálogo de procedimentos, relatórios analíticos de faturamento e gestão de equipe.

---

## ✨ Funcionalidades Principais

### 1. 📅 Agenda Inteligente & Calendário
* **Visualização Mensal:** Calendário com marcação dinâmica via bolinhas e destaque visual com dia circulado para datas de alta demanda (4 ou mais agendamentos).
* **Grade de 30 em 30 minutos:** Escala de 24 horas (00:00 às 23:30) com bloqueio automático de horários ocupados de acordo com a duração do procedimento.
* **Autocomplete de Clientes:** Busca em tempo real por nome ou telefone direto na lista de clientes cadastrados.
* **Gestão de Vagas:** Opção de cancelamento que remove o atendimento do banco e libera a vaga instantaneamente.

### 2. 📊 Painel Geral (Dashboard do Dia)
* **Métricas do Dia:** Resumo diário de clientes agendados e faturamento previsto em tempo real.
* **Destaque do Próximo Atendimento:** Card prioritário com o próximo horário e atalho rápido com link para confirmação direta no WhatsApp.
* **Ações Rápidas:** Modal para marcar status como **Concluído**, **Cancelado** ou **Reagendar** (com redirecionamento automático para a tela de agenda).

### 3. 👥 Gestão de Clientes (CRUD)
* Cadastro completo de clientes com nome e telefone (chave identificadora).
* Busca em tempo real por nome ou número.
* Edição de dados e exclusão com diálogo de confirmação.

### 4. 💅 Catálogo de Serviços e Procedimentos (CRUD)
* Cadastro de procedimentos com código identificador (`cod_proc`), nome, tempo de duração estimado (`temp_proc`) e valor tabelado (`valor_proc`).
* Atualização rápida de valores e prazos.

### 5. 📈 Relatórios Analíticos & Métricas (Status)
* **Filtros Temporais:** Alternância entre relatórios **Mensais** e **Anuais** com navegação retroativa e futura.
* **Gráficos de Faturamento:** Visualização em barras com o `react-native-gifted-charts`, mostrando o faturamento por semana (mês) ou mês a mês (ano).
* **Indicadores Financeiros:** Faturamento realizado, faturamento previsto e ticket médio por atendimento.
* **Ranking de Serviços:** Lista de procedimentos mais rentáveis com barra de progresso visual.

### 6. ⚙️ Painel de Configurações & Segurança
* Cadastro de novas contas de acesso para funcionários/recepcionistas com senhas criptografadas via `generate_password_hash`.
* Alteração de senha da conta ativa através do e-mail.
* Diagnóstico de conexão com a API e versão do app.

---

## 🛠️ Tecnologias Utilizadas

### Frontend Mobile
* **[React Native](https://reactnative.dev/)** com **[Expo SDK](https://expo.dev/)**
* **[TypeScript](https://www.typescriptlang.org/)** para tipagem estática e segurança de código
* **[React Navigation](https://reactnavigation.org/)** (Native Stack Navigation)
* **[Lucide React Native](https://lucide.dev/)** para ícones modernos
* **[react-native-calendars](https://github.com/wix/react-native-calendars)** para renderização de calendários
* **[react-native-gifted-charts](https://github.com/Abhinandan-Kushwaha/react-native-gifted-charts)** para relatórios gráficos
* **[expo-splash-screen](https://docs.expo.dev/versions/latest/sdk/splash-screen/)** e **[expo-linear-gradient](https://docs.expo.dev/versions/latest/sdk/linear-gradient/)**

### Backend & Banco de Dados
* **[Python](https://www.python.org/)** & **[Flask](https://flask.palletsprojects.com/)**
* **[SQLite3](https://sqlite.org/)** para armazenamento relacional leve
* **[Werkzeug Security](https://werkzeug.palletsprojects.com/)** para hashing seguro de senhas

---

## 📂 Estrutura de Diretórios

```plaintext
app_lash_agenda/
├── assets/
│   └── img/
│       └── primary.png          # Logotipo e assets visuais
├── src/
│   ├── auth/
│   │   └── LoginScreen/         # Fluxo de autenticação
│   ├── colors/
│   │   └── colors.ts            # Paleta de cores da identidade visual
│   ├── screens/
│   │   ├── Agenda/              # Agenda com grid 30m e calendário
│   │   ├── Clientes/            # CRUD de clientes
│   │   ├── Configuracoes/       # Modal de usuários e senhas
│   │   ├── Dashboard/           # Painel geral e métricas do dia
│   │   ├── Procedimentos/       # CRUD de serviços e procedimentos
│   │   ├── Status/              # Gráficos analíticos mensais/anuais
│   │   └── HomeScreen.tsx       # Bottom bar e roteamento de abas
│   └── services/
│       ├── ClientService/       # Comunicação com a rota /cliente
│       ├── ProcedureService/    # Comunicação com a rota /procedure
│       ├── SchedulingService/   # Comunicação com a rota /agendamento
│       └── UserService/         # Comunicação com a rota /users
├── App.tsx                      # Ponto de entrada, carregamento de fontes e splash
├── app.json                     # Configurações do Expo e Splash Screen
├── eas.json                     # Perfil de geração de APK/AAB via EAS Build
└── package.json
