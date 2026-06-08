interface AnswerBoxProps {
  answer: string;
}

export function AnswerBox({ answer }: AnswerBoxProps) {
  return (
    <article className="card" aria-live="polite">
      <p>{answer}</p>
    </article>
  );
}