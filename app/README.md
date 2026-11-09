# AI Onboarding API

## Prerequisites

- Docker Engine 29.6.1 or compatible
- Docker Compose v5.3.0 or compatible
- Container Python 3.11
- FastAPI 0.162.2
- Ollama 0.40.12
- Ollama model `qwen3:8b`

Python and project packages run inside the container. A local Python virtual
environment is not required.

## Start the development server

Create the local environment file once:

```powershell
Copy-Item .env.example .env
```

Replace every `replace-with-...` value in `.env`. The `.env` file is ignored
by Git.

```powershell
docker compose up --build -d
```

Run the same command after changing application code so the image includes the
latest source.

Check container status:

```powershell
docker compose ps
```

Check the API:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected result:

```text
status
------
ok
```

## PostgreSQL schemas and accounts

The PostgreSQL container creates two isolated work areas on its first start:

- `backend` schema, owned by `backend_user`
- `ai` schema, owned by `ai_user`

Each account can create objects only in its own schema. PostgreSQL data is
stored in the named Docker volume `postgres-data` and survives container
restarts. The default host port is `5433` to avoid conflicts with an existing
local PostgreSQL service; containers use port `5432` internally.

Check PostgreSQL status:

```powershell
docker compose ps postgres
```

Initialization scripts run only when the database volume is empty. Later
schema changes must use migrations instead of editing an already-run script.

The `vector` extension is enabled automatically for a new database. To enable
it in an existing local database volume, run:

```powershell
Get-Content -Raw db/init/02-enable-vector.sql | `
  docker compose exec -T postgres `
  psql -U postgres -d ai_onboarding -v ON_ERROR_STOP=1
```

Confirm the extension:

```powershell
docker compose exec -T postgres `
  psql -U postgres -d ai_onboarding `
  -c "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
```

API documentation is available at <http://localhost:8000/docs>.

## Run tests

Run the automated tests in the same Docker Python environment used by the
application:

```powershell
docker compose run --rm --build `
  -v "${PWD}\tests:/workspace/tests:ro" `
  ai-server python -m unittest discover -s tests -v
```

## Test the Ollama connection

Ollama runs on the Windows host. The FastAPI container connects through
`host.docker.internal:11434` and uses `qwen3:8b`.

Make sure the Ollama Windows application is running. If its API is not
available, start the server in PowerShell:

```powershell
ollama serve
```

```powershell
$body = @{ question = "한 문장으로 자기소개해줘." } | ConvertTo-Json
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/api/v1/chat/test `
  -ContentType "application/json; charset=utf-8" `
  -Body $body
```

## View logs

```powershell
docker compose logs -f ai-server
```

## Stop the environment

```powershell
docker compose down
```
