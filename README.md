<div align="center">
  <h1>Agenda Lash API ⚙️🌸</h1>
  <p><strong>RESTful API para Gestão Operacional, Agendamentos e Segurança do Estúdio Lash</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
    <img src="https://img.shields.io/badge/Werkzeug-Security-F7DF1E?style=for-the-badge&logo=security&logoColor=black" alt="Werkzeug" />
  </p>
</div>

---

## 📖 Visão Geral

A **Agenda Lash API** é o núcleo de regras de negócio e persistência do ecossistema Agenda Lash. Construída com arquitetura modular utilizando **Flask Blueprints** e **SQLite**, a API provê endpoints otimizados para consumo por clientes móveis (React Native/Expo).

Ela gerencia o ciclo completo de atendimentos, cálculo dinâmico de horário de término baseado na duração dos procedimentos, validação de choque de horários (conflitos na agenda), além de persistência de clientes, procedimentos e controle seguro de credenciais de usuários.

---

## 🚀 Arquitetura e Módulos

O projeto adota estrutura modular por responsabilidade:

```plaintext
api-agendalash/
├── src/
│   ├── database/
│   │   └── conn.py                # Gerenciador de conexão SQLite
│   ├── routes/ (Blueprints)
│   │   ├── users.py               # Autenticação e gestão de usuários
│   │   ├── client.py              # Gestão de clientes (base de contatos)
│   │   ├── procedure.py           # Gestão da tabela de serviços e preços
│   │   └── agendamento.py         # Agenda inteligente, validação e datas
│   └── validations/
│       ├── valid_hour.py          # Verificação de disponibilidade de horários
│       └── valid_proc_end_hour.py # Cálculo do dt_end conforme a duração do serviço
├── app.py                         # Inicialização e registro de Blueprints
└── requirements.txt