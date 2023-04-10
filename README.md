# ZSSN - Rede Social de Sobrevivência Zumbi

ZSSN (Rede Social de Sobrevivência Zumbi) é uma rede social para um mundo com cenário apocalíptico, infestado por um vírus produzido em laboratório que está transformando seres humanos e animais em zumbis. O objetivo é desenvolver um sistema para compartilhar recursos entre humanos não infectados. E esta, é uma _API REST_ que armazenará informações sobre os sobreviventes em um apocalipse zumbi, bem como os recursos que eles possuem.

## Casos de uso

-   Adicionar sobreviventes ao banco de dados
-   Atualizar local do sobrevivente
-   Sinalizar sobrevivente como infectado
-   Negociação de recursos entre sobreviventes
-   Emitir relatórios - porcentagem de: sobreviventes infectados, sobreviventes não infectados. Quantidade média de cada tipo de recurso por sobrevivente. Pontos perdidos por causa do sobrevivente infectado.

## Executar

Para executar o projeto siga os comandos abaixo:

-   Criar e ativar ambiente virtual:

```
python3 -m venv venv && source venv/bin/activate
```

-   Instalar as dependências:

```
pip install -r requirements.txt
```

-   Executar as migrations:

```
python manage.py makemigrations
python manage.py migrate
```

-   Executar as testes:

```
python manage.py test
```

-   Executar as projeto:

```
python manage.py runserver
```

## Documentação

A documentação da api pode ser encontrada acessando as urls `/` e `/redoc`.

## Tecnologias

-   <a href='https://www.djangoproject.com/' target='_blank'>Django</a>
-   <a href='https://www.django-rest-framework.org/' target='_blank'>Django Rest Framework</a>
-   <a href='https://developer.mozilla.org/pt-BR/docs/Web/HTML' target='_blank'>HTML</a>
-   <a href='https://developer.mozilla.org/pt-BR/docs/Web/CSS/' target='_blank'>CSS</a>
-   <a href='https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/' target='_blank'>Javascript</a>
-   <a href='https://git-scm.com/' target='_blank'>Git</a>
-   <a href='https://www.postgresql.org/' target='_blank'>PostgreSQL</a>
-   <a href='https://drf-yasg.readthedocs.io/en/stable/' target='_blank'>drf yasg</a>
