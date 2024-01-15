document.addEventListener("DOMContentLoaded", () => {
  const signInForm = document.querySelector('.login-form');
  const usernameInput = document.querySelector('.usrnm');
  const passwordInput = document.querySelector('.pswd');
  const submitButton = document.querySelector('input[type="submit"]');

  signInForm.addEventListener('input', () => {
    submitButton.disabled = usernameInput.value.length === 0 || passwordInput.value.length === 0;
  });
});
