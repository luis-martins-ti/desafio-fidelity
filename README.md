# desafio-fidelity
Refactor aplicação de Web Scraping com estrutura Docker. Aplicação desenvolvida com Python + Django.
Foram criadas novas entidades para atender as necessidades das chaves estrangeiras e remodelado a estrutura geral dos dados.
Para modularizar as consultas em outras plataformas, é necessário criar o MAP dos elementos e ações que o selenium deve executar e gerar uma classe
com as opções para uso no método carrega_site. 

## 🚀 Como iniciar o projeto

### ✅ Pré-requisitos
- Docker + Docker Compose

---

### 🧱 STEP 1 - Build e start com Docker

**Renomeie o arquivo .env.example para .env e execute:**

```bash
docker compose build --no-cache
docker compose up -d
```

### 📦 STEP 2 - Criar Dados para Testes
**Aguarde alguns segundos para a aplicação iniciar e execute:**

```bash
docker compose exec web python manage.py populate_pesquisas
```

### 🖥️ STEP 3 - Executar a aplicação

```bash
docker compose exec web python manage.py run_spv
#Executa com filtro específico
docker compose exec web python manage.py run_spv --filtro 2
```

### 🖥️ STEP 4 - Visualizar os Resultados

```bash
docker compose exec web python manage.py list_pesquisa_spv
```


### 📘 Tecnologias Utilizadas
- Django
- Python
- PostgreSQL
- Docker
- Selenium Web Driver

**Para encerrar a aplicação rodar:**
```bash
docker compose down -v --remove-orphans
```