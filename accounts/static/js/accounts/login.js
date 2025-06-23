document.addEventListener("DOMContentLoaded", () => {
    
  
  
  // x 버튼 누르면 input 내용 삭제
    document.querySelectorAll('.clear_btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const targetId = btn.dataset.target;
        const input = document.getElementById(targetId);
        if (input) {
          input.value = '';
          input.dispatchEvent(new Event('input'));
        }
      });
    });


    // inputField 스타일 기본 제거
    inputFields.forEach((field) => {
      field.classList.remove('error', 'success');

      const input = field.querySelector('input');
      const img = field.querySelector('img');

      if (img && input) {
      const defaultIcon = input.dataset.defaultIcon;
      img.src = defaultIcon || "/static/icons/account_default.svg";
      }
    });




  const idInp = document.getElementById("username");
  const pwInp = document.getElementById("password");
  const btn = document.getElementById("loginBtn");

  const validate = () => {
    const ok = idInp.value.trim() !== "" && pwInp.value.trim() !== "";
    btn.disabled = !ok; //조건 만족안되면 비활성화
    btn.classList.toggle("active", ok); //조건만족하면 주황색으로 active
  };
  [idInp, pwInp, btn].forEach((el) => el.addEventListener("input", validate));
  validate(); // 최초 1회

  document.getElementById("loginForm").addEventListener("submit", (e) => {
    if (btn.disabled) e.preventDefault();
  });
});
