async function verify(email, token) {
  const res = await fetch("http://127.0.0.1:8000/verify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, token }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || data);
  alert(data.message);
}
