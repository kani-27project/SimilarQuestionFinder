import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState([]);
  const [history, setHistory] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("All");

  const findSimilar = async () => {
    try {
      await fetch("http://127.0.0.1:5000/add-question", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const response = await fetch(
        "http://127.0.0.1:5000/similar",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.log(error);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/history/1"
      );

      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="container py-5">
      <div className="bg-white p-5 rounded shadow-lg">

        <div className="text-center mb-5">
          <h1 className="display-4 fw-bold text-primary">
            Similar Question Finder
          </h1>

          <p className="text-muted">
            AI Powered Semantic Question Search
          </p>
        </div>

        <div className="row justify-content-center mb-4">
          <div className="col-md-8">

            <div className="input-group">
              <input
                type="text"
                className="form-control form-control-lg"
                placeholder="Enter your study question..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />

              <button
                className="btn btn-primary btn-lg"
                onClick={findSimilar}
              >
                🔍 Search
              </button>
            </div>

          </div>
        </div>

        <div className="text-center mb-4">
          <button
            className="btn btn-secondary"
            onClick={loadHistory}
          >
            📜 View History
          </button>
        </div>

        <h2 className="text-center mb-4 text-primary fw-bold">
          Search Results
        </h2>

        {result.length === 0 ? (
          <div className="text-center text-muted">
            No results found
          </div>
        ) : (
          result.map((item, index) => (
            <div
              key={index}
              className="card shadow-lg mb-4 border-start border-4 border-primary"
            >
              <div className="card-body">

                <h5 className="card-title mb-3">
                  {item.question}
                </h5>

                <span className="badge bg-success mb-3">
                  {item.topic}
                </span>

                <p className="mb-0 fs-5">
                  <strong>Similarity:</strong>{" "}
                  <span className="text-success fw-bold">
                    {item.similarity}%
                  </span>
                </p>

              </div>
            </div>
          ))
        )}

        <h2 className="text-center mt-5 text-primary fw-bold">
          History
        </h2>

        <div className="mb-4">
          <select
            className="form-select"
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
          >
            <option value="All">All Topics</option>
            <option value="Biology">Biology</option>
            <option value="Physics">Physics</option>
            <option value="Math">Math</option>
          </select>
        </div>

        {history.length === 0 ? (
          <div className="text-center text-muted">
            Click "View History" to load previous questions
          </div>
        ) : (
          history
            .filter(
              (item) =>
                selectedTopic === "All" ||
                item.topic === selectedTopic
            )
            .map((item) => (
              <div
                key={item.id}
                className="card shadow-sm mb-3"
              >
                <div className="card-body">
                  <h5>{item.question}</h5>

                  <span className="badge bg-info">
                    {item.topic}
                  </span>
                </div>
              </div>
            ))
        )}

      </div>
    </div>
  );
}

export default App;