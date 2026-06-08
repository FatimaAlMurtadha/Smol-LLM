import { useState } from "react";
import { askQuestion } from "../api/client";

interface QuestionFormProps {
  onAnswer: (answer: string) => void;
}

export function QuestionForm({ onAnswer }: QuestionFormProps) {
  const [question, setQuestion] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const result = await askQuestion(question);
    onAnswer(result.answer);
  }

  return (
    <section aria-label="Ask a question about the data">
      <form onSubmit={handleSubmit}>
        <label htmlFor="question-input">Fråga</label>
        <input
          id="question-input"
          className="input"
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What is the average score?"
        />
        <button type="submit" className="btn-secondary">
          Fråga
        </button>
      </form>
    </section>
  );
}