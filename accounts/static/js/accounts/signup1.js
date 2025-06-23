document.addEventListener("DOMContentLoaded", () => {
  const $ = (id) => document.getElementById(id);
  const idI = $("username");
  const pwI = $("password");
  const cfI = $("confirm");
  const nxt = $("nextBtn");

  const pwGuide = $("password_textcontainer");
  const pwErr = $("password_error");
  const cfErr = $("confirm_error");

  const rule = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^\w\s]).{8,20}$/;
  const inputFields = document.querySelectorAll('.input_field');

  function validate() {
    const id = idI.value.trim();
    const pw = pwI.value.trim();
    const cf = cfI.value.trim();

    const idOK = id !== "";

    let pwOK = false;
    pwGuide.style.display = pw ? "none" : "block";

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


    //------------아이디-------------//

    // 아이디 입력 시
    if (idOK) {
      inputFields.forEach((field) => {
        const input = field.querySelector('input');
        if (input && input.id === "username") {
          field.classList.add('success');
          const img = field.querySelector('img');
          if (img) img.src = "/static/icons/account_chdeck.svg";
        }
      });
    }


    //-----------비밀번호-------------//

    // 비밀번호 유효성 검사
    if (!pw) {
      pwGuide.textContent = "영어,숫자,특수문자를 포함하여 8-20자 이내로 작성해주세요."
      pwErr.style.display = "none";
    } else if (pw.length < 8) {
      pwErr.textContent = "비밀번호는 8자 이상이어야 합니다.";
      //pwGuide.classList.add("error");
      pwErr.style.display = "block";
    } else if (pw.length > 20) {
      pwErr.textContent = "비밀번호는 20자 이하이어야 합니다.";
      //pwGuide.classList.add("error");
      pwErr.style.display = "block";
    } else if (!/[!@#$%^&*()_\-+={[}\]|\\:;"'<>,.?/]/.test(pw)) {
      pwErr.textContent = "비밀번호는 특수문자를 포함해야 합니다.";
      //pwGuide.classList.add("error");
      pwErr.style.display = "block";
    } else if (!rule.test(pw)) {
      pwErr.textContent = "영문과 숫자를 모두 포함해야 합니다.";
      //pwGuide.classList.add("error");
      pwErr.style.display = "block";
    } else {
      pwOK = true;
      pwGuide.textContent = "사용 가능한 비밀번호입니다.";
      //pwGuide.classList.add("success");
      pwErr.style.display = "none";
    }

    // 비밀번호가 유효하지 않을 경우
    if (pw && !pwOK) {
      inputFields.forEach((field) => {
        const input = field.querySelector('input');
        if (input && input.id === "password") {
          field.classList.add('error');
        }
      });
    }

    // 비밀번호가 유효할 경우
    if (pwOK) {
      inputFields.forEach((field) => {
        const input = field.querySelector('input');
        if (input && input.id === "password") {
          field.classList.add('success');
          const img = field.querySelector("img");
          if (img) img.src = "/static/icons/account_chdeck.svg";
        }
      });
    }


    // 비밀번호 eyeson eyesoff 기능
    const toggleIcons = document.querySelectorAll('.toggle-icon');

    toggleIcons.forEach((icon) => {
      icon.addEventListener('click', () => {
        const input = icon.previousElementSibling;

        const defaultIcon = icon.dataset.defaultIcon;
        const toggleIcon = icon.dataset.toggleIcon;

        if (input.type === "password") {
          input.type = "text";
          icon.src = toggleIcon;
        } else {
          input.type = "password";
          icon.src = defaultIcon;
        }
      });
    });


    //--------비밀번호 확인----------//

    // 비밀번호 일치 여부 검사
    const same = pwOK && cf && pw === cf;
    cfErr.style.display = cf && !same ? "block" : "none";

    const ok = idOK && pwOK && same;
    nxt.disabled = !ok;
    nxt.classList.toggle("active", ok);


    // 비밀번호가 일치하지 않을 경우
    if (cf && !same) {
      inputFields.forEach((field) => {
        const input = field.querySelector('input');
        if (input && input.id === "confirm") {
          field.classList.add('error');
          const img = field.querySelector("img");
          if (img) img.src = "/static/icons/account_alert.svg";
        }
      });
    }

    // 비밀번호가 일치할 경우
    if (same) {
      inputFields.forEach((field) => {
        const input = field.querySelector('input');
        if (input && input.id === "confirm") {
          field.classList.add('success');
          const img = field.querySelector("img");
          if (img) img.src = "/static/icons/account_chdeck.svg";
        }
      });
    }  
    
  }//validate 함수 끝





  [idI, pwI, cfI].forEach((el) => el.addEventListener("input", validate));
  validate(); // 최초 1회

  document.getElementById("signupForm").addEventListener("submit", (e) => {
    if (nxt.disabled) e.preventDefault();
  });
});
