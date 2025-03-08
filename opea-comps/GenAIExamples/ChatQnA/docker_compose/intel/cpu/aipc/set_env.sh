#!/usr/bin/env bash

# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

pushd "../../../../../" > /dev/null
if [ -f .set_env.sh ]; then
    source .set_env.sh
fi
popd > /dev/null

# For macOS, use different approach to get IP
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Get the IP address for en0 (usually Wi-Fi) or en1 interfaces on Mac
    export host_ip=$(ifconfig en0 2>/dev/null | grep 'inet ' | awk '{print $2}')
    if [ -z "$host_ip" ]; then
        export host_ip=$(ifconfig en1 2>/dev/null | grep 'inet ' | awk '{print $2}')
    fi
    # If all else fails, use localhost for Docker Desktop
    if [ -z "$host_ip" ]; then
        export host_ip="host.docker.internal"
        echo "Using host.docker.internal for Docker Desktop"
    fi
else
    # Original Linux approach
    export host_ip=$(hostname -I | awk '{print $1}')
fi

if [ -z "${HUGGINGFACEHUB_API_TOKEN}" ]; then
    echo "Error: HUGGINGFACEHUB_API_TOKEN is not set. Please set HUGGINGFACEHUB_API_TOKEN."
fi

if [ -z "${host_ip}" ]; then
    echo "Error: host_ip is not set. Please set host_ip manually."
fi

export HUGGINGFACEHUB_API_TOKEN=${HUGGINGFACEHUB_API_TOKEN}
export EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"
export RERANK_MODEL_ID="BAAI/bge-reranker-base"
export INDEX_NAME="rag-redis"
export OLLAMA_HOST=${host_ip}
export OLLAMA_MODEL="llama3.2"
# Set it as a non-null string, such as true, if you want to enable logging facility,
# otherwise, keep it as "" to disable it.
export LOGFLAG=""

# Fix no_proxy for Mac Docker Desktop if it's not already set
if [ -z "$no_proxy" ]; then
    export no_proxy="localhost,127.0.0.1,host.docker.internal,chatqna-aipc-backend-server,tei-embedding-service,retriever,tei-reranking-service,redis-vector-db,dataprep-redis-service,ollama-service"
else
    export no_proxy="${no_proxy},host.docker.internal,chatqna-aipc-backend-server,tei-embedding-service,retriever,tei-reranking-service,redis-vector-db,dataprep-redis-service,ollama-service"
fi

echo "Host IP set to: $host_ip"
echo "OLLAMA_HOST set to: $OLLAMA_HOST"
