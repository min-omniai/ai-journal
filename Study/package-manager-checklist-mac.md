## 📍 한 번에 모든 것 확인하는 스크립트
```bash
#!/bin/bash

echo "🔍 macOS 설치된 패키지 전체 확인"
echo "=================================="

# Homebrew 확인
echo ""
echo "🍺 Homebrew 패키지:"
if command -v brew >/dev/null 2>&1; then
    echo "Formula ($(brew list --formula | wc -l | tr -d ' ')개):"
    brew list --formula | head -10
    if [ $(brew list --formula | wc -l) -gt 10 ]; then
        echo "... (더 많은 패키지가 있습니다. 'brew list --formula' 로 전체 확인)"
    fi
    
    echo ""
    echo "Cask ($(brew list --cask | wc -l | tr -d ' ')개):"
    brew list --cask | head -10
    if [ $(brew list --cask | wc -l) -gt 10 ]; then
        echo "... (더 많은 패키지가 있습니다. 'brew list --cask' 로 전체 확인)"
    fi
else
    echo "❌ Homebrew가 설치되지 않았습니다."
fi

# Python 패키지 확인
echo ""
echo "🐍 Python 패키지:"
if command -v python3 >/dev/null 2>&1; then
    echo "Python 버전: $(python3 --version)"
    
    if command -v pip >/dev/null 2>&1; then
        echo "pip 패키지 ($(pip list | wc -l | tr -d ' ')개):"
        pip list | head -10
        if [ $(pip list | wc -l) -gt 10 ]; then
            echo "... (더 많은 패키지가 있습니다. 'pip list' 로 전체 확인)"
        fi
    fi
    
    if command -v uv >/dev/null 2>&1; then
        echo "uv 버전: $(uv --version)"
    fi
    
    if command -v conda >/dev/null 2>&1; then
        echo "conda 환경: $(conda env list | grep '*' | awk '{print $1}')"
    fi
else
    echo "❌ Python이 설치되지 않았습니다."
fi

# Node.js 패키지 확인
echo ""
echo "📦 Node.js 패키지:"
if command -v node >/dev/null 2>&1; then
    echo "Node.js 버전: $(node --version)"
    
    if command -v npm >/dev/null 2>&1; then
        echo "npm 전역 패키지:"
        npm list -g --depth=0 2>/dev/null | grep -v "npm@" | head -10
    fi
    
    if command -v pnpm >/dev/null 2>&1; then
        echo "pnpm 버전: $(pnpm --version)"
    fi
    
    if command -v yarn >/dev/null 2>&1; then
        echo "yarn 버전: $(yarn --version)"
    fi
else
    echo "❌ Node.js가 설치되지 않았습니다."
fi

# Ruby 패키지 확인
echo ""
echo "💎 Ruby 패키지:"
if command -v ruby >/dev/null 2>&1; then
    echo "Ruby 버전: $(ruby --version)"
    
    if command -v gem >/dev/null 2>&1; then
        echo "gem 패키지 ($(gem list | wc -l | tr -d ' ')개):"
        gem list | head -10
        if [ $(gem list | wc -l) -gt 10 ]; then
            echo "... (더 많은 패키지가 있습니다. 'gem list' 로 전체 확인)"
        fi
    fi
else
    echo "❌ Ruby가 설치되지 않았습니다."
fi

# Java 도구 확인
echo ""
echo "☕ Java 도구:"
if command -v java >/dev/null 2>&1; then
    echo "Java 버전: $(java --version 2>/dev/null | head -1 || java -version 2>&1 | head -1)"
    
    if command -v mvn >/dev/null 2>&1; then
        echo "Maven 버전: $(mvn --version | head -1)"
    fi
    
    if command -v gradle >/dev/null 2>&1; then
        echo "Gradle 버전: $(gradle --version | grep Gradle)"
    fi
else
    echo "❌ Java가 설치되지 않았습니다."
fi

# 기타 도구들
echo ""
echo "🔧 기타 개발 도구:"
if command -v go >/dev/null 2>&1; then
    echo "Go 버전: $(go version)"
fi

if command -v rust >/dev/null 2>&1; then
    echo "Rust 버전: $(rustc --version)"
fi

if command -v php >/dev/null 2>&1; then
    echo "PHP 버전: $(php --version | head -1)"
    if command -v composer >/dev/null 2>&1; then
        echo "Composer 버전: $(composer --version)"
    fi
fi

echo ""
echo "✅ 패키지 확인 완료!"
echo ""
echo "💡 상세 확인 명령어:"
echo "- 전체 Homebrew: brew list"
echo "- 전체 Python: pip list"
echo "- 전체 Node.js: npm list -g --depth=0"
echo "- 전체 Ruby: gem list"
```

---

### 스크립트 저장 및 실행

```bash
# 스크립트를 파일로 저장
curl -o check-packages.sh https://raw.githubusercontent.com/your-repo/check-packages.sh

# 또는 직접 생성
nano check-packages.sh
# (위의 스크립트 내용 복사 붙여넣기)

# 실행 권한 부여
chmod +x check-packages.sh

# 실행
./check-packages.sh
```
