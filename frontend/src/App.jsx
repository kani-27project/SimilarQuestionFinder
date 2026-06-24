import { useState } from "react";

function App() {
const [question, setQuestion] = useState("");
const [result, setResult] = useState([]);

const findSimilar = async () => {
try {
  await fetch(
  "http://127.0.0.1:5000/add-question",
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

return (
<div style={{ padding: "30px" }}>
<h1>Similar Question Finder</h1>

  <input
    type="text"
    placeholder="Enter your study question"
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
  />

  <button onClick={findSimilar}>
    Find Similar Questions
  </button>

  <hr />

  <h2>Results</h2>

  {result.map((item, index) => (
    <div key={index}>
      <p>
        <strong>Question:</strong> {item.question}
      </p>
      <p>
  <strong>Topic:</strong> {item.topic}
      </p>
      <p>
        <strong>Similarity:</strong> {item.similarity}%
      </p>

      <hr />
    </div>
  ))}
</div>

);
}

export default App;