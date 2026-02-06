#!/bin/bash
# Final execution script – Build, Test, Deploy AMNE-Engine

set -e

echo "════════════════════════════════════════════════════════════════════════"
echo "AMNE-ENGINE DOCKER DEPLOYMENT – FINAL EXECUTION"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# === STAGE 1: Validation ===
echo "📋 STAGE 1: Pre-deployment validation..."
echo ""

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi
echo "✓ requirements.txt exists"

if [ ! -f "main.py" ]; then
    echo "❌ main.py not found"
    exit 1
fi
echo "✓ main.py exists"

if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found"
    exit 1
fi
echo "✓ Dockerfile exists"

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi
echo "✓ docker-compose.yml exists"

if [ ! -d "amne" ]; then
    echo "❌ amne/ directory not found"
    exit 1
fi
echo "✓ amne/ directory exists"

if [ ! -d "frontend" ]; then
    echo "❌ frontend/ directory not found"
    exit 1
fi
echo "✓ frontend/ directory exists"

echo ""
echo "✅ Pre-deployment validation passed"
echo ""

# === STAGE 2: Environment Setup ===
echo "⚙️  STAGE 2: Environment setup..."
echo ""

if [ ! -f ".env" ]; then
    echo "⚠️  .env not found, creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ .env created from .env.example"
        echo "⚠️  IMPORTANT: Update GEMINI_API_KEY in .env before deployment"
    else
        cat > .env << 'EOF'
GEMINI_API_KEY=sk-test-placeholder
PYTHONUNBUFFERED=1
PORT=8000
ENVIRONMENT=production
EOF
        echo "✓ .env created with defaults"
    fi
else
    echo "✓ .env exists"
fi

echo ""

# === STAGE 3: Docker Build ===
echo "🔨 STAGE 3: Building Docker image..."
echo ""

# Check Docker daemon
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon not responding. Start Docker and try again."
    exit 1
fi

echo "Building image (this may take 1-2 minutes)..."
docker build -t amne-engine:latest . --progress=plain

if [ $? -eq 0 ]; then
    echo "✓ Docker image built successfully"
    docker images | grep amne-engine | head -1
else
    echo "❌ Docker build failed"
    exit 1
fi

echo ""

# === STAGE 4: Stop Old Containers ===
echo "🛑 STAGE 4: Cleaning up old containers..."
echo ""

if [ "$(docker ps -q -f name=amne-engine)" ]; then
    echo "Stopping running amne-engine container..."
    docker-compose down 2>/dev/null || docker stop amne-engine 2>/dev/null
    sleep 2
    echo "✓ Stopped"
else
    echo "✓ No running containers to stop"
fi

echo ""

# === STAGE 5: Start Services ===
echo "▶️  STAGE 5: Starting Docker services..."
echo ""

docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✓ Services started"
else
    echo "❌ Failed to start services"
    docker-compose logs
    exit 1
fi

echo ""

# === STAGE 6: Health Check ===
echo "⏳ STAGE 6: Waiting for service to be healthy..."
echo ""

max_attempts=30
attempt=0
healthy=false

while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Service is healthy"
        healthy=true
        break
    fi

    attempt=$((attempt + 1))
    if [ $((attempt % 5)) -eq 0 ]; then
        echo "  Waiting... ($attempt/$max_attempts)"
    fi
    sleep 1
done

if [ "$healthy" = false ]; then
    echo "❌ Service health check failed"
    echo ""
    echo "Recent logs:"
    docker-compose logs amne-engine | tail -20
    exit 1
fi

echo ""

# === STAGE 7: Verification ===
echo "✔️  STAGE 7: Verifying deployment..."
echo ""

# Test API endpoint
echo "Testing /health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✓ Health check passed"
else
    echo "⚠️  Health response: $HEALTH"
fi

# Get compiler status
echo "Fetching compiler status..."
STATUS=$(curl -s http://localhost:8000/api/state)
if echo "$STATUS" | grep -q "compilation_count"; then
    echo "✓ API state endpoint working"
else
    echo "⚠️  State response: $STATUS"
fi

echo ""

# === STAGE 8: Summary ===
echo "════════════════════════════════════════════════════════════════════════"
echo "✅ DEPLOYMENT COMPLETE"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "🌐 ACCESS POINTS:"
echo "   Frontend:      http://localhost:8000"
echo "   API Docs:      http://localhost:8000/docs"
echo "   Health Status: http://localhost:8000/health"
echo "   API State:     http://localhost:8000/api/state"
echo ""
echo "📊 CONTAINER INFO:"
docker ps -f name=amne-engine --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "📋 USEFUL COMMANDS:"
echo "   View logs:     docker-compose logs -f amne-engine"
echo "   Stop service:  docker-compose down"
echo "   Restart:       docker-compose restart"
echo "   Shell:         docker-compose exec amne-engine bash"
echo ""
echo "🔧 CONFIGURATION:"
echo "   Environment:   .env"
echo "   Compose file:  docker-compose.yml"
echo "   Backend:       main.py"
echo "   Frontend:      frontend/index.html"
echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 NEXT STEPS:"
echo "   1. Visit http://localhost:8000 in your browser"
echo "   2. Enter Hebrew text in the input field"
echo "   3. Review compilation results and Gemini analysis"
echo "   4. Check logs: docker-compose logs -f"
echo ""
