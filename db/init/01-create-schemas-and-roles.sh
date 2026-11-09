#!/bin/bash
set -euo pipefail

psql \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  --set=backend_password="$BACKEND_DB_PASSWORD" \
  --set=ai_password="$AI_DB_PASSWORD" <<'EOSQL'
CREATE ROLE backend_user LOGIN PASSWORD :'backend_password';
CREATE ROLE ai_user LOGIN PASSWORD :'ai_password';

CREATE SCHEMA backend AUTHORIZATION backend_user;
CREATE SCHEMA ai AUTHORIZATION ai_user;

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA backend FROM PUBLIC;
REVOKE ALL ON SCHEMA ai FROM PUBLIC;

GRANT USAGE, CREATE ON SCHEMA backend TO backend_user;
GRANT USAGE, CREATE ON SCHEMA ai TO ai_user;
EOSQL
