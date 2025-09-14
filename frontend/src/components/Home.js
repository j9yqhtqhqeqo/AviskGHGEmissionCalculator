import React, { useState } from "react";

function Home() {
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    setResponse("");
    try {
      const res = await fetch("http://127.0.0.1:5000/");
      const data = await res.json();
      setResponse(data.message);
    } catch (err) {
      setResponse("Error connecting to backend");
    }
    setLoading(false);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginTop: 100,
      }}
    >
      <h1>GHG Emission Calculator</h1>
      <p>Click below to test the backend connection</p>
      <button
        onClick={handleClick}
        disabled={loading}
        style={{ fontSize: 20, padding: "10px 30px" }}
      >
        {loading ? "Loading..." : "Get Backend Response"}
      </button>
      {response && (
        <div style={{ marginTop: 30, fontSize: 18 }}>{response}</div>
      )}
    </div>
  );
}

export default Home;
