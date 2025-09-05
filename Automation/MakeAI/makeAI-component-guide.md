# Make AI — Component Guide
_작성일: 2025-08-28 · 정리 목적: 내가 실제 시나리오에서 활용한 Make 컴포넌트의 쓰임새, 사용처, 활용방법 정리_

---

## 1) Iterator
**쓰임새**: 배열을 항목별로 쪼개 단일 아이템 단위로 처리.  
**사용처**: 정규식으로 추출한 여러 이미지 URL을 개별 검증 후 재집계.  
**활용방법**:  
- Input: `images[]`  
- Output: 개별 `image_url` → 다음 모듈로 전달  
- 패턴: **Iterator → (필터/정규화) → Array Aggregator**  

**세부 설명**
| 항목 | 내용 |
|---|---|
| 입력 구조 | 배열(any[]) |
| 출력 구조 | 단일 요소(each item) |
| 주요 활용 | 이미지 URL, 문장 리스트, JSON 배열 |
| 흔한 오류 | 빈 배열 → 실행 실패 |
| 해결 | Filter로 length 체크 / Null-safe 경로 추가 |

---

## 2) Array Aggregator
**쓰임새**: Iterator에서 분리된 데이터를 다시 배열로 합침.  
**사용처**: Buffer 업로드용 `images[]`, 불릿 리스트 등.  
**활용방법**:  
- Target structure = `images[]`  
- Source = Iterator 출력  
- 최대 개수 제한 = 4  
- 중복 제거 = 해시/정규화 사용  

**세부 설명**
| 항목 | 내용 |
|---|---|
| 입력 구조 | 단일 값 스트림 |
| 출력 구조 | 배열(array[]) |
| 주요 활용 | 이미지 묶기, 포인트 리스트 만들기 |
| 흔한 오류 | 중복 포함, 정렬 불일치 |
| 해결 | Set Variable로 unique 처리, 정렬 규칙 적용 |

---

## 3) Set Variable
**쓰임새**: 문자열/JSON을 가공하고 새로운 변수를 생성.  
**사용처**: 이미지 URL 추출, 공백 제거, 해시 생성.  
**활용방법**:  
- Regex 추출 + 캡처 그룹 지정  
- Query 파라미터 제거  
- lower() 등 함수 적용 후 해시 생성  

**세부 설명**
| 항목 | 내용 |
|---|---|
| 입력 | 텍스트, JSON |
| 출력 | 새로운 변수(string, number, array 등) |
| 주요 활용 | Regex 추출, 해시 키 생성, 기본값 지정 |
| 흔한 오류 | 캡처 그룹 인덱스 혼동 |
| 해결 | `Matches[*].Groups[1]` 패턴 고정, Iterator와 조합 |

**예시 Regex**
```regex
<img[^>]+src=["'](https?:\/\/[^"']+\.(?:jpg|jpeg|png|gif|webp))["']
<meta[^>]+property=["']og:image["'][^>]*content=["'](https?:\/\/[^"']+)["']
```

---

## 4) Filter
**쓰임새**: 조건을 만족할 때만 다음 모듈 실행. 흐름 제어의 핵심.  
**사용처**: 이미지 없는 경우 텍스트-only 플로우, 중복 URL 차단.  
**활용방법**:  
- 조건식 예시: `length(images[]) > 0`, `not exists(url_hash)`  

**세부 설명**
| 항목 | 내용 |
|---|---|
| 입력 | 조건식(boolean) |
| 출력 | true → 다음 모듈 실행 / false → 차단 |
| 주요 활용 | 데이터 유효성 체크, 중복 방지, 분기 제어 |
| 흔한 오류 | 타입 불일치(숫자 vs 문자열) |
| 해결 | 변환 함수 적용(toNumber, toString 등) |

**조건 예시**
- 이미지 업로드 분기: `length(images[]) > 0`  
- 중복 방지: `not exists(url_hash)`  
- 특정 키워드 포함 여부: `contains(title, "AI")`  

---

## 5) Data Store
**쓰임새**: 중복 차단 및 간단한 상태 저장.  
**사용처**: 같은 URL의 중복 업로드 방지, 게시 메타데이터 기록.  
**활용방법**:  
- Key = `url_hash`  
- Value = `{ posted_at, channel, images_count }`  

**세부 설명**
| 항목 | 내용 |
|---|---|
| 입력 | Key, Value |
| 출력 | 저장된 객체 |
| 주요 활용 | 중복 방지, 상태 관리 |
| 흔한 오류 | 해시 충돌, Key 포맷 불일치 |
| 해결 | 정규화 규칙 고정(소문자, query 제거) |

---

## 6) HTTP (요청 모듈)
**쓰임새**: 외부 API/웹 리소스를 호출해 데이터 가져오기.  
**사용처**: RSS에 없는 원문 HTML 확보, 이미지/메타데이터 요청.  

**메서드 종류**
| 메서드 | 용도 | 활용 예시 |
|---|---|---|
| GET | 리소스 조회 | 기사 원문 HTML 가져오기 |
| POST | 데이터 전송 | 외부 요약 API 호출 |
| PUT | 데이터 수정 | 외부 DB 업데이트 |
| DELETE | 데이터 삭제 | 외부 리소스 제거 |

**대표 설정**
- URL: `{{1.url}}`  
- Headers: `Content-Type: application/json`  
- Body: JSON, form-data 등 선택 가능  

**흔한 오류/해결**
- 차단/리다이렉트 → 스킵 후 RSS summary 사용  
- 인증 실패 → API Key 환경변수 사용  

---

## 7) LLM 모듈 (Perplexity / Claude)
**쓰임새**: 뉴스 본문 요약 → 한국어 스레드 변환.  
**사용처**: RSS/HTML 텍스트를 입력받아 스레드 글 규칙에 맞게 포맷.  
**활용방법**:  
- Prompt = `thread_writer_v3.md`  
- Input = `{title, url, published_at, clean_text, images[]}`  
- Output = `post_text`, `comment_text` (--- 분리)  

**세부 설명**
| 항목 | 내용 |
|---|---|
| 입력 | 원문 텍스트, 메타데이터 |
| 출력 | 스레드 글(본문, 댓글) |
| 주요 활용 | 한국어 요약, 존댓말 변환, 불릿 강조 |
| 흔한 오류 | 길이 초과, --- 분리 누락 |
| 해결 | Prompt에 규칙 명시, 280자 제한 적용 |

---

## 8) Formatter (텍스트 정리)
**쓰임새**: 텍스트 가공(길이, 공백, 특수문자 제거).  
**사용처**: 280자 컷, 링크 정리.  
**활용방법**:  
- 트림(trim), replace, substring 등 함수 활용  
- URL 축약기로 긴 링크 처리  

**체크리스트**
- [ ] 말줄임은 문장 단위 컷  
- [ ] 링크는 깨지지 않도록 축약/정리  

---

## 베스트 프랙티스 (요약)
- **Iterator → Array Aggregator** 순서 고정.  
- 이미지: 최대 4장, 실패 시 1장 폴백 → 최종은 텍스트-only.  
- **Data Store**로 멱등성(동일한 연산을 여러 번 적용해도 결과가 처음과 달라지지 않는 성질) 보장.  
- **Filter**로 각 분기 안전하게 제어.  
- **HTTP** 요청은 실패해도 폴백 경로 유지.  
