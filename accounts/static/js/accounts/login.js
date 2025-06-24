document.addEventListener("DOMContentLoaded", () => {
    
  const inputFields = document.querySelectorAll(".input_field");
  const idInp = document.getElementById("username");
  const pwInp = document.getElementById("password");
  const btn = document.getElementById("loginBtn");
  const errorExists = document.querySelector("span[style*='color:red']");

  
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


  // 비밀번호 표시 토글
  document.querySelectorAll('.toggle-icon').forEach(icon => {
    icon.addEventListener('click', () => {
      const input = icon.previousElementSibling;
      const def = icon.dataset.defaultIcon;
      const tog = icon.dataset.toggleIcon;
      if (input.type === 'password') { input.type = 'text'; icon.src = tog; }
      else { input.type = 'password'; icon.src = def; }
    });
  });


  //로그인 버튼 활성화
  const validate = () => {
    const ok = idInp.value.trim() !== "" && pwInp.value.trim() !== "";
    btn.disabled = !ok; //조건 만족안되면 비활성화
    btn.classList.toggle("active", ok); //조건만족하면 주황색으로 active
  };
  [idInp, pwInp, btn].forEach((el) => el.addEventListener("input", validate));
  validate(); // 최초 1회 //여기에서 btn 삭제?

  document.getElementById("loginForm").addEventListener("submit", (e) => {
    if (btn.disabled) e.preventDefault();
  });


  // 에러 메시지가 존재하면 input field에 에러 스타일 적용
  if (errorExists) { 
    inputFields.forEach((field) => {
      field.classList.add('error');
      const img = field.querySelector("img.clear_btn");
      if (img) {
        img.src = "/static/icons/account_alert.svg";
      }
    });
  } 
  
  
  // 에러 없을 때 inputField 스타일 기본 제거
    const clearError = () => {
      inputFields.forEach((field) => {
        field.classList.remove('error');

        const img = field.querySelector('img.clear_btn', 'img.toggle-icon');

        if (img) {
        const defaultIcon = img.dataset.defaultIcon;
        img.src = defaultIcon || "/static/icons/account_default.svg";
      }
     });


  // 에러메시지 숨기기
    if (errorExists) {
      errorExists.style.display = "none";
      }
    };



  // 한 번만 에러 제거하도록 설정 (focus 시)
  [idInp, pwInp].forEach((input) => {
    input.addEventListener("focus", clearError, { once: true }); // 딱 1번만 실행
  });

  // form 제출 전에 에러 메시지 숨기기
  document.getElementById("loginForm").addEventListener("submit", (e) => {
    if (btn.disabled) {
      e.preventDefault();
    } else {
      if (errorMsg) errorMsg.style.display = "none";
    }
    
  });

      
});