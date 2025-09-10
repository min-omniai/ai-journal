# 📌 OS별 대표 패키지 매니저

## 📍 macOS

### Homebrew (추천)
- **설명**: macOS용 가장 인기 있는 패키지 매니저
- **특징**: 최신 버전 유지, 개발자 도구 풍부
- **설치**: 
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- **기본 명령어**:
  - 설치: `brew install [패키지명]`
  - 삭제: `brew uninstall [패키지명]`
  - 업데이트: `brew update && brew upgrade`
  - 목록 확인: `brew list`

### MacPorts
- **설명**: 포트 시스템 기반
- **특징**: 소스 컴파일, 안정성 중시
- **용도**: 서버/연구용 환경

---

## 📍 Windows

### Chocolatey (추천)
- **설명**: Windows용 가장 많은 패키지 보유
- **특징**: 9천개+ 패키지, GUI 지원
- **설치**: PowerShell 관리자 권한으로 실행
  ```powershell
  Set-ExecutionPolicy Bypass -Scope Process -Force
  iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
  ```
- **기본 명령어**:
  - 설치: `choco install [패키지명]`
  - 삭제: `choco uninstall [패키지명]`
  - 업데이트: `choco upgrade all`
  - 목록 확인: `choco list --local-only`

### Winget (MS 공식)
- **설명**: 마이크로소프트 공식 패키지 매니저
- **특징**: Windows 10/11 기본 내장, 안전성
- **기본 명령어**:
  - 설치: `winget install [패키지명]`
  - 삭제: `winget uninstall [패키지명]`
  - 업데이트: `winget upgrade --all`
  - 검색: `winget search [패키지명]`

### Scoop
- **설명**: 포터블 앱 중심
- **특징**: 깔끔한 설치, 개발자 도구 특화
- **기본 명령어**:
  - 설치: `scoop install [패키지명]`
  - 삭제: `scoop uninstall [패키지명]`

---

## 📍 Linux

### Ubuntu/Debian - APT
- **설명**: 데비안 계열 기본 패키지 매니저
- **특징**: 안정성 중시, 의존성 관리 우수
- **기본 명령어**:
  - 설치: `sudo apt install [패키지명]`
  - 삭제: `sudo apt remove [패키지명]`
  - 업데이트: `sudo apt update && sudo apt upgrade`
  - 검색: `apt search [패키지명]`

### CentOS/RHEL - YUM/DNF
- **설명**: 레드햇 계열 패키지 매니저
- **특징**: 기업용 환경, 롱텀 지원
- **기본 명령어**:
  - 설치: `sudo dnf install [패키지명]` (최신) 또는 `sudo yum install [패키지명]` (구버전)
  - 삭제: `sudo dnf remove [패키지명]`
  - 업데이트: `sudo dnf update`

### Arch Linux - Pacman
- **설명**: 아치 리눅스 전용
- **특징**: 최신 패키지, 빠른 성능
- **기본 명령어**:
  - 설치: `sudo pacman -S [패키지명]`
  - 삭제: `sudo pacman -R [패키지명]`
  - 업데이트: `sudo pacman -Syu`

### openSUSE - Zypper
- **설명**: 오픈수세 전용
- **특징**: 의존성 해결 우수
- **기본 명령어**:
  - 설치: `sudo zypper install [패키지명]`
  - 삭제: `sudo zypper remove [패키지명]`
  - 업데이트: `sudo zypper update`

---

## 📍 언어별 패키지 매니저

### Node.js
- **npm**: 기본 패키지 매니저
- **yarn**: 페이스북 개발, 속도 개선
- **pnpm**: 디스크 공간 절약

### Python
- **pip**: 기본 패키지 매니저
- **conda**: 과학 컴퓨팅 특화

### PHP
- **Composer**: 의존성 관리 도구

### Ruby
- **gem**: 루비 젬 관리
- **bundler**: 프로젝트 의존성 관리

---

## 📍 선택 기준

| 우선순위 | 기준 | 고려사항 |
|---|---|---|
| 1 | **OS 호환성** | 내 운영체제에서 잘 작동하는가 |
| 2 | **패키지 수량** | 필요한 소프트웨어가 있는가 |
| 3 | **업데이트 주기** | 정기적으로 관리되는가 |
| 4 | **커뮤니티** | 문제 해결 자료가 많은가 |
| 5 | **안정성** | 버그나 보안 이슈가 적은가 |

## 추천 조합

### 개발자용
- **macOS**: Homebrew + npm + pip
- **Windows**: Chocolatey + npm + pip
- **Linux**: 배포판 기본 + npm + pip

### 서버 관리자용
- **Ubuntu**: apt + Docker
- **CentOS**: dnf + Docker
- **macOS**: Homebrew + Docker

---

## ✅ 체크리스트
- [ ] 내 OS 확인 완료
- [ ] 해당 OS 대표 패키지 매니저 파악
- [ ] 설치 명령어 숙지
- [ ] 기본 사용법 테스트

**다음 단계**: 선택한 패키지 매니저 설치 및 첫 패키지 설치 실습
