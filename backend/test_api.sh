#!/bin/bash
# Comprehensive API testing script

echo "🧪 Testing Smart Parking System Backend API"
echo "=========================================="

BASE_URL="http://localhost:5000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    local headers=$5
    
    echo -n "Testing: $description... "
    
    if [ "$method" = "GET" ]; then
        if [ -n "$headers" ]; then
            response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL$endpoint" -H "$headers")
        else
            response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL$endpoint")
        fi
    elif [ "$method" = "POST" ]; then
        if [ -n "$headers" ]; then
            response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
                -H "Content-Type: application/json" \
                -H "$headers" \
                -d "$data")
        else
            response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
                -H "Content-Type: application/json" \
                -d "$data")
        fi
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        echo "  Response: $body"
        ((FAILED++))
    fi
}

echo ""
echo "1. Health Check"
test_endpoint "GET" "/health" "Health check"

echo ""
echo "2. Root Endpoint"
test_endpoint "GET" "/" "Root endpoint"

echo ""
echo "3. API Documentation"
test_endpoint "GET" "/api/docs" "Swagger UI"

echo ""
echo "4. Authentication Tests"
echo "   Registering test user..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "testuser@example.com",
        "password": "test123",
        "full_name": "Test User",
        "phone_number": "+1234567890"
    }')

if echo "$REGISTER_RESPONSE" | grep -q "email"; then
    echo -e "${GREEN}✓ User registered${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ User may already exist${NC}"
fi

echo "   Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser@example.com&password=test123")

TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ Login successful${NC}"
    ((PASSED++))
    AUTH_HEADER="Authorization: Bearer $TOKEN"
    
    echo "   Getting current user..."
    test_endpoint "GET" "/api/v1/users/me" "Get current user" "" "$AUTH_HEADER"
else
    echo -e "${RED}✗ Login failed${NC}"
    ((FAILED++))
    AUTH_HEADER=""
fi

echo ""
echo "5. Parking Lots Tests"
test_endpoint "GET" "/api/v1/parking-lots/" "Get all parking lots"
test_endpoint "GET" "/api/v1/parking-lots/nearby?latitude=40.7128&longitude=-74.0060&radius_km=5" "Get nearby parking lots"

echo ""
echo "6. Safety Ratings Tests"
test_endpoint "GET" "/api/v1/safety/1" "Get safety rating"

echo ""
echo "7. Analytics Tests"
if [ -n "$AUTH_HEADER" ]; then
    test_endpoint "GET" "/api/v1/analytics/dashboard" "Get dashboard analytics" "" "$AUTH_HEADER"
fi

echo ""
echo "=========================================="
echo "Test Results:"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "=========================================="


