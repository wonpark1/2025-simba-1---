/* ===== 회원가입 1단계 : 클라이언트 검증 ===== */
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
    const idOK = idI.value.trim() !== "";

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

  [idI, pwI, cfI].forEach((el) => el.addEventListener("input", validate));
  validate(); // 최초 1회

  document.getElementById("signupForm").addEventListener("submit", (e) => {
    if (nxt.disabled) e.preventDefault();
  });
});
