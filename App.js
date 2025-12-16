import { BrowserRouter, Route, Routes } from "react-router-dom";
import Chatbot from "./pages/Chatbot";
import Login from "./pages/Login";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Login page */}
        <Route path="/" element={<Login />} />

        {/* Chatbot page */}
        <Route path="/chat" element={<Chatbot />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
