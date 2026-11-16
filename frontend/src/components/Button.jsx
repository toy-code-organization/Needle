// 재사용 가능한 버튼 컴포넌트입니다.
// props(부모가 넘겨주는 값)로 버튼에 표시할 글자(label)와 클릭 시 실행할 함수(onClick)를 받습니다.
// Button 자체는 상태를 갖지 않고, "무엇을 할지"는 부모가 결정합니다.
function Button({ label, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{ padding: '8px 16px', fontSize: '16px', cursor: 'pointer' }}
    >
      {label}
    </button>
  )
}

export default Button
