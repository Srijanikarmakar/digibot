async function requestLoginOtp(email) {
  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || data);
  alert(data.message);
}
const token = localStorage.getItem("jwt");
fetch("http://127.0.0.1:8000/protected-endpoint", {
  headers: { "Authorization": `Bearer ${token}` }
});