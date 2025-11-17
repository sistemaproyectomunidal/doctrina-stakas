# Architecture - High Level

- api-gateway: single entrypoint (FastAPI)
- ml-service: model inference endpoints (FastAPI)
- social-service: handles social integrations (FastAPI)
- ads-service: handles ad creation / management (FastAPI)
- Postgres: relational store for metadata
- MinIO: S3-compatible object storage for media
