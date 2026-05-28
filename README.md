# Exercício 11 — RabbitMQ (Python)

Este projeto implementa um sistema de monitoramento de sensores industriais usando **RabbitMQ** com o protocolo **AMQP**. Três tipos de sensores publicam leituras em filas distintas, e consumidores especializados processam cada fila, simulando ações como acionamento de alertas e atuadores.

## Arquitetura

```
[producer_temperature.py] ──→ fila: temperature ──→ [consumer_temperature.py]
[producer_humidity.py]    ──→ fila: humidity    ──→ [consumer_humidity.py]
[producer_pressure.py]    ──→ fila: pressure    ──→ [consumer_pressure.py]
                    (via factory-exchange — direct)
```

- **producer_temperature.py** — publica leituras de temperatura (20°C a 100°C) a cada 3 segundos
- **producer_humidity.py** — publica leituras de umidade (30% a 100%) a cada 4 segundos
- **producer_pressure.py** — publica leituras de pressão (1 bar a 15 bar) a cada 5 segundos
- **consumer_temperature.py** — processa leituras de temperatura; emite alerta e aciona sistema de resfriamento se > 80°C
- **consumer_humidity.py** — processa leituras de umidade; emite alerta e aciona desumidificador se > 90%
- **consumer_pressure.py** — processa leituras de pressão; emite alerta e aciona válvula de alívio se > 10 bar

## Tecnologias utilizadas

- Python 3
- RabbitMQ (broker AMQP)
- rabbitpy (cliente Python para RabbitMQ)
- Amazon Linux 2023 (EC2)

## Pré-requisitos

- Duas instâncias EC2 com Amazon Linux 2023
- Portas 5672 e 15672 liberadas no Security Group
- Python 3 e pip instalados nas duas instâncias

## Configuração

Edite o arquivo `const.py` com o IP privado da EC2-1 (servidor RabbitMQ):

```python
RABBITMQ_ADDR  = "172.31.x.x"  # IP privado da EC2-1
RABBITMQ_USER  = "myuser"
RABBITMQ_PASS  = "abc123"
RABBITMQ_VHOST = "my_vhost"
```

## Instalação do RabbitMQ (EC2-1)

```bash
sudo dnf install -y erlang

sudo tee /etc/yum.repos.d/rabbitmq.repo <<EOF
[rabbitmq-server]
name=RabbitMQ Server
baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/8/x86_64
gpgcheck=0
enabled=1
EOF

sudo dnf install -y rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

sudo rabbitmqctl add_user myuser abc123
sudo rabbitmqctl add_vhost my_vhost
sudo rabbitmqctl set_permissions -p my_vhost myuser ".*" ".*" ".*"
```

## Instalação do cliente Python (ambas as instâncias)

```bash
sudo dnf install -y python3-pip git
pip3 install rabbitpy
```

## Como executar

### EC2-1 (consumidores) — abrir 3 terminais

**Terminal 1:**
```bash
python3 consumer_temperature.py
```

**Terminal 2:**
```bash
python3 consumer_humidity.py
```

**Terminal 3:**
```bash
python3 consumer_pressure.py
```

### EC2-2 (produtores) — abrir 3 terminais

**Terminal 1:**
```bash
python3 producer_temperature.py
```

**Terminal 2:**
```bash
python3 producer_humidity.py
```

**Terminal 3:**
```bash
python3 producer_pressure.py
```

## Exemplo de saída

**Produtores (EC2-2):**
```
Published temperature: 83.45°C
Published humidity: 91.20%
Published pressure: 11.73 bar
```

**Consumidores (EC2-1):**
```
[TEMPERATURE] 2026-05-11T01:23:45.123456 → 83.45°C
  ⚠ ALERT: Temperature too high (83.45°C)! Activating cooling system...
[HUMIDITY] 2026-05-11T01:23:46.000000 → 91.20%
  ⚠ ALERT: Humidity too high (91.20%)! Activating dehumidifier...
[PRESSURE] 2026-05-11T01:23:47.000000 → 11.73 bar
  ⚠ ALERT: Pressure critical (11.73 bar)! Triggering pressure relief valve...
```