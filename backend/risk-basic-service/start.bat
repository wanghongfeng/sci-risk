@echo off
set DB_URL=jdbc:postgresql://neondb_owner:npg_Q6ISApjOe0cy@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require
set DB_USERNAME=neondb_owner
set DB_PASSWORD=npg_Q6ISApjOe0cy
set ALGORITHM_TARIFF_ENDPOINT=http://localhost:5000/tariff
set ALGORITHM_SCENARIO_ENDPOINT=http://localhost:5000/scenario
set ALGORITHM_ML_ENDPOINT=http://localhost:5001/ml
set CALLBACK_URL=http://localhost:8080
set SERVER_PORT=8080
set SPRING_PROFILES_ACTIVE=local
cd /d %~dp0
call mvn spring-boot:run
