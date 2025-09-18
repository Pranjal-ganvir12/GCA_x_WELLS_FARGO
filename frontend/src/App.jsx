import React, { useState } from "react";

function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleCheck = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8001/precheck?age_group=30-44");
      const data = await res.json();
      console.log(data);
      setMessage(data.message);
    } catch (err) {
      setMessage("❌ Could not load eligibility. Try again.");
    }
  };
  

  return (
    <div className="container">
      <div className="card">
        <h1>Unexpected Bill?</h1>
        <p>Wells Fargo Emergency Cushion helps you get funds instantly.</p>
        <button onClick={handleCheck}>Check Eligibility</button>

        {result && (
          <div className="result">
            <p>{result.message}</p>
            <p>
              ✅ Eligible: <b>{result.eligible ? "Yes" : "No"}</b>
            </p>
          </div>
        )}

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
