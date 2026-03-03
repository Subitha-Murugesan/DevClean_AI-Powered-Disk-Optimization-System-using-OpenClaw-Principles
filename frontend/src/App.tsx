import { useEffect, useState } from 'react'
import './App.css'

interface FileTypes {
  [key: string]: number;
}

interface Folders {
  [key: string]: number;
}

interface DiskAnalysis {
  agent: string;
  file_types: FileTypes;
  folders: Folders;
  total_size: number;
}

interface DockerAnalysis {
  agent: string;
  unused_images: string[];
  dangling_volumes: string[];
  stopped_containers?: string[];
  error?: string;
}

interface CacheAnalysis {
  agent: string;
  npm_cache?: { path: string; size: number } | null;
  pip_cache?: { path: string; size: number } | null;
  docker_cache?: { path: string; size: number } | null;
  git_objects?: { path: string; size: number } | null;
}

interface AgentResult {
  agent: string;
  [key: string]: any;
}

interface MultiAgentResponse {
  workflow: string;
  agents: AgentResult[];
  recommendations: string;
}

function App() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<MultiAgentResponse | null>(null)
  const [agentStatus, setAgentStatus] = useState<any>(null)

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
  }

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    
    // Fetch agent status first
    try {
      const statusResponse = await fetch('http://localhost:8000/agents/status')
      if (statusResponse.ok) {
        const status = await statusResponse.json()
        setAgentStatus(status)
      }
    } catch (err) {
      console.warn('Could not fetch agent status')
    }
    
    try {
      const response = await fetch('http://localhost:8000/analyze')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analysis')
    } finally {
      setLoading(false)
    }
  }

  const getDiskAgentData = (): DiskAnalysis | null => {
    if (!data) return null
    return data.agents.find(agent => agent.agent === 'disk_analyzer') as DiskAnalysis | null
  }

  const getDockerAgentData = (): DockerAnalysis | null => {
    if (!data) return null
    return data.agents.find(agent => agent.agent === 'docker_analyzer') as DockerAnalysis | null
  }

  const getCacheAgentData = (): CacheAnalysis | null => {
    if (!data) return null
    return data.agents.find(agent => agent.agent === 'cache_analyzer') as CacheAnalysis | null
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🧹 DevClean</h1>
          <p>Intelligent Disk Optimization & Cleanup</p>
        </header>

        <div className="button-section">
          <button 
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? '⏳ Analyzing...' : '🚀 Analyze Disk'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            <span>❌ {error}</span>
          </div>
        )}

        {data && (
          <div className="results">
            {/* Agent Status */}
            {data && (
              <div className="result-card agents-info">
                <h2>🤖 Multi-Agent Analysis Report</h2>
                <p className="workflow-info">Workflow: <strong>{data.workflow}</strong></p>
                <div className="agents-list">
                  {data.agents.map((agent, index) => (
                    <div key={index} className="agent-badge">
                      {agent.agent === 'disk_analyzer' && '💾'}
                      {agent.agent === 'docker_analyzer' && '🐳'}
                      {agent.agent === 'cache_analyzer' && '📦'}
                      {' ' + agent.agent.replace('_', ' ')}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* File Types Analysis */}
            {getDiskAgentData() && (
              <div className="result-card">
                <h2>📊 File Types Analysis <span className="agent-label">📁 Disk Analyzer</span></h2>
                <div className="file-types">
                  {Object.entries(getDiskAgentData()!.file_types).length > 0 ? (
                    <div className="table">
                      <div className="table-header">
                        <div className="table-cell">Extension</div>
                        <div className="table-cell">Size</div>
                        <div className="table-cell">Percentage</div>
                      </div>
                      {Object.entries(getDiskAgentData()!.file_types)
                        .sort(([, a], [, b]) => b - a)
                        .slice(0, 10)
                        .map(([ext, size]) => {
                          const totalSize = getDiskAgentData()!.total_size
                          const percentage = ((size / totalSize) * 100).toFixed(2)
                          return (
                            <div key={ext} className="table-row">
                              <div className="table-cell">{ext || 'No Extension'}</div>
                              <div className="table-cell">{formatBytes(size)}</div>
                              <div className="table-cell">
                                <div className="progress-bar">
                                  <div 
                                    className="progress-fill"
                                    style={{ width: `${percentage}%` }}
                                  ></div>
                                </div>
                                {percentage}%
                              </div>
                            </div>
                          )
                        })}
                    </div>
                  ) : (
                    <p>No file types data available</p>
                  )}
                </div>
              </div>
            )}

            {/* Largest Folders */}
            {getDiskAgentData() && (
              <div className="result-card">
                <h2>💾 Largest Folders <span className="agent-label">📁 Disk Analyzer</span></h2>
                <div className="folders">
                  {Object.entries(getDiskAgentData()!.folders).length > 0 ? (
                    <div className="table">
                      <div className="table-header">
                        <div className="table-cell">Folder</div>
                        <div className="table-cell">Size</div>
                      </div>
                      {Object.entries(getDiskAgentData()!.folders)
                        .sort(([, a], [, b]) => b - a)
                        .slice(0, 10)
                        .map(([folder, size]) => (
                          <div key={folder} className="table-row">
                            <div className="table-cell folder-name">{folder}</div>
                            <div className="table-cell">{formatBytes(size)}</div>
                          </div>
                        ))}
                    </div>
                  ) : (
                    <p>No folder data available</p>
                  )}
                </div>
              </div>
            )}

            {/* Docker Analysis */}
            {getDockerAgentData() && !getDockerAgentData()?.error && (
              <div className="result-card">
                <h2>🐳 Docker Analysis <span className="agent-label">🐳 Docker Analyzer</span></h2>
                <div className="docker-info">
                  <div className="info-item">
                    <strong>Unused Images:</strong> 
                    <span style={{ fontSize: '1.2rem', fontWeight: '700', color: '#a5f3fc' }}>
                      {getDockerAgentData()?.unused_images?.length || 0}
                    </span>
                  </div>
                  <div className="info-item">
                    <strong>Dangling Volumes:</strong>
                    <span style={{ fontSize: '1.2rem', fontWeight: '700', color: '#a5f3fc' }}>
                      {getDockerAgentData()?.dangling_volumes?.length || 0}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Cache Analysis */}
            {getCacheAgentData() && (
              <div className="result-card">
                <h2>📦 Package Caches <span className="agent-label">📦 Cache Analyzer</span></h2>
                <div className="cache-info">
                  {getCacheAgentData()?.npm_cache && (
                    <div className="cache-item">
                      <strong>npm cache:</strong> 
                      <span style={{ fontSize: '1.1rem', fontWeight: '700', color: '#a5f3fc', display: 'block' }}>
                        {formatBytes(getCacheAgentData()!.npm_cache!.size)}
                      </span>
                    </div>
                  )}
                  {getCacheAgentData()?.pip_cache && (
                    <div className="cache-item">
                      <strong>pip cache:</strong>
                      <span style={{ fontSize: '1.1rem', fontWeight: '700', color: '#a5f3fc', display: 'block' }}>
                        {formatBytes(getCacheAgentData()!.pip_cache!.size)}
                      </span>
                    </div>
                  )}
                  {getCacheAgentData()?.git_objects && (
                    <div className="cache-item">
                      <strong>git objects:</strong>
                      <span style={{ fontSize: '1.1rem', fontWeight: '700', color: '#a5f3fc', display: 'block' }}>
                        {formatBytes(getCacheAgentData()!.git_objects!.size)}
                      </span>
                    </div>
                  )}
                  {!getCacheAgentData()?.npm_cache && !getCacheAgentData()?.pip_cache && (
                    <p>No significant caches found</p>
                  )}
                </div>
              </div>
            )}

            {/* AI Recommendations */}
            <div className="result-card suggestions">
              <h2>💡 AI Recommendations <span className="agent-label">🤖 Optimization Agent</span></h2>
              <div className="suggestions-content">
                {data.recommendations.split('\n').map((line, index) => (
                  line.trim() && <p key={index}>{line}</p>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
