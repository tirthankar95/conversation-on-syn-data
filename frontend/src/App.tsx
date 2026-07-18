import { useMemo, useState } from 'react'
import './App.css'

type DdlMap = Record<string, string>
type DataRow = { id: string; name: string; category: string; value: number }

const SAMPLE_DATA: DataRow[] = [
  { id: '001', name: 'Sample Data 1', category: 'Category A', value: 245.5 },
  { id: '002', name: 'Sample Data 2', category: 'Category B', value: 127.8 },
  { id: '003', name: 'Sample Data 3', category: 'Category A', value: 389.2 },
]

function readFilesAsText(
  files: File[],
): Promise<Array<{ name: string; content: string }>> {
  return Promise.all(
    files.map(
      (file) =>
        new Promise<{ name: string; content: string }>((resolve, reject) => {
          const reader = new FileReader()
          reader.onload = () => {
            resolve({ name: file.name, content: String(reader.result ?? '') })
          }
          reader.onerror = () => reject(reader.error)
          reader.readAsText(file)
        }),
    ),
  )
}

function App() {
  const [activeView, setActiveView] = useState<'generation' | 'chat'>('generation')
  const [uploadedDdls, setUploadedDdls] = useState<DdlMap>({})
  const [prompt, setPrompt] = useState('')
  const [temperature, setTemperature] = useState(0.7)
  const [maxTokens, setMaxTokens] = useState(100)
  const [selectedDataset, setSelectedDataset] = useState('users')
  const [quickEdit, setQuickEdit] = useState('')

  const ddlEntries = useMemo(() => Object.entries(uploadedDdls), [uploadedDdls])

  const handleSingleUpload = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const files = Array.from(event.target.files ?? [])
    if (!files.length) return

    const parsed = await readFilesAsText([files[0]])
    setUploadedDdls((prev) => ({ ...prev, [parsed[0].name]: parsed[0].content }))
    event.target.value = ''
  }

  const handleGenerate = () => {
    if (prompt.trim().length === 0) {
      return
    }
  }

  const clearAll = () => {
    setUploadedDdls({})
  }

  return (
    <main className="page-wrap">
      <aside className="sidebar">
        <h2 className="sidebar-title">Data Assistant</h2>
        <nav className="sidebar-nav" aria-label="Mode Switcher">
          <button
            type="button"
            className={
              activeView === 'generation' ? 'side-btn active-side-btn' : 'side-btn'
            }
            onClick={() => setActiveView('generation')}
          >
            <span className="icon-dot" aria-hidden="true">
              ●
            </span>
            Data Generation
          </button>
          <button
            type="button"
            className={activeView === 'chat' ? 'side-btn active-side-btn' : 'side-btn'}
            onClick={() => setActiveView('chat')}
          >
            <span className="icon-dot" aria-hidden="true">
              ●
            </span>
            Talk to your data
          </button>
        </nav>
      </aside>

      <section className="content-area">
        <section className="card">
          <div className="field-group">
            <label htmlFor="prompt" className="field-label">
              Prompt
            </label>
            <input
              id="prompt"
              className="text-input"
              placeholder="Enter your prompt here..."
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
            />
          </div>

          <div className="upload-row">
            <label className="upload-btn" htmlFor="ddl-upload">
              Upload DDL Schema
            </label>
            <input
              id="ddl-upload"
              type="file"
              accept=".ddl,.sql,.json"
              onChange={handleSingleUpload}
              className="hidden-upload"
            />
            <span className="hint-text">Supported formats: SQL, JSON</span>
          </div>

          {ddlEntries.length > 0 ? (
            <div className="uploaded-files-line">
              <strong>Loaded:</strong> {ddlEntries.map(([name]) => name).join(', ')}
            </div>
          ) : null}

          <hr className="separator" />

          <h3 className="section-title">Advanced Parameters</h3>
          <div className="advanced-grid">
            <div className="field-group">
              <label htmlFor="temperature" className="field-label">
                Temperature
              </label>
              <input
                id="temperature"
                className="slider"
                type="range"
                min={0}
                max={1}
                step={0.05}
                value={temperature}
                onChange={(event) => setTemperature(Number(event.target.value))}
              />
            </div>

            <div className="field-group">
              <label htmlFor="maxTokens" className="field-label">
                Max Tokens
              </label>
              <input
                id="maxTokens"
                className="text-input"
                type="number"
                min={1}
                value={maxTokens}
                onChange={(event) => setMaxTokens(Number(event.target.value) || 1)}
              />
            </div>
          </div>

          <button className="primary-btn" type="button" onClick={handleGenerate}>
            Generate
          </button>
        </section>

        <section className="card preview-card">
          <div className="preview-head">
            <h3 className="section-title">Data Preview</h3>
            <select
              className="dataset-select"
              value={selectedDataset}
              onChange={(event) => setSelectedDataset(event.target.value)}
            >
              <option value="users">users</option>
              <option value="orders">orders</option>
              <option value="products">products</option>
            </select>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Category</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {SAMPLE_DATA.map((row) => (
                  <tr key={row.id}>
                    <td>{row.id}</td>
                    <td>{row.name}</td>
                    <td>{row.category}</td>
                    <td>{row.value.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="quick-edit-row">
            <input
              className="text-input"
              placeholder="Enter quick edit instructions..."
              value={quickEdit}
              onChange={(event) => setQuickEdit(event.target.value)}
            />
            <button className="primary-btn submit-btn" type="button">
              Submit
            </button>
          </div>

          {ddlEntries.length > 0 ? (
            <button
              className="ghost-btn"
              type="button"
              onClick={clearAll}
              aria-label="Clear uploaded DDL files"
            >
              Clear uploaded schemas
            </button>
          ) : null}
        </section>
      </section>
    </main>
  )
}

export default App
