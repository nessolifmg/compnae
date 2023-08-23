# ComPNAE

Esse sistema foi desenvolvido com o intuito de gerenciar o fornecimento de alimentos para o IFMG-Campus Bambuí. Alimentos esses, oriundos de processos licitatórios por parte de produtores rurais da região. 

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.


### 📋 Pré-requisitos

 1. Clonar o Projeto

- Clone o projeto do repositório usando o seguinte comando:

```bash
git clone git@github.com:nessolifmg/compnae.git
cd compnae
```

2. Criar Ambiente Virtual

- No terminal, certifique-se de estar no diretório raiz do projeto.

- Execute os seguintes comandos para criar e ativar o ambiente virtual via pip:
```bash
# Instale o virtualenv (caso ainda não esteja instalado)
pip install virtualenv

# Crie um ambiente virtual chamado "compnae"
virtualenv compnae

# Ative o ambiente virtual (no macOS/Linux)
source compnae/bin/activate

# Ative o ambiente virtual (no Windows)
source compnae\Scripts\activate
```
```bash
# Instale o virtualenv (caso ainda não esteja instalado)
pip install virtualenv

# Crie um ambiente virtual chamado "compnae"
virtualenv compnae

# Ative o ambiente virtual (no macOS/Linux)
source compnae/bin/activate

# Ative o ambiente virtual (no Windows)
source compnae\Scripts\activate
```
- Execute os seguintes comandos para criar e ativar o ambiente virtual via conda:

```bash
# Crie um ambiente virtual chamado "compnae"
conda create --name compnae

# Ative o ambiente virtual
conda activate compnae
```

3. Instalar as dependências do projeto: 
- Este comando deve ser executado no terminal, no mesmo diretório onde o arquivo requirements.txt está localizado.
```bash
  pip install -r requirements.txt
```

2. Configurar variáveis de ambiente para configurações do Django:
```bash
export DEBUG=True
export ALLOWED_HOSTS='localhost,127.0.0.1'
``` 

3. Configurar variáveis de ambiente para o envio de e-mails: (opcional)
```bash
export MAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
export EMAIL_HOST='smtp.gmail.com'
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export EMAIL_HOST_USER='seu-email-aqui@gmail.com'
export EMAIL_HOST_PASSWORD='sua-senha-aqui'
```

### 🔧 Instalação

Para que você possa executar o projeto em um ambiente de desenvolvimento, execute os seguintes passos:
- Na pasta do projeto ```compnae```;
- Na listagem dos itens desse diretório deve conter um arquivo chamado ```manage.py```, por meio dele será possível executar os comandos para executar o projeto;
- Após localizar esse arquivo, digite no seu terminal:
```bash
  python manage.py makemigrations
```
Em seguida: 
```bash
  python manage.py migrate
```
- Após execução desses códigos crie um super-usuário, para acessar todos os recursos padrão django, através do comando:
```bash
  python manage.py createsuperuser
```
- Após executar esse comando, será solicitado um usuário, e-mail e senha. 
- A seguir, para executar o projeto:
```bash
  python manage.py runserver
```

## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

* [Django](https://docs.djangoproject.com/en/4.2/) - Django é um framework web Python de alto nível que incentiva o desenvolvimento rápido e um design limpo.
* [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) - Framework Web responsivo com diversos recursos


## 📌 Versão

Esse sistema está atualmente na sua primeira versão. 

## ✒️ Autores

Todos os envolvidos no desenvolvimento desse projeto, encontram-se abaixo listados. 

* **Colaborador** - *Planejamento e programação* - [Jorge Murilo](https://github.com/Jorge-Comp)
* **Colaborador** - *Planejamento e programação* - [Lucas Batista](https://github.com/luks-santos)
* **Professor Orientador** - *Documentação* - [Marcos Ribeiro](https://github.com/ribeiromarcos)

Você também pode ver a lista de todos os [colaboradores](https://github.com/usuario/projeto/colaboradores) que participaram deste projeto.

## 📄 Licença

Este projeto está sob a licença (sua licença) - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

## 🎁 Expressões de gratidão

* Conte a outras pessoas sobre este projeto 📢;
* Implemente esse projeto em sua instituição;
* Contate-nos para sugestões;

