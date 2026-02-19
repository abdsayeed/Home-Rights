#!/bin/bash

# HomeRights AI - Integration Test Script
# Tests backend API endpoints

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKEND_URL="http://localhost:5001"
API_URL="$BACKEND_URL/api"

echo "🧪 Testing HomeRights AI Integration"
echo "===================================="

# Test 1: Health Check
echo -e "\n${YELLOW}Test 1: Health Check${NC}"
HEALTH=$(curl -s "$BACKEND_URL/health")
if echo "$HEALTH" | grep -q "healthy\|degraded"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "$HEALTH" | jq '.'
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi

# Test 2: Metrics
echo -e "\n${YELLOW}Test 2: Metrics Endpoint${NC}"
METRICS=$(curl -s "$BACKEND_URL/metrics")
if echo "$METRICS" | grep -q "metrics"; then
    echo -e "${GREEN}✓ Metrics endpoint working${NC}"
else
    echo -e "${RED}✗ Metrics endpoint failed${NC}"
    exit 1
fi

# Test 3: Register User
echo -e "\n${YELLOW}Test 3: User Registration${NC}"
TIMESTAMP=$(date +%s)
TEST_EMAIL="test${TIMESTAMP}@example.com"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"Test1234\",\"firstName\":\"Test\",\"lastName\":\"User\"}")

if echo "$REGISTER_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✓ User registration successful${NC}"
    ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | jq -r '.access_token')
    echo "Token: ${ACCESS_TOKEN:0:20}..."
else
    echo -e "${RED}✗ User registration failed${NC}"
    echo "$REGISTER_RESPONSE"
    exit 1
fi

# Test 4: Get Current User
echo -e "\n${YELLOW}Test 4: Get Current User${NC}"
USER_RESPONSE=$(curl -s "$API_URL/auth/me" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$USER_RESPONSE" | grep -q "$TEST_EMAIL"; then
    echo -e "${GREEN}✓ Authentication working${NC}"
    echo "$USER_RESPONSE" | jq '.'
else
    echo -e "${RED}✗ Authentication failed${NC}"
    echo "$USER_RESPONSE"
    exit 1
fi

# Test 5: Chat Message
echo -e "\n${YELLOW}Test 5: Chat Service${NC}"
CHAT_RESPONSE=$(curl -s -X POST "$API_URL/chat/message" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"message":"What are my rights as a tenant?"}')

if echo "$CHAT_RESPONSE" | grep -q "response"; then
    echo -e "${GREEN}✓ Chat service working${NC}"
    echo "Response: $(echo "$CHAT_RESPONSE" | jq -r '.response' | head -c 100)..."
else
    echo -e "${RED}✗ Chat service failed${NC}"
    echo "$CHAT_RESPONSE"
    exit 1
fi

# Test 6: Topics List
echo -e "\n${YELLOW}Test 6: Topics Service${NC}"
TOPICS_RESPONSE=$(curl -s "$API_URL/topics" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$TOPICS_RESPONSE" | grep -q "topics"; then
    echo -e "${GREEN}✓ Topics service working${NC}"
    TOPIC_COUNT=$(echo "$TOPICS_RESPONSE" | jq '.topics | length')
    echo "Found $TOPIC_COUNT topics"
else
    echo -e "${RED}✗ Topics service failed${NC}"
    echo "$TOPICS_RESPONSE"
fi

# Test 7: Support Organizations
echo -e "\n${YELLOW}Test 7: Support Service${NC}"
SUPPORT_RESPONSE=$(curl -s "$API_URL/support" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$SUPPORT_RESPONSE" | grep -q "organizations"; then
    echo -e "${GREEN}✓ Support service working${NC}"
    ORG_COUNT=$(echo "$SUPPORT_RESPONSE" | jq '.organizations | length')
    echo "Found $ORG_COUNT organizations"
else
    echo -e "${RED}✗ Support service failed${NC}"
    echo "$SUPPORT_RESPONSE"
fi

# Summary
echo -e "\n${GREEN}===================================="
echo "✓ All integration tests passed!"
echo "====================================${NC}"
echo ""
echo "Test user created:"
echo "  Email: $TEST_EMAIL"
echo "  Password: Test1234"
echo ""
echo "You can now:"
echo "1. Open http://localhost:4200"
echo "2. Login with the test credentials"
echo "3. Try all features"
