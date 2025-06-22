document.addEventListener("DOMContentLoaded", () => {
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
