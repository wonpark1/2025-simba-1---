document.addEventListener("DOMContentLoaded", () => {
  const nickI = document.getElementById("nickname");
  const okBtn = document.getElementById("completeBtn");

  const test = () => {
    const filled = nickI.value.trim() !== "";
    okBtn.disabled = !filled;
    okBtn.classList.toggle("active", filled);
  };

  nickI.addEventListener("input", test);
  test(); //초기화

  document.getElementById("nickform").addEventListener("submit", (e) => {
    if (okBtn.disabled) e.preventDefault(); //버튼이 비활성화일 떄 막기
  });
});
