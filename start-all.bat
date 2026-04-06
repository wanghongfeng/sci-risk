@echo off
echo ========================================
echo 启动供应链风险模拟平台
echo ========================================

echo.
echo [1/4] 启动后端服务 (端口 8080)...
start "Backend Service" cmd /k "cd /d d:\12.code\test\sci\risk\backend\risk-basic-service && java -jar target\risk-basic-service-1.0.0.jar"

timeout /t 8 /nobreak >nul

echo.
echo [2/4] 启动算法服务 1 (端口 5000)...
start "Algorithm Service 1" cmd /k "cd /d d:\12.code\test\sci\risk\algorithms\risk-algorithm-service && python main.py"

echo.
echo [3/4] 启动算法服务 2 (端口 5001)...
start "Algorithm Service 2" cmd /k "cd /d d:\12.code\test\sci\risk\algorithms\risk-ml-algorithm && python main.py"

timeout /t 3 /nobreak >nul

echo.
echo [4/4] 启动前端服务 (端口 3000)...
start "Frontend Service" cmd /k "cd /d d:\12.code\test\sci\risk\frontend && npm run dev"

echo.
echo ========================================
echo 所有服务已启动！
echo ========================================
echo.
echo 服务地址：
echo - 前端: http://localhost:3000/sci-risk/
echo - 后端: http://localhost:8080
echo - 算法服务1: http://localhost:5000
echo - 算法服务2: http://localhost:5001
echo.
echo Swagger文档：
echo - 后端: http://localhost:8080/swagger-ui.html
echo - 算法服务1: http://localhost:5000/apidocs/
echo.
