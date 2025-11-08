@echo off
REM Comprehensive API testing script for Windows

echo Testing Smart Parking System Backend API
echo ==========================================

set BASE_URL=http://localhost:5000
set PASSED=0
set FAILED=0

echo.
echo 1. Health Check
curl -s -o nul -w "%%{http_code}" "%BASE_URL%/health"
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Health check
    set /a PASSED+=1
) else (
    echo [FAILED] Health check
    set /a FAILED+=1
)

echo.
echo 2. Root Endpoint
curl -s -o nul -w "%%{http_code}" "%BASE_URL%/"
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Root endpoint
    set /a PASSED+=1
) else (
    echo [FAILED] Root endpoint
    set /a FAILED+=1
)

echo.
echo 3. API Documentation
curl -s -o nul -w "%%{http_code}" "%BASE_URL%/api/docs"
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Swagger UI
    set /a PASSED+=1
) else (
    echo [FAILED] Swagger UI
    set /a FAILED+=1
)

echo.
echo 4. Authentication Tests
echo    Registering test user...
curl -s -X POST "%BASE_URL%/api/v1/auth/register" ^
    -H "Content-Type: application/json" ^
    -d "{\"email\":\"testuser@example.com\",\"password\":\"test123\",\"full_name\":\"Test User\"}" > nul

echo    Logging in...
for /f "tokens=*" %%i in ('curl -s -X POST "%BASE_URL%/api/v1/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser@example.com&password=test123"') do set LOGIN_RESPONSE=%%i

echo    Login response received

echo.
echo 5. Parking Lots Tests
curl -s -o nul -w "%%{http_code}" "%BASE_URL%/api/v1/parking-lots/"
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Get all parking lots
    set /a PASSED+=1
) else (
    echo [FAILED] Get all parking lots
    set /a FAILED+=1
)

echo.
echo ==========================================
echo Test Results:
echo Passed: %PASSED%
echo Failed: %FAILED%
echo ==========================================
pause


