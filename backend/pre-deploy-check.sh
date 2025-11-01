#!/usr/bin/env bash
# Lexsy Backend - Pre-Deployment Checklist
# Run this locally before deploying to catch issues early

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Pre-Deployment Checklist for Lexsy Backend"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to print check result
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Check if requirements.txt exists
echo "📦 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    check_pass "requirements.txt exists"
else
    check_fail "requirements.txt not found!"
fi

# 2. Check if app.py exists
echo "🐍 Checking Flask app..."
if [ -f "app.py" ]; then
    check_pass "app.py exists"
else
    check_fail "app.py not found!"
fi

# 3. Check if services directory exists
if [ -d "services" ]; then
    check_pass "services/ directory exists"
else
    check_fail "services/ directory not found!"
fi

# 4. Check if .env.example or .env exists (should NOT commit .env)
echo "🔐 Checking environment configuration..."
if [ -f ".env" ]; then
    check_warn ".env file exists - Make sure it's in .gitignore!"
fi

if [ -f ".gitignore" ]; then
    if grep -q ".env" .gitignore 2>/dev/null; then
        check_pass ".env is in .gitignore"
    else
        check_warn ".env should be in .gitignore"
    fi
fi

# 5. Check if build.sh exists and is executable
echo "🔨 Checking build scripts..."
if [ -f "build.sh" ]; then
    check_pass "build.sh exists"
    if [ -x "build.sh" ]; then
        check_pass "build.sh is executable"
    else
        check_fail "build.sh is not executable (run: chmod +x build.sh)"
    fi
else
    check_fail "build.sh not found!"
fi

# 6. Check critical Python files
echo "📄 Checking service files..."
for file in "services/ai_service.py" "services/document_processor.py" "services/firebase_auth.py" "services/placeholder_detector.py"; do
    if [ -f "$file" ]; then
        check_pass "$file exists"
    else
        check_fail "$file not found!"
    fi
done

# 7. Check if critical dependencies are in requirements.txt
echo "🔍 Checking critical dependencies in requirements.txt..."
for dep in "flask" "gunicorn" "groq" "python-docx" "flask-cors"; do
    if grep -qi "^$dep" requirements.txt 2>/dev/null; then
        check_pass "$dep in requirements.txt"
    else
        check_fail "$dep missing from requirements.txt!"
    fi
done

# 8. Check Python syntax (if Python is available)
if command -v python3 &> /dev/null; then
    echo "🐍 Checking Python syntax..."
    if python3 -m py_compile app.py 2>/dev/null; then
        check_pass "app.py has valid Python syntax"
    else
        check_fail "app.py has syntax errors!"
    fi
else
    check_warn "Python not available to check syntax"
fi

# 9. Check if firebase-service-account.json exists (if using Firebase)
echo "🔥 Checking Firebase configuration..."
if [ -f "firebase-service-account.json" ]; then
    check_warn "firebase-service-account.json found - Ensure it's in .gitignore!"
    if grep -q "firebase-service-account.json" .gitignore 2>/dev/null; then
        check_pass "firebase-service-account.json is in .gitignore"
    else
        check_fail "firebase-service-account.json should be in .gitignore!"
    fi
else
    check_warn "firebase-service-account.json not found (OK if using env vars)"
fi

# 10. Check if sensitive files are properly ignored
echo "🔒 Checking .gitignore..."
if [ -f ".gitignore" ]; then
    check_pass ".gitignore exists"
    
    # Check for critical entries
    for entry in "venv/" "__pycache__/" "*.pyc" "uploads/" "processed/" ".env"; do
        if grep -q "$entry" .gitignore 2>/dev/null; then
            check_pass "$entry is in .gitignore"
        else
            check_warn "$entry should be in .gitignore"
        fi
    done
else
    check_fail ".gitignore not found!"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Pre-Deployment Check Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"
echo -e "${RED}Failed: $CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All critical checks passed! Ready to deploy.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Commit and push to GitHub: git push origin main"
    echo "  2. Deploy on Render dashboard"
    echo "  3. Set environment variables in Render"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix them before deploying.${NC}"
    exit 1
fi

