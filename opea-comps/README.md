# Building the OPEA ChatQnA Megaservice

This repository contains the work done to build the OPEA ChatQnA Megaservice. Two attempts were made to build the service: one on a Mac M1 chip and another on an AWS EC2 instance. Both attempts were partially successful, with the Mac M1 chip build having more success than the AWS EC2 instance build.

## Mac M1 Chip

Here's a summary of what was accomplished. For the full details, please refer to the [Mac M1 Chip README](GenAIExamples/ChatQnA/docker_compose/intel/cpu/aipc/README.md).

  1. Adapted Intel-based ChatQnA for Mac ARM Architectures:
    - Added platform: linux/amd64 to all services in the compose.yaml file to enable emulation
    - Updated set_env.sh to properly detect Mac IP addresses and handle Docker networking
    - Changed the LLM model from llama3.2 to tinyllama for better compatibility with memory constraints
  2. Addressed Runtime Issues:
    - Fixed port conflict for port 7000 by changing port mapping
    - Ensured proper environment variable configuration
    - Added Hugging Face token for accessing models
  3. Current Status:
    - LLM Service (Ollama): Working with TinyLLama model
    - Embedding Service: Working
    - Retriever Service: Not working due to AVX instruction incompatibility
    - Web UI: Working
  4. Limitations:
    - No RAG capabilities due to retriever service failures
    - Only basic chat functionality is available
    - Some performance impact from emulation
  5. Documentation Updates:
    - Added comprehensive notes about ARM compatibility issues
    - Documented required changes and known limitations
    - Provided troubleshooting steps for common issues

  This adaptation demonstrates that it's possible to run parts of the ChatQnA service on Mac ARM architecture, though with limited functionality. For a full ChatQnA experience with RAG capabilities, users would either need x86 hardware or
  custom ARM-native builds of the components.

  The updated README now clearly communicates these limitations and provides guidance for users attempting to use the system on Mac ARM architecture, setting proper expectations while still enabling basic functionality.

## AWS EC2 Instance

An attempt to deploy the [ChatQnA Example](https://opea-project.github.io/latest/getting-started/README.html) on AWS EC2 resulted in partial success. Despite following the official OPEA instructions, only some components of the system became operational.

The EC2 instance was configured according to specifications:

- Ubuntu
- m7i.4xlarge (Intel Xeon)
- 100 GiB

The following docker OPEA microservices successfully launched:

- chatqna-xeon-nginx-server
- chatqna-xeon-ui-server
- chatqna-xeon-backend-server
- retriever-redis-server
- dataprep-redis-server
- redis-vector-db

These microservices failed to launch:

- vllm-service
- tei-embedding-server
- tei-reranking-server

A notable error observed during troubleshooting:

`api_server.py: error: argument --model: expected one argument`

This error appears related to a variable defined in `chatqna.py` in the OPEA GenAIExamples repository:

```python
# ChatQnA/chatqna.py
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
```

Although the environment variable was properly set in the Ubuntu environment:

```bash
echo $LLM_MODEL
meta-llama/Meta-Llama-3-8B-Instruct
```

After extensive troubleshooting without resolution, the EC2 instance was terminated to allow for a different approach in the future.
