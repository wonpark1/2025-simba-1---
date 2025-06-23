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
  function validate() {
    const id = idI.value.trim();
    const pw = pwI.value.trim();
    const cf = cfI.value.trim();

    const idOK = id !== "";

    let pwOK = false;
    pwGuide.style.display = pw ? "none" : "block";
    if (!pw) {
      pwErr.style.display = "none";
    } else if (pw.length < 8) {
      pwErr.textContent = "비밀번호는 8자 이상이어야 합니다.";
      pwErr.style.display = "block";
    } else if (pw.length > 20) {
      pwErr.textContent = "비밀번호는 20자 이하이어야 합니다.";
      pwErr.style.display = "block";
    } else if (!/[!@#$%^&*()_\-+={[}\]|\\:;"'<>,.?/]/.test(pw)) {
      pwErr.textContent = "비밀번호는 특수문자를 포함해야 합니다.";
      pwErr.style.display = "block";
    } else if (!rule.test(pw)) {
      pwErr.textContent = "영문과 숫자를 모두 포함해야 합니다.";
      pwErr.style.display = "block";
    } else {
      pwOK = true;
      pwErr.style.display = "none";
    }

    const same = pwOK && cf && pw === cf;
    cfErr.style.display = cf && !same ? "block" : "none";

    const ok = idOK && pwOK && same;
    nxt.disabled = !ok;
    nxt.classList.toggle("active", ok);
  }
  [idI, pwI, cfI].forEach((el) => el.addEventListener("input", validate));
  validate(); // 최초 1회

  document.getElementById("signupForm").addEventListener("submit", (e) => {
    if (nxt.disabled) e.preventDefault();
  });
});
