
async function resetPassword(email, otp, new_password) {
  const res = await fetch("http://127.0.0.1:8000/reset-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, otp, new_password })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || data);
  alert(data.message);
}
