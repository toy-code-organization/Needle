# API 명세

원본: [PJT Needle API 명세](https://app.notion.com/p/414e1f6a336e8044bcf0cf48d0407a4f)

Notion 데이터베이스에 기록된 설계 초안이며 실제 구현 여부는 별도 확인이 필요합니다.

## 배정 업무 목록 조회

- 메서드: `GET`
- 경로: `/api/employees/{employeeId}/task-assignments`
- 사용자: 유저
- 카테고리: 온보딩
- 파라미터: employeeId: 사원 ID
- 설명: 사원에게 배정된 업무와 기한, 변경 여부 조회
- 기타: 설계 초안; 테스트용 사원 식별, 인증·인가 추후 적용
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e8008820bf5b718850e4f)

### Request

<table header-row="true">
<colgroup>
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
</colgroup>
<tr>
<td>
key
</td>
<td>
설명
</td>
<td>
value 타입
</td>
<td>
옵션
</td>
<td>
Nullable
</td>
<td>
예시
</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

**Query parameter**



### Response

<table header-row="true">
<colgroup>
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
<col width="114.83333333333333" />
</colgroup>
<tr>
<td>
key
</td>
<td>
설명
</td>
<td>
value 타입
</td>
<td>
옵션
</td>
<td>
Nullable
</td>
<td>
예시
</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

**Example**

```javascript
{
		"code": 200,
		"message": "요청이 성공적으로 처리되었니다",
		"data": {
				
		}
}
```

### Status

| status | response content |
| --- | --- |
| 200 |  |
| 400 |  |

### API 설계 초안

### 요청

`GET /api/employees/{employeeId}/task-assignments`

- `employeeId`: 테스트용 사원 번호. 로그인 도입 후 서버의 사용자 식별과 권한 확인이 필요합니다.
- 요청 본문 없음.

### 응답 예시: 200 OK

```json
{
  "employeeId": 1,
  "assignments": [
    {
      "assignmentId": 100,
      "taskId": 10,
      "title": "개발 환경 설정",
      "dueAt": "2026-11-20T09:00:00Z",
      "hasChanges": true
    }
  ]
}
```

- 배정된 업무가 없으면 `assignments`는 빈 배열입니다.
- `dueAt`은 없을 수 있습니다. 아직 상세를 열지 않은 배정은 `hasChanges`가 `false`입니다.
- 목록 조회는 확인 기준을 변경하지 않습니다.

### 오류

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 사원을 찾을 수 없음

구현 전 설계 초안입니다.

## 참고 자료 수정

- 메서드: `PATCH`
- 경로: `/api/references/{referenceId}`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: referenceId: 참고 자료 ID
- 설명: 공유 참고 자료의 제목 또는 설명 수정
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e81339c8dc2eef519099d)

### Request

`PATCH /api/references/{referenceId}`

```json
{"description":"새 실행 방법: https://example.com/new-guide"}
```

### Response

성공 응답 형식 및 상태 코드는 미확정.

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

변경은 연결된 모든 업무에 반영되며, 각 배정자의 마지막 확인 내용과 비교한다.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 업무 등록

- 메서드: `POST`
- 경로: `/api/tasks`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: 없음
- 설명: 공통 업무 생성
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e8149a342e8b78c1557ac)

### Request

`POST /api/tasks`

```json
{"title":"개발 환경 설정","description":"프로젝트를 내려받고 백엔드를 실행합니다.","completionCriteria":"헬스 체크가 정상 응답합니다."}
```

### Response

201 Created 예시:

```json
{"id":10,"title":"개발 환경 설정","description":"프로젝트를 내려받고 백엔드를 실행합니다.","completionCriteria":"헬스 체크가 정상 응답합니다."}
```

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

업무 내용은 배정된 사원에게 공통으로 제공된다.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 참고 자료 상세 조회

- 메서드: `GET`
- 경로: `/api/references/{referenceId}`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: referenceId: 참고 자료 ID
- 설명: 공유 참고 자료의 제목과 설명 조회
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e81859e3dc64b51ac2eb0)

### Request

`GET /api/references/{referenceId}`

요청 본문 없음.

### Response

200 OK. 응답 상세 형식은 설계 시 확정.

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

존재하지 않는 자료는 404.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 업무 상세 조회

- 메서드: `GET`
- 경로: `/api/tasks/{taskId}`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: taskId: 업무 ID
- 설명: 관리자가 공통 업무의 상세 정보 조회
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e8187a5d8e29f13062a0b)

### Request

`GET /api/tasks/{taskId}`

요청 본문 없음.

### Response

200 OK. 응답 상세 형식은 설계 시 확정.

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

존재하지 않는 업무는 404.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 사원에게 업무 배정

- 메서드: `POST`
- 경로: `/api/tasks/{taskId}/assignments`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: taskId: 업무 ID
- 설명: 사원에게 업무 배정 및 선택적 기한 설정
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e8196afabd551fe67daaa)

### Request

`POST /api/tasks/{taskId}/assignments`

```json
{"employeeId":1,"dueAt":"2026-11-20T09:00:00Z"}
```

`dueAt`은 생략하거나 null로 전달할 수 있다.

### Response

201 Created 예시:

```json
{"assignmentId":100,"employeeId":1,"taskId":10,"dueAt":"2026-11-20T09:00:00Z"}
```

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

동일 사원과 업무의 중복 배정은 409 Conflict.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 업무 변경 내용 확인

- 메서드: `POST`
- 경로: `/api/task-assignments/{assignmentId}/confirm`
- 사용자: 유저
- 카테고리: 온보딩
- 파라미터: assignmentId: 배정 ID
- 설명: 사용자가 실제로 본 업무 변경 내용을 확인
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e8196afacf3d0b3d2a5a9)

### Request

`POST /api/task-assignments/{assignmentId}/confirm`

```json
{"viewToken":"서버가_발급한_확인용_값"}
```

### Response

204 No Content

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

해당 사원의 확인 기준만 갱신한다. 확인 중 생긴 새 변경은 남긴다. 오래된 확인 요청의 처리와 토큰 방식은 구현 설계 시 확정한다.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 참고 자료 등록

- 메서드: `POST`
- 경로: `/api/references`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: 없음
- 설명: 여러 업무에서 공유할 참고 자료 생성
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e8199bbf2e649535c9b92)

### Request

`POST /api/references`

```json
{"title":"백엔드 실행 안내","description":"실행 방법: https://example.com/guide"}
```

### Response

201 Created 예시:

```json
{"id":30,"title":"백엔드 실행 안내","description":"실행 방법: https://example.com/guide"}
```

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

URL은 description의 텍스트로 저장한다. 첨부파일 저장·업로드 방식은 미확정.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 배정 업무 상세 열기

- 메서드: `POST`
- 경로: `/api/task-assignments/{assignmentId}/open`
- 사용자: 유저
- 카테고리: 온보딩
- 파라미터: assignmentId: 배정 ID
- 설명: 배정 업무의 최신 내용과 마지막 확인 이후 변경 내용을 조회
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e819cae5ed2cd077d0d98)

### Request

`POST /api/task-assignments/{assignmentId}/open`

요청 본문 없음.

### Response

200 OK 예시:

```json
{"assignmentId":100,"task":{"id":10,"title":"개발 환경 설정","description":"프로젝트를 내려받고 백엔드를 실행합니다.","completionCriteria":"헬스 체크가 정상 응답합니다."},"dueAt":"2026-11-20T09:00:00Z","references":[{"id":30,"title":"백엔드 실행 안내","description":"https://example.com/guide"}],"changes":[{"field":"dueAt","before":"2026-11-15T09:00:00Z","after":"2026-11-20T09:00:00Z"}],"viewToken":"서버가_발급한_확인용_값"}
```

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

처음 상세를 열 때 응답한 내용을 확인 기준으로 저장하고 changes는 빈 배열이다. 이후 마지막 확인 값과 현재 값을 비교한다. viewToken의 발급·검증 방식은 미확정.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 업무 내용 수정

- 메서드: `PATCH`
- 경로: `/api/tasks/{taskId}`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: taskId: 업무 ID
- 설명: 공통 업무의 제목, 설명 또는 완료 기준 수정
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e81a2a1e7d8d7f0b9f68d)

### Request

`PATCH /api/tasks/{taskId}`

```json
{"description":"프로젝트를 내려받고 백엔드와 DB를 실행합니다."}
```

### Response

성공 응답 형식 및 상태 코드는 미확정.

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

변경 내용은 해당 업무의 모든 배정자에게 반영되며 사원별 확인 내용과 비교한다.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 업무의 참고 자료 연결 해제

- 메서드: `DELETE`
- 경로: `/api/tasks/{taskId}/references/{referenceId}`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: taskId: 업무 ID; referenceId: 참고 자료 ID
- 설명: 업무와 참고 자료의 연결만 해제
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e81ab9f41cd8b539975d4)

### Request

`DELETE /api/tasks/{taskId}/references/{referenceId}`

요청 본문 없음.

### Response

성공 응답 형식 및 상태 코드는 미확정.

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

공유 참고 자료 자체와 다른 업무의 연결은 삭제하지 않는다. 연결 해제는 변경 비교 대상이다.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 업무에 참고 자료 연결

- 메서드: `PUT`
- 경로: `/api/tasks/{taskId}/references/{referenceId}`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: taskId: 업무 ID; referenceId: 참고 자료 ID
- 설명: 업무와 공유 참고 자료 연결
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e81b5b032cd235b25a429)

### Request

`PUT /api/tasks/{taskId}/references/{referenceId}`

요청 본문 없음.

### Response

204 No Content

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

이미 연결되어 있어도 같은 연결 상태를 유지한다. 연결 추가는 변경 비교 대상이다.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.

## 업무 배정 기한 수정

- 메서드: `PATCH`
- 경로: `/api/task-assignments/{assignmentId}`
- 사용자: 관리자
- 카테고리: 온보딩
- 파라미터: assignmentId: 배정 ID
- 설명: 사원별 업무 기한 추가, 변경 또는 제거
- 기타: 설계 초안 · 미구현
- Notion: [원본 항목](https://app.notion.com/p/414e1f6a336e81cbaa75c0fd20a4997c)

### Request

`PATCH /api/task-assignments/{assignmentId}`

```json
{"dueAt":"2026-11-25T09:00:00Z"}
```

기한 제거: `{"dueAt": null}`

### Response

성공 응답 형식 및 상태 코드는 미확정.

### Status

- `400 Bad Request`: 잘못된 요청
- `404 Not Found`: 대상이 없을 때
- `409 Conflict`: 중복 배정 또는 상태 충돌에 해당하는 경우

### 참고

기한은 시간대가 포함된 시각이다. 기한 변경은 해당 사원에게만 반영된다.

이 문서는 구현 전 API 설계 초안이다. 인증·인가는 추후 설계하며, 테스트용 사용자 식별과 관리 API는 개발 환경에서만 사용한다.
