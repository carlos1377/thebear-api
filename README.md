<p align="center" ><img align="center" src="github-logo.png" width=50></p>
<h1 align="center">The Bear API </h1>

<p align="center">
 <a href="#started">Getting Started</a> • 
  <a href="#routes">API Endpoints</a> •
 <a href="#colab">Collaborators</a> •
 <a href="#contribute">Contribute</a>
</p>

<p align="center">
  <b>Uma API desenvolvida para utilização em sistemas para Bares e estabelecimentos correlacionados.</b>
</p>


<h2 id="started">🚀 Configurando a API Localmente</h2>

Para testar a API localmente vamos precisar de alguns pré-requisitos

### Pré requisitos

- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/get-started/)

### ⬇️ Clonando o repositório

Execute o seguinte comando na pasta onde deseja clonar o repositório

```bash
git clone https://github.com/carlos1377/thebear-api.git
```

### ⚙️ Configurando o .ENV

Utilize como base o arquivo `.env-example` para criar um arquivo `.env` na raiz do projeto com suas configurações

 - Configure as informações do Banco de Dados MySQL
 - Certifique-se de usar a variável `TEST_MODE = 1` para você ter acesso a todos endpoints e conseguir utilizar corretamente a API posteriormente.
 - Gere uma chave aleatória para a variável `SECRET_KEY`.

### 🐳 Docker Compose

Para rodar o projeto usando containers do docker execute os seguintes comandos

```bash
cd thebear-api # Para entrar no diretório do projeto

docker-compose up # Pull das imagens e build dos serviços

docker-compose run --user 1000 bear sh -c "alembic upgrade heads" # Para aplicar as migrações ao banco
```
Após o Build do Docker e a inicialização do Uvicorn, execute o comando `curl http://localhost:8000/health-check` caso você tenha o Curl instalado, ou por meio de uma ferramenta de requisições para APIs como [Postman](https://www.postman.com/downloads/) ou [Insomnia](https://insomnia.rest/download) para a rota descrita acima (`http://localhost:8000/health-check`). Se tudo estiver correto, a requisição deve retornar `{"message":"OK"}`.

## 🚩 Documentação de Rotas

Sendo a principal tecnologia usada nesse projeto o [FastAPI](https://fastapi.tiangolo.com/) o framework proporciona uma "auto-documentação" das rotas da API, podendo ser acessado pelo seu navegador na rota `http://localhost:8000/docs`. 

Atualmente estou trabalhando em também em uma documentação providenciada pela [Scalar](https://docs.scalar.com), como possivelmente sendo o meio principal de documentação de rotas do **The Bear** futuramente.

## 🚧 Testes

Se você modificar o projeto e quiser ter certeza que tudo está funcionando, execute os testes do Pytest usando o Docker. Podemos fazer isso com o seguinte comando 

```bash
docker ps # Vai nos retornar o ID dos container que estão UP

# Certifique-se de trocar {YOUR_CONTAINER_ID} pelos 4 primeiros digitos do ID do container Bear
docker exec -it {YOUR_CONTAINER_ID} bash
```

Com isso estaremos usando o *bash* dentro do container Bear, para rodar os testes execute o comando
```bash
pytest
```
 
Para mais informações sobre o uso do [Pytest](https://docs.pytest.org) considere consultar a documentação do mesmo.

## 💻 Tecnologias usadas no projeto

- FastAPI
- Poetry
- Pydantic
- SQLAlchemy
- Pytest
- MySQL
- Docker