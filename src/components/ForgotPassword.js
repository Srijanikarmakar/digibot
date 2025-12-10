const form = document.getElementById("forgotPasswordForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;

  try {
    const res = await fetch("http://127.0.0.1:8000/forgot-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || data.message);

    alert("Reset link sent! Please check your email.");
  } catch (err) {
    alert(err.message);
  }
});
