import { useEffect, useRef, useState } from "react";
import "../styles/chat.css";

// Create a new empty chat
function createEmptyChat() {
  return {
    id: Date.now(),
    title: "Untitled Chat",
    messages: [],
  };
}

export default function Chatbot() {
  const [chats, setChats] = useState(() => {
    const saved = localStorage.getItem("digibotChats");
    return saved ? JSON.parse(saved) : [createEmptyChat()];
  });

  const [activeId, setActiveId] = useState(() => {
    const saved = localStorage.getItem("digibotChats");
    if (saved) {
      const parsed = JSON.parse(saved);
      return parsed[0]?.id;
    }
    return null;
  });

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const chatEndRef = useRef(null);
  const activeChat = chats.find((c) => c.id === activeId);

  // Save chats to localStorage
  useEffect(() => {
    localStorage.setItem("digibotChats", JSON.stringify(chats));
  }, [chats]);

  // Auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeChat?.messages, isTyping]);

  // ---------------- SEND MESSAGE ----------------
  async function sendMessage() {
    if (!input.trim() || !activeChat) return;

    const text = input;
    setInput("");

    // Add user message
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === activeId
          ? {
              ...chat,
              title:
                chat.messages.length === 0
                  ? text.slice(0, 30)
                  : chat.title,
              messages: [...chat.messages, { sender: "user", text }],
            }
          : chat
      )
    );

    setIsTyping(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text }),
      });

      const data = await res.json();

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeId
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  { sender: "bot", text: data.reply || "No response." },
                ],
              }
            : chat
        )
      );
    } catch {
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeId
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  {
                    sender: "bot",
                    text: "Unable to connect to backend.",
                  },
                ],
              }
            : chat
        )
      );
    } finally {
      setIsTyping(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  }

  // ---------------- NEW CHAT ----------------
  function createChat() {
    const newChat = createEmptyChat();
    setChats((prev) => [newChat, ...prev]);
    setActiveId(newChat.id);
  }

  // ---------------- DELETE CHAT ----------------
  function deleteChat(id) {
    const remaining = chats.filter((c) => c.id !== id);
    const fallback = remaining.length ? remaining : [createEmptyChat()];
    setChats(fallback);
    setActiveId(fallback[0].id);
  }

  return (
    <div className="chat-container">
      {/* SIDEBAR */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>DigiBot</h2>
          <button onClick={createChat}>+ New Chat</button>
        </div>

        <div className="chat-list">
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${
                chat.id === activeId ? "active" : ""
              }`}
              onClick={() => setActiveId(chat.id)}
            >
              <span className="chat-title">{chat.title}</span>
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteChat(chat.id);
                }}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* MAIN CHAT */}
      <div className="chat-main">
        <div className="messages">
          {activeChat?.messages.map((msg, i) => (
            <div
              key={i}
              className={`msg ${
                msg.sender === "user" ? "user-msg" : "bot-msg"
              }`}
            >
              {msg.text}
            </div>
          ))}

          {isTyping && (
            <div className="msg bot-msg typing">
              DigiBot is typing…
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* INPUT */}
        <div className="input-area">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask DigiBot anything…"
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}
