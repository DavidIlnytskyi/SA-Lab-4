# SA-Lab-4

Author: Davyd Ilnytskyi

Queue: Kafka

---

### Setup hazelcast network
`docker network create --subnet=172.18.0.0/16 hazelcast-network`

###
```
pip install -r requirements.txt
```

### Setup hazelcast node
```
bash ./bash-scripts/setup-hazelcast.sh
```

### Setup Config, Facade, Logging, Message services
```
python3 ./python-scripts/setup.py
```

---

# Tasks
