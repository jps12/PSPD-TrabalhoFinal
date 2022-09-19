# PSPD-TrabalhoFinal

## Como rodar:

### Pré-requisitos:

No arquivo de docker-compose.yml, nos seguintes campos:
```
      - "host.docker.internal:192.168.15.1"
```

Substitua o ip pelo ip local da sua máquina. Caso não saiba, é possível verificar rodando o seguinte comando:
```
docker run -it --rm alpine nslookup host.docker.internal
```

Verifique também se seu arquivo /etc/hosts possui a seguinte linha:
```
127.0.0.1       host.docker.internal
```
Por padrão o docker adiciona essa linha no arquivo, mas em algumas instalações podem acontecer alguns erros.

O elasticsearch por ter problemas de limitação de memória da própria máquina. Para contornar esse problema, é necessário aumentar o limite de memória virtual da máquina, rodando o seguinte comando:
```
sysctl -w vm.max_map_count=262144 
```
### Comandos:

Feitos os prerequisitos, basta apenas iniciar o docker-compose
```
docker-compose up -d
```

É necessário esperar de 5 a 10 minutos para todas as aplicações subirem.
