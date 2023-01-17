# Chat com Vue.JS e FastAPI com websocket


- Autenticação de usuário e senha (sem criptografia e segurança necessários apenas para o protótipo)
- Criação de Sala
- Chat simultâneo 

## Instalação API
- Versão do python: 3.10 necessária

### Entrar na pasta do backend
```
cd service
```

### Criar e instalar pacotes no ambiente virtual
```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r requirements.txt
```


### Subir API
```
uvicorn main:app --reload
```

### Documentação
[http://localhost:8000/docs]


## Frontend
- Versão Node necessária: v17.9.0

### Entrar na pasta
```
cd frontend/chat
```

### Instalar pacotes
```
npm install
```

### Iniciar projeto
```
npm run serve
```

### Link sistema
[http://localhost:8080/]

