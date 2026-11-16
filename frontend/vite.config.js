import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // 개발 서버(localhost:5173)로 들어온 /api 요청을 백엔드(localhost:8080)로 대신 전달합니다.
    // 브라우저 입장에서는 같은 주소로 요청하는 것이라 CORS 에러가 나지 않습니다.
    // 예: fetch('/api/users')  →  http://localhost:8080/api/users
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
})
