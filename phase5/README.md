# Phase 5: Dapr Integration for Event-Driven Architecture

This folder contains the Dapr integration implementation for the Todo Hackathon Phase 5.

## Structure

```
phase5/
├── backend/
│   └── dapr_integration.py       # Dapr pub/sub and state management module
├── notification-service/
│   ├── main.py                   # Standalone notification service
│   ├── Dockerfile                # Container image
│   └── requirements.txt          # Python dependencies
├── dapr-components/
│   ├── kafka-pubsub.yaml        # Dapr Kafka pub/sub component
│   └── statestore.yaml          # Dapr Redis state store component
└── docs/
    ├── integration_guide.md     # How to integrate Dapr
    └── testing_guide.md         # How to test Dapr features
```

## Features

### 1. Event-Driven Pub/Sub
- Task events published to Kafka when created/updated/completed/deleted
- Notification service subscribes to events via Dapr
- Decoupled microservices architecture

### 2. State Management
- Redis-backed state store via Dapr
- API endpoints for saving/retrieving app state
- Cached data for performance

### 3. Cloud-Native
- Runs on Azure Kubernetes Service (AKS)
- Kafka KRaft mode (no ZooKeeper)
- Optimized for single-node free-tier cluster

## Quick Start

See `docs/integration_guide.md` for detailed instructions.

## Author

Tahir Yamin <tahiryamin2050@gmail.com>
