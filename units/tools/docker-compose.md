---
id: docker-compose
title: Docker Compose
paths: ["**/compose.yaml", "**/compose.yml", "**/docker-compose.yaml", "**/docker-compose.yml", "**/compose.*.yaml", "**/Dockerfile", "**/*.Dockerfile", "**/.dockerignore"]
commands: ["docker compose", "docker-compose", "docker build"]
---
Docker and Docker Compose. Follow the Compose specification and Docker's Dockerfile best practices (docs.docker.com/build/building/best-practices).

Compose files
- Name the file `compose.yaml` for new projects; drop the obsolete top-level `version:` key.
- Pin image tags (`postgres:17`, never `latest`) and give services `healthcheck`s; use `depends_on: { db: { condition: service_healthy } }` instead of sleep loops.
- Secrets and environment-specific values through `.env` (gitignored) or `env_file`, with a committed `.env.example`; never inline credentials.
- Named volumes for data that must survive `down`; bind mounts only for source code in development.
- Profiles or override files (`compose.override.yaml`) for dev-only services, not separate copies of the whole file.

Dockerfiles
- Multi-stage builds: build in one stage, copy only the artifact into a slim runtime image.
- Order layers from least to most frequently changing (dependency manifests and install before source) to keep the cache useful.
- Run as a non-root `USER`; `.dockerignore` excludes `.git`, build output, `node_modules`, and env files.
- Exec-form `CMD`/`ENTRYPOINT` (`["java", "-jar", "app.jar"]`) so signals reach the process.

Working with it
- Check the active context first (`docker context ls`); on Apple Silicon, mind `platform:` for images without arm64 builds.
- `docker compose up -d <service>`, `docker compose logs -f <service>`, `docker compose ps`. Don't `down -v` (it deletes volumes) without the user's go-ahead.
- Validate changes with `docker compose config` before starting.
