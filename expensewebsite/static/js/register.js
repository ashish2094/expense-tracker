const usernameField = document.querySelector("#usernamefield");
const emailField = document.querySelector("#emailfield");
const userfeed = document.querySelector(".invalid-userfeed");
const uservalidfeed = document.querySelector(".valid-userfeed");
const emailfeed = document.querySelector(".invalid-emailfeed");
const emailvalidfeed = document.querySelector(".valid-emailfeed");
const showPass = document.querySelector(".showpass");
const passwordField = document.querySelector("#passwordfield");
const submitbtn = document.querySelector(".submit-btn");

usernameField.addEventListener("keyup", (e) => {
  console.log("619");
  const usernameVal = e.target.value;
  if (usernameVal.length > 0) {
    fetch("/auth/validate-username/", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    }).then((res) =>
      res.json().then((data) => {
        console.log("data", data);
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          userfeed.style.display = "block";
          uservalidfeed.style.display = "none";
          userfeed.innerHTML = `<p style="color : red;">${data.username_error}</p>`;
          submitbtn.disabled = true;
        } else {
          usernameField.classList.remove("is-invalid");
          userfeed.style.display = "none";
          uservalidfeed.style.display = "block";
          uservalidfeed.innerHTML = `<p style="color : green;">${data.username_valid}</p>`;
          submitbtn.disabled = false;
        }
      })
    );
  }
});

emailField.addEventListener("keyup", (e) => {
  console.log("pass");
  const emailVal = e.target.value;
  if (emailVal.length > 0) {
    fetch("/auth/validate-email/", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    }).then((res) =>
      res.json().then((data) => {
        console.log("data", data);
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          emailfeed.style.display = "block";
          emailfeed.innerHTML = `<p style="color : red;">${data.email_error}</p>`;
          submitbtn.disabled = true;
        } else {
          emailField.classList.remove("is-invalid");
          emailfeed.style.display = "none";
          //emailvalidfeed.style.display = "block";
          submitbtn.disabled = false;
        }
      })
    );
  }
});

showPass.addEventListener("click", (e) => {
  showPass.style.cursor = "pointer"; //dont why its not working in main.css
  showPass.style.transform = "scale(1.2)"; //dont why its not working in main.css
  if (showPass.textContent === "Show") {
    showPass.textContent = "Hide";
    passwordField.setAttribute("type", "text");
  } else {
    showPass.textContent = "Show";
    passwordField.setAttribute("type", "password");
  }
});
