#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	
	-- Create training data table to record INGESTION
	CREATE TABLE inference (
		inference_id SERIAL PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        model VARCHAR(255) NOT NULL,
        start_at TIMESTAMP NOT NULL,
        results_file VARCHAR(255) NOT NULL
	);
	
EOSQL