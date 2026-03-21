const Sidebar = ({ onNewChat }) => {
  const services = [
    { name: "GitHub", icon: "○" },
    { name: "Notion", icon: "□" },
    { name: "Web Search", icon: "◎" },
    { name: "Documents", icon: "▭" },
  ];

  return (
    <div
      style={{
        width: "240px",
        background: "#f1efe8",
        borderRight: "0.5px solid #d3d1c7",
        display: "flex",
        flexDirection: "column",
        padding: "16px 12px",
        flexShrink: 0,
      }}
    >
      {/* Logo */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          padding: "4px 8px",
          marginBottom: "20px",
        }}
      >
        <div
          style={{
            width: "32px",
            height: "32px",
            background: "#c96442",
            borderRadius: "8px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            fontSize: "13px",
            fontWeight: "500",
            flexShrink: 0,
          }}
        >
          P
        </div>
        <div>
          <div
            style={{ fontSize: "15px", fontWeight: "500", color: "#1a1a19" }}
          >
            PersonalAI
          </div>
          <div style={{ fontSize: "11px", color: "#888780" }}>
            Your AI Assistant
          </div>
        </div>
      </div>

      {/* New Chat */}
      <button
        onClick={onNewChat}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          padding: "8px 12px",
          border: "0.5px solid #b4b2a9",
          borderRadius: "8px",
          background: "transparent",
          cursor: "pointer",
          fontSize: "13px",
          color: "#5f5e5a",
          marginBottom: "24px",
          width: "100%",
        }}
        onMouseOver={(e) => (e.currentTarget.style.background = "#e8e6de")}
        onMouseOut={(e) => (e.currentTarget.style.background = "transparent")}
      >
        + New chat
      </button>

      {/* Services */}
      <div
        style={{
          fontSize: "11px",
          color: "#888780",
          letterSpacing: "0.05em",
          textTransform: "uppercase",
          padding: "0 8px",
          marginBottom: "8px",
        }}
      >
        Connected
      </div>

      {services.map((s) => (
        <div
          key={s.name}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "6px 8px",
            borderRadius: "6px",
            fontSize: "13px",
            color: "#5f5e5a",
            cursor: "pointer",
          }}
        >
          <span style={{ fontSize: "12px" }}>{s.icon}</span>
          {s.name}
          <span
            style={{
              marginLeft: "auto",
              width: "6px",
              height: "6px",
              borderRadius: "50%",
              background: "#3b6d11",
            }}
          />
        </div>
      ))}

      <div style={{ flex: 1 }} />

      {/* Clear */}
      <button
        onClick={onNewChat}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          padding: "8px 12px",
          borderRadius: "6px",
          border: "none",
          background: "transparent",
          cursor: "pointer",
          fontSize: "13px",
          color: "#888780",
          width: "100%",
        }}
        onMouseOver={(e) => (e.currentTarget.style.background = "#e8e6de")}
        onMouseOut={(e) => (e.currentTarget.style.background = "transparent")}
      >
        ⌫ Clear chat
      </button>
    </div>
  );
};

export default Sidebar;
