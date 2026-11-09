# Git 컨벤션

## 브랜치

| 브랜치 | 용도 | 생성 기준 | 병합 대상 |
| --- | --- | --- | --- |
| `main` | 배포 가능한 코드 | - | - |
| `develop` | 개발 내용 통합 | `main` | - |
| `feat/기능명` | 기능 개발 | `develop` | `develop` |
| `fix/수정명` | 일반 버그 수정 | `develop` | `develop` |
| `release/버전` | 배포 준비 및 검증 | `develop` | `develop` |
| `hotfix/수정명` | 배포된 코드의 긴급 수정 | `main` | `main`, `develop` |

브랜치 이름은 영문 소문자와 하이픈을 사용한다.

```text
feat/user-login
fix/login-validation
release/1.0.0
hotfix/login-error
```

`main`과 `develop`에는 직접 커밋하지 않고 PR을 통해 병합한다.

## 커밋 메시지

```text
타입: 변경 내용
```

| 타입 | 용도 |
| --- | --- |
| `feat` | 기능 추가 |
| `fix` | 버그 수정 |
| `refactor` | 기능 변경 없는 코드 구조 개선 |
| `docs` | 문서 변경 |
| `test` | 테스트 추가 또는 수정 |
| `chore` | 설정, 의존성 등 기타 작업 |
| `style` | 코드 동작에 영향을 주지 않는 형식 변경 |

```text
feat: 사용자 로그인 기능 추가
fix: 로그인 비밀번호 검증 오류 수정
chore: PostgreSQL 및 Flyway 설정 추가
docs: 백엔드 실행 방법 추가
```

- 하나의 커밋에는 가능한 한 하나의 의미 있는 변경을 담는다.
- 메시지는 무엇을 변경했는지 구체적으로 작성한다.
- 비밀번호, API 키, `.env` 파일은 커밋하지 않는다.

## Pull Request

PR 제목은 커밋 메시지와 같은 형식을 사용한다. 본문에는 변경 내용과 검증 결과를 작성한다.

```markdown
## 변경 내용
- 변경한 기능이나 설정

## 검증 결과
- 실행하거나 테스트한 내용과 결과
- 확인하지 못한 항목
```

PR을 올리기 전 변경 파일과 실행 결과를 확인하고, 병합 후 작업 브랜치를 삭제한다.
