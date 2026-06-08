import './App.css'
import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import type { ColumnStats } from './interfaces/stats';
import { QuestionForm } from './components/QuestionForm';
import { AnswerBox } from './components/AnswerBox';

function App() {
  const [stats, setStats] = useState<Record<string, ColumnStats> | null>(null);
  const [answer, setAnswer] = useState("");

  return (
    <>
      <div className="home">
        <header>
          <div className="container">
            <h1 className="title">KK2 Oracle UI</h1>
            <p>Ladda upp data, fråga och få AI svar om din data</p>
          </div>
        </header>

        <main>
          <section className="container" aria-labelledby="data-section-title">
            <h2 className="data-section-title">Data uppladdning</h2>
            <FileUpload onStats={setStats} />

            {stats && (
              <section aria-labelledby="stats-title">
                <h3 className="stats-title">Statistiker</h3>
                <pre className="card">{JSON.stringify(stats, null, 2)}</pre>
              </section>
            )}
          </section>

          <section className="container" aria-labelledby="qa-section-title">
            <h2 id="qa-section-title">Fråga Oraklet</h2>
            <QuestionForm onAnswer={setAnswer} />

            {answer && (
              <section aria-labelledby="answer-title">
                <h3 id="answer-title">Answer</h3>
                <AnswerBox answer={answer} />
              </section>
            )}
          </section>
        </main>

        <footer>
          <div className="container">
            <small>KK2 · Oraklet chain demo</small>
          </div>
        </footer>
      </div>
    </>
  );
}

export default App
