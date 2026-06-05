import './App.css'
import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import type { ColumnStats } from './interfaces/stats';

function App() {
  const [stats, setStats] = useState<Record<string, ColumnStats> | null>(null);

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
              <pre className="card">
                {JSON.stringify(stats, null, 2)}
              </pre>
            </section>
          )}
        </section>
        </main>
      
      </div>

      
    </>
  );
}

export default App
