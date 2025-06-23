document.addEventListener("DOMContentLoaded", () => {
  const $ = (id) => document.getElementById(id);
  const idI = $("username");
  const pwI = $("password");
  const cfI = $("confirm");
  const nxt = $("nextBtn");

  const pwGuide = $("password_textcontainer");
  const pwErr = $("password_error");
  const cfErr = $("confirm_error");
  const idErr = $("id_error");

  const rule = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^\w\s]).{8,20}$/;

  function validate() {
    const idOK = idI.value.trim() !== "";
    idErr.style.display = idOK && !idUnique ? "block" : "none";

    const pw = pwI.value.trim();
    const pwOK = rule.test(pw);
    pwGuide.style.display = pw ? "none" : "block";
    pwErr.style.display = pw && !pwOK ? "block" : "none";

    const cf = cfI.value.trim();
    const same = pw && cf && pw === cf;
    cfErr.style.display = cf && !same ? "block" : "none";

    const ok = idOK && pwOK && same;
    nxt.disabled = !ok;
    nxt.classList.toggle("active", ok);
  }

  // 이런식으로 분기 처리하는 건 어때요??
  // function validate() {
  //   if (pw) {
  //     if (pw.length < 8){
  //       pwGuide.style.display = "block";
  //       pwErr.stextContent = "비밀번호는 8자 이상이어야 합니다.";
  //     } else if (pw.length > 20){
  //       pwGuide.style.display = "block";
  //       pwErr.textContent = "비밀번호는 20자 이하이어야 합니다.";
  //     } else if (!/[^\w\s]/.test(pw)){
  //       pwGuide.style.display = "block";
  //       pwErr.textContent = "비밀번호는 특수문자를 포함해야 합니다.";
  //     } else {
  //       pwOK = true;
  //     }
  //   }
  // }

  [idI, pwI, cfI].forEach((el) => el.addEventListener("input", validate));
  validate(); // 최초 1회

  document.getElementById("signupForm").addEventListener("submit", (e) => {
    if (nxt.disabled) e.preventDefault();
  });
});
