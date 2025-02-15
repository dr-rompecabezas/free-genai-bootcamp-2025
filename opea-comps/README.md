# Building the ChatQnA Megaservice in OPEA

Following OPEA's instructions to launch the [ChatQnA Example](https://opea-project.github.io/latest/getting-started/README.html), I managed to get most docker containers running, but after multiple tries and hours of troubleshooting, I was unable to get the entire system to work.

The EC2 instance was configured exactly per the instructions:

- Ubuntu
- m7i.4xlarge (Intel Xeon)
- 100 GiB

The following docker OPEA microservices were running:

- chatqna-xeon-nginx-server
- chatqna-xeon-ui-server
- chatqna-xeon-backend-server
- retriever-redis-server
- dataprep-redis-server
- redis-vector-db

The following docker OPEA microservices were not running:

- vllm-service
- tei-embedding-server
- tei-reranking-server

The following is an exemple of an error observed:

`api_server.py: error: argument --model: expected one argument`

This appears to refer to a variable set by the `chatqna.py` in the OPEA GenAIExamples repository.

```python
# ChatQnA/chatqna.py
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
```

However, the variable was clearly set in the Ubuntu environment:

```bash
echo $LLM_MODEL
meta-llama/Meta-Llama-3-8B-Instruct
```

Eventually, I destroyed the EC2 instance with the intention to try a different approach at a later time.
