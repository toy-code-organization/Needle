import { useState } from 'react'
import Button from '../components/Button.jsx'

// Home 페이지 컴포넌트입니다.
function Home() {
  // useState: 컴포넌트가 기억하는 값(상태)을 만듭니다.
  // count는 현재 값, setCount는 값을 바꾸는 함수입니다.
  // setCount로 값을 바꾸면 React가 화면을 자동으로 다시 그립니다(리렌더링).
  const [count, setCount] = useState(0)

  const handleIncrease = () => {
    setCount(count + 1)
  }

  const handleReset = () => {
    setCount(0)
  }

  return (
    <main style={{ padding: '32px' }}>
      <h1>Needle</h1>
      <p>버튼을 클릭한 횟수: {count}</p>

      {/* 같은 Button 컴포넌트를 props만 바꿔서 두 번 재사용합니다. */}
      <div style={{ display: 'flex', gap: '8px' }}>
        <Button label="+1 올리기" onClick={handleIncrease} />
        <Button label="초기화" onClick={handleReset} />
      </div>
    </main>
  )
}

export default Home
