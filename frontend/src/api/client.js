// 백엔드 API를 호출하는 공통 함수가 모여 있는 파일입니다.
// 모든 요청이 이 함수를 거치게 하면, 주소/헤더/에러 처리를 한 곳에서 관리할 수 있습니다.

// .env 파일의 VITE_API_BASE_URL 값을 사용하고, 없으면 '/api'를 기본값으로 씁니다.
// (Vite에서는 이름이 VITE_로 시작하는 환경변수만 프론트 코드에서 읽을 수 있습니다.)
const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * 백엔드에 요청을 보내고 JSON 응답을 돌려줍니다.
 *
 * 사용 예:
 *   const users = await request('/users')
 *   const created = await request('/users', { method: 'POST', body: { name: 'kim' } })
 *
 * @param {string} path - '/users' 처럼 BASE_URL 뒤에 붙는 경로
 * @param {object} options - method, body, headers 등 fetch 옵션
 */
export async function request(path, { method = 'GET', body, headers = {}, ...rest } = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      // body가 있을 때만 JSON 형식이라고 알려줍니다.
      ...(body !== undefined && { 'Content-Type': 'application/json' }),
      ...headers,
    },
    // JS 객체는 그대로 보낼 수 없어서 JSON 문자열로 바꿔서 보냅니다.
    body: body !== undefined ? JSON.stringify(body) : undefined,
    ...rest,
  })

  // fetch는 404, 500 같은 에러 응답이어도 예외를 던지지 않습니다.
  // 그래서 response.ok(상태코드 200~299 여부)를 직접 확인해서 에러를 던집니다.
  if (!response.ok) {
    const message = await response.text()
    throw new Error(`API 요청 실패 (${response.status}): ${message}`)
  }

  // 204 No Content처럼 응답 본문이 없는 경우를 처리합니다.
  if (response.status === 204) {
    return null
  }

  const contentType = response.headers.get('Content-Type') || ''
  return contentType.includes('application/json') ? response.json() : response.text()
}
