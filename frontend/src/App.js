const { useState, useEffect } = React;

const API_BASE_URL = 'http://localhost:8000';

function App() {
    const [prompt, setPrompt] = useState('');
    const [language, setLanguage] = useState('auto');
    const [generatedCode, setGeneratedCode] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);
    const [status, setStatus] = useState(null);
    const [outputId, setOutputId] = useState(null);
    const [rating, setRating] = useState(0);
    const [feedbackComments, setFeedbackComments] = useState('');
    const [statistics, setStatistics] = useState(null);
    
    const languages = [
        { value: 'auto', label: '🔍 Auto-detect' },
        { value: 'python', label: '🐍 Python' },
        { value: 'javascript', label: '📜 JavaScript' },
        { value: 'typescript', label: '📘 TypeScript' },
        { value: 'java', label: '☕ Java' },
        { value: 'cpp', label: '⚙️ C++' },
        { value: 'rust', label: '🦀 Rust' },
        { value: 'go', label: '🔷 Go' },
        { value: 'csharp', label: '💠 C#' },
    ];
    
    const examples = [
        { name: 'Python REST API', prompt: 'Create a REST API endpoint for user authentication with JWT tokens in Python using FastAPI' },
        { name: 'React Component', prompt: 'Build a React component for a todo list with add, delete, and mark complete functionality' },
        { name: 'Binary Search', prompt: 'Implement a binary search algorithm in Python with error handling' },
        { name: 'Sorting Algorithm', prompt: 'Create a quick sort implementation in JavaScript with comments' },
        { name: 'Database CRUD', prompt: 'Build CRUD operations for a user model in Java with Spring Boot' },
        { name: 'Web Scraper', prompt: 'Create a web scraper in Python using BeautifulSoup to extract article titles' },
    ];
    
    useEffect(() => {
        fetchStatistics();
    }, []);
    
    const fetchStatistics = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/statistics`);
            const data = await response.json();
            setStatistics(data);
        } catch (error) {
            console.error('Failed to fetch statistics:', error);
        }
    };
    
    const handleGenerate = async () => {
        if (!prompt.trim()) {
            setStatus({ type: 'error', message: 'Please enter a prompt' });
            return;
        }
        
        setIsGenerating(true);
        setStatus({ type: 'info', message: 'Generating code...' });
        setGeneratedCode('');
        setOutputId(null);
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    language: language === 'auto' ? null : language,
                    temperature: 0.3,
                    max_tokens: 1000
                })
            });
            
            if (!response.ok) {
                throw new Error('Generation failed');
            }
            
            const data = await response.json();
            setGeneratedCode(data.code);
            setOutputId(data.output_id);
            setStatus({
                type: 'success',
                message: `✅ Generated ${data.language} code with ${data.model} in ${data.generation_time_ms}ms`
            });
            
            // Highlight code
            setTimeout(() => {
                Prism.highlightAll();
            }, 100);
            
        } catch (error) {
            setStatus({ type: 'error', message: `❌ Error: ${error.message}` });
        } finally {
            setIsGenerating(false);
        }
    };
    
    const handleFeedback = async () => {
        if (!outputId) {
            setStatus({ type: 'error', message: 'No code to rate' });
            return;
        }
        
        if (rating === 0) {
            setStatus({ type: 'error', message: 'Please select a rating' });
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    output_id: outputId,
                    rating: rating,
                    comments: feedbackComments || null
                })
            });
            
            if (!response.ok) {
                throw new Error('Feedback submission failed');
            }
            
            setStatus({ type: 'success', message: '✅ Thank you for your feedback!' });
            setRating(0);
            setFeedbackComments('');
            fetchStatistics(); // Refresh stats
            
        } catch (error) {
            setStatus({ type: 'error', message: `❌ Error: ${error.message}` });
        }
    };
    
    const handleCopy = () => {
        navigator.clipboard.writeText(generatedCode);
        setStatus({ type: 'success', message: '📋 Code copied to clipboard!' });
    };
    
    const handleClear = () => {
        setGeneratedCode('');
        setOutputId(null);
        setRating(0);
        setFeedbackComments('');
        setStatus(null);
    };
    
    const handleExampleClick = (examplePrompt) => {
        setPrompt(examplePrompt);
    };
    
    return (
        <div>
            {/* Header */}
            <div className="header">
                <h1>🚀 AI Code Generator</h1>
                <p>Generate code in multiple languages using local Ollama Mistral model</p>
            </div>
            
            {/* Status Bar */}
            {status && (
                <div className={`status-bar ${status.type}`}>
                    <span>{status.message}</span>
                </div>
            )}
            
            {/* Main Container */}
            <div className="container">
                {/* Left Column - Input */}
                <div>
                    <div className="card">
                        <h2>📝 Input</h2>
                        
                        <div className="prompt-section">
                            <textarea
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                placeholder="Describe the code you want to generate... (e.g., 'Create a REST API endpoint for user login with password validation in Python')"
                            />
                        </div>
                        
                        <div className="language-selector">
                            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                                {languages.map(lang => (
                                    <option key={lang.value} value={lang.value}>
                                        {lang.label}
                                    </option>
                                ))}
                            </select>
                        </div>
                        
                        <button
                            className="btn btn-primary"
                            onClick={handleGenerate}
                            disabled={isGenerating}
                        >
                            {isGenerating ? (
                                <>
                                    <span className="loading"></span>
                                    Generating...
                                </>
                            ) : (
                                <>🚀 Generate Code</>
                            )}
                        </button>
                    </div>
                    
                    {/* Quick Examples */}
                    <div className="card" style={{marginTop: '20px'}}>
                        <h2>💡 Quick Examples</h2>
                        <div className="examples-grid">
                            {examples.map((example, index) => (
                                <button
                                    key={index}
                                    className="example-btn"
                                    onClick={() => handleExampleClick(example.prompt)}
                                >
                                    {example.name}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
                
                {/* Right Column - Output */}
                <div>
                    <div className="card">
                        <h2>📄 Generated Code</h2>
                        
                        {generatedCode ? (
                            <>
                                <div className="code-output">
                                    <pre><code className={`language-${language === 'auto' ? 'python' : language}`}>{generatedCode}</code></pre>
                                </div>
                                
                                <div className="code-actions">
                                    <button className="btn btn-secondary" onClick={handleCopy}>
                                        📋 Copy
                                    </button>
                                    <button className="btn btn-secondary" onClick={handleClear}>
                                        🗑️ Clear
                                    </button>
                                </div>
                                
                                {/* Feedback Section */}
                                <div className="feedback-section">
                                    <h3>💬 Rate This Code</h3>
                                    <p style={{color: 'var(--text-secondary)', fontSize: '0.9rem'}}>
                                        Help improve the AI by rating the generated code
                                    </p>
                                    
                                    <div className="rating-buttons">
                                        {[1, 2, 3, 4, 5].map(stars => (
                                            <button
                                                key={stars}
                                                className={`rating-btn ${rating === stars ? 'selected' : ''}`}
                                                onClick={() => setRating(stars)}
                                            >
                                                {'⭐'.repeat(stars)}
                                            </button>
                                        ))}
                                    </div>
                                    
                                    <textarea
                                        className="feedback-input"
                                        placeholder="Optional: Add comments about the generated code..."
                                        value={feedbackComments}
                                        onChange={(e) => setFeedbackComments(e.target.value)}
                                    />
                                    
                                    <button
                                        className="btn btn-primary"
                                        onClick={handleFeedback}
                                        style={{marginTop: '16px'}}
                                    >
                                        📤 Submit Feedback
                                    </button>
                                </div>
                            </>
                        ) : (
                            <div style={{textAlign: 'center', padding: '60px 20px', color: 'var(--text-secondary)'}}>
                                <div style={{fontSize: '4rem', marginBottom: '20px'}}>💻</div>
                                <p>Generated code will appear here...</p>
                                <p style={{fontSize: '0.9rem', marginTop: '10px'}}>Enter a prompt and click "Generate Code"</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
            
            {/* Statistics */}
            {statistics && (
                <div className="card">
                    <h2>📊 Statistics</h2>
                    <div className="stats-grid">
                        <div className="stat-card">
                            <div className="stat-value">{statistics.total_prompts}</div>
                            <div className="stat-label">Total Generations</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-value">{statistics.total_feedback}</div>
                            <div className="stat-label">Feedback Received</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-value">{statistics.avg_rating.toFixed(1)}⭐</div>
                            <div className="stat-label">Average Rating</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-value">{statistics.learning_patterns}</div>
                            <div className="stat-label">Patterns Learned</div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
