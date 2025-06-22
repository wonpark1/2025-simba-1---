// static/accounts/js/signup1.js
document.addEventListener("DOMContentLoaded", () => {
  const idInput = document.getElementById("username");
  const pwInput = document.getElementById("password");
  const confirmInput = document.getElementById("confirm");
  const nextBtn = document.getElementById("nextBtn");
  const pwGuide = document.getElementById("password_textcontainer");
  const pwError = document.getElementById("password_error");
  const confirmError = document.getElementById("confirm_error");

  const pwRule = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^\w\s]).{8,20}$/;

  function validate() {
    const idFilled = idInput.value.trim() !== "";
    const pwFilled = pwInput.value.trim();
    const confirmFilled = confirmInput.value.trim();

    /* 형식 검사 */
    const pwValid = pwRule.test(pwFilled);
    pwGuide.style.display = pwFilled ? "none" : "block";
    pwError.style.display = pwFilled && !pwValid ? "block" : "none";

    /* 일치 검사 */
    const pwMatch = pwFilled && confirmFilled && pwFilled === confirmFilled;
    confirmError.style.display = confirmFilled && !pwMatch ? "block" : "none";

    /* 버튼 on/off */
    const canSubmit = idFilled && pwValid && pwMatch;
    nextBtn.disabled = !canSubmit;
    nextBtn.classList.toggle("active", canSubmit);
  }

  /* 이벤트 */
  [idInput, pwInput, confirmInput].forEach((el) =>
    el.addEventListener("input", validate)
  );

  document.querySelector(".form").addEventListener("submit", (e) => {
    if (nextBtn.disabled) e.preventDefault();
  });
});
