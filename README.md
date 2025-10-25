# 🚀 AI Code Generator with Feedback Learning# 🚀 Advanced Code Generation AI System



A powerful AI-powered code generation application that learns from your feedback using your local Ollama Mistral model.A comprehensive, modern code generation platform powered by cutting-edge AI models including CodeLlama, StarCoder, GPT-4, and Claude-3. This system provides multiple approaches to code generation with ensemble capabilities, cloud API integrations, and advanced evaluation tools.



## ✨ Features![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

![License](https://img.shields.io/badge/License-MIT-green.svg)

- **🤖 AI-Powered Generation**: Uses your local Ollama Mistral model![Status](https://img.shields.io/badge/Status-Active%20Development-orange.svg)

- **💻 Multi-Language Support**: Python, JavaScript, Java, C++, Rust, Go, TypeScript

- **📚 Feedback Learning System**: Learns from your ratings to improve## ✨ Features

- **🎯 Smart Model Selection**: Automatically picks the best available model

- **💡 AI Suggestions**: Get tips based on successful past generations### 🎯 **Multi-Model Support**

- **📊 Progress Tracking**: Detailed statistics on your learning journey- **Local Models**: CodeLlama, StarCoder, WizardCoder, CodeT5-Plus

- **Cloud APIs**: OpenAI GPT-4, Anthropic Claude-3, Hugging Face Inference

## 🚀 Quick Start- **Ensemble Generation**: Combines multiple models for optimal results

- **Fallback Support**: Automatic fallback to alternative models

### 1. Install Dependencies

### 🏗️ **Advanced Architecture**

```bash- **Quantization Support**: 4-bit and 8-bit model loading for efficiency

pip install -r requirements.txt- **Flash Attention**: Optimized attention mechanisms for faster inference

```- **LoRA Fine-tuning**: Efficient model adaptation capabilities

- **Async Processing**: Concurrent model execution for speed

### 2. Ensure Ollama is Running

### 🌐 **Modern Web Interface**

```bash- **Interactive UI**: Gradio-powered web interface

# Start Ollama server- **Real-time Generation**: Live code generation with progress tracking

ollama serve- **Multiple Languages**: Support for Python, JavaScript, TypeScript, Java, C++, Rust, Go

- **Export Functionality**: Save generated code to files

# Verify Mistral is installed- **Generation History**: Track and manage previous generations

ollama list

### 🔍 **Comprehensive Evaluation**

# If not installed, pull Mistral- **Syntax Validation**: Multi-language syntax checking

ollama pull mistral- **Quality Metrics**: Cyclomatic complexity, maintainability index, documentation score

```- **Security Analysis**: Vulnerability detection and recommendations

- **Performance Analysis**: Algorithm complexity and optimization suggestions

### 3. Run the Application- **Overall Scoring**: 0-100 quality score with detailed feedback



```bash## 🚀 Quick Start

python app.py

```### Prerequisites



### 4. Open in Browser- Python 3.8 or higher

- CUDA-capable GPU (recommended for local models)

Navigate to: http://localhost:7860- 16GB+ RAM (32GB+ recommended for larger models)



## 📖 How to Use### Installation



1. **Enter a Code Description**: Be specific about what you want to create1. **Clone the repository:**

2. **Select Language**: Choose from 7 programming languages```bash

3. **Generate Code**: Click the "Generate Code" buttongit clone <repository-url>

4. **Review Output**: Check the generated codecd gen

5. **Rate & Provide Feedback**: Help the AI learn by rating (1-5 stars) and adding comments```

6. **View Progress**: Check the "Learning Statistics" section to see improvement

2. **Create virtual environment:**

## 💡 Tips for Best Results```bash

python -m venv venv

- **Be Specific**: Include details about error handling, validation, edge casessource venv/bin/activate  # On Windows: venv\Scripts\activate

- **Rate Honestly**: Your feedback directly improves future generations```

- **Add Comments**: Specific feedback is more valuable than just ratings

- **Try Examples**: Use the quick example buttons to see what works well3. **Install dependencies:**

```bash

## 📊 Learning Systempip install -r requirements.txt

```

The application learns from your feedback:

- **High Ratings (4-5 ⭐)**: Patterns are saved as successful approaches4. **Set up API keys (optional for cloud models):**

- **Low Ratings (1-2 ⭐)**: Issues are identified to avoid in futureCreate a `.env` file in the project root:

- **Suggestions**: AI provides language-specific tips based on history```env

- **Continuous Improvement**: More feedback = better results over timeOPENAI_API_KEY=your_openai_api_key_here

ANTHROPIC_API_KEY=your_anthropic_api_key_here

## 🗂️ Data StorageHUGGINGFACE_API_KEY=your_huggingface_api_key_here

```

- **feedback.json**: Stores all your feedback entries

- **patterns.json**: Stores learned patterns (good and bad)### Launch Web Interface

- Data is saved in the `data/` directory

```bash

## 🔧 Configurationpython web_ui/gradio_interface.py

```

The application automatically:

- Detects available Ollama modelsThe interface will be available at `http://localhost:7860`

- Selects the best model for code generation (prioritizes: codellama > deepseek-coder > mistral > llama3)

- Falls back to templates if Ollama is unavailable## 📁 Project Structure



## 📝 Example Prompts```

gen/

Try these for great results:├── models/                          # AI model implementations

- "Create a REST API endpoint for user authentication with JWT tokens and input validation"│   ├── codet5_generator.py         # Basic CodeT5 generator

- "Build a binary search algorithm with proper error handling for edge cases"│   ├── advanced_generator.py       # Modern transformer models

- "Implement a web scraper with rate limiting, retry logic, and data validation"│   └── ensemble_generator.py       # Multi-model ensemble system

- "Create database CRUD operations with transaction support and connection pooling"├── api_integrations/                # Cloud API integrations

│   └── cloud_generators.py         # OpenAI, Anthropic, HuggingFace APIs

## 🤝 Contributing├── web_ui/                         # Web interface

│   └── gradio_interface.py         # Modern Gradio-based UI

Feedback and suggestions are welcome! The more you use and rate generations, the better the system becomes.├── evaluation/                     # Code quality analysis

│   └── code_evaluator.py          # Comprehensive evaluation tools

## 📄 License├── examples/                       # Usage examples and demos

├── requirements.txt                # Python dependencies

Free to use and modify.└── README.md                       # This file

```

---

## 💻 Usage Examples

**Made with ❤️ using Gradio, Ollama, and your local Mistral model**

### Basic Code Generation

```python
from models.advanced_generator import AdvancedCodeGenerator, ModelType

# Initialize generator
generator = AdvancedCodeGenerator(
    model_type=ModelType.CODE_LLAMA,
    use_quantization=True,
    load_in_4bit=True
)

# Generate code
code = generator.generate_code(
    prompt="binary search algorithm with error handling",
    language="python"
)

print(code)
```

### Ensemble Generation

```python
from models.ensemble_generator import EnsembleCodeGenerator, MockCodeGenerator
import asyncio

# Create ensemble
ensemble = EnsembleCodeGenerator()

# Add models
models = [
    ("CodeLlama", MockCodeGenerator("CodeLlama", 0.85)),
    ("StarCoder", MockCodeGenerator("StarCoder", 0.80)),
]

for name, model in models:
    ensemble.add_model(name, model)

# Generate with all models
results = asyncio.run(
    ensemble.generate_code_async("fibonacci function", "python")
)

# Get best result
best = ensemble.generate_code_ensemble(
    "fibonacci function", 
    voting_strategy="weighted_confidence"
)
```

### Cloud API Usage

```python
from api_integrations.cloud_generators import (
    CloudCodeGeneratorManager,
    CodeGenerationRequest,
    OpenAICodeGenerator
)
import asyncio

# Setup manager
manager = CloudCodeGeneratorManager()

# Add GPT-4 generator
if os.getenv("OPENAI_API_KEY"):
    gpt4 = OpenAICodeGenerator("gpt-4")
    manager.add_generator("gpt4", gpt4)

# Create request
request = CodeGenerationRequest(
    prompt="REST API endpoint for user authentication",
    language="python",
    style="clean",
    include_tests=True,
    framework="FastAPI"
)

# Generate code
result = asyncio.run(manager.generate_code(request))
print(f"Generated {result.tokens_used} tokens in {result.generation_time:.2f}s")
print(result.code)
```

### Code Evaluation

```python
from evaluation.code_evaluator import ComprehensiveCodeEvaluator, AnalysisLevel

# Create evaluator
evaluator = ComprehensiveCodeEvaluator()

# Evaluate code
result = evaluator.evaluate_code(
    code=your_generated_code,
    language="python",
    analysis_level=AnalysisLevel.COMPREHENSIVE
)

print(f"Quality Score: {result.overall_score}/100")
print(f"Issues Found: {len(result.issues)}")
for recommendation in result.recommendations:
    print(f"💡 {recommendation}")
```

## 🎛️ Configuration

### Model Configuration

```python
# Advanced model with custom settings
generator = AdvancedCodeGenerator(
    model_type=ModelType.CODE_LLAMA_13B,
    use_quantization=True,
    use_flash_attention=True,
    load_in_4bit=True,
    device_map="auto"
)

# Setup LoRA for fine-tuning
generator.setup_lora_fine_tuning(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05
)
```

### Generation Configuration

```python
from models.advanced_generator import GenerationConfig

config = GenerationConfig(
    max_new_tokens=1024,
    temperature=0.1,      # Lower = more deterministic
    top_p=0.9,           # Nucleus sampling
    top_k=50,            # Top-k sampling
    repetition_penalty=1.1,
    do_sample=True,
    num_beams=1,
    early_stopping=True
)

code = generator.generate_code(
    prompt="your prompt",
    config=config
)
```

## 🔧 API Reference

### AdvancedCodeGenerator

Main class for modern code generation with optimizations.

#### Methods:
- `generate_code(prompt, language, config, system_prompt)` - Generate code from prompt
- `generate_function(name, description, parameters, return_type)` - Generate specific function
- `generate_class(name, description, methods)` - Generate complete class
- `setup_lora_fine_tuning(r, lora_alpha, target_modules)` - Setup LoRA adaptation

### EnsembleCodeGenerator

Ensemble system for combining multiple models.

#### Methods:
- `add_model(name, model, weight)` - Add model to ensemble
- `generate_code_async(prompt, language)` - Async generation with all models
- `generate_code_ensemble(prompt, voting_strategy)` - Generate with voting
- `get_model_performance_stats()` - Get performance metrics

### CloudCodeGeneratorManager

Manager for cloud-based API integrations.

#### Methods:
- `add_generator(name, generator)` - Add cloud generator
- `generate_code(request, generator_name)` - Generate with specific model
- `generate_with_fallback(request, generator_names)` - Generate with fallbacks
- `compare_generators(request)` - Compare multiple generators

### ComprehensiveCodeEvaluator

Advanced code quality evaluation system.

#### Methods:
- `evaluate_code(code, language, analysis_level)` - Full evaluation
- Returns `EvaluationResult` with quality metrics, issues, and recommendations

## 🌟 Advanced Features

### Quantization Support

Reduce memory usage while maintaining quality:

```python
# 4-bit quantization (most memory efficient)
generator = AdvancedCodeGenerator(
    model_type=ModelType.CODE_LLAMA_13B,
    load_in_4bit=True,
    use_quantization=True
)

# 8-bit quantization (balance of quality and efficiency)
generator = AdvancedCodeGenerator(
    model_type=ModelType.STARCODER,
    load_in_8bit=True,
    use_quantization=True
)
```

### Flash Attention

Optimize attention mechanisms for speed:

```python
generator = AdvancedCodeGenerator(
    model_type=ModelType.CODE_LLAMA,
    use_flash_attention=True  # Significantly faster inference
)
```

### Custom Prompt Formatting

Different models use different prompt formats:

```python
# Automatic formatting based on model
code = generator.generate_code(
    prompt="create a web scraper",
    system_prompt="You are an expert Python developer"
)

# Models automatically format prompts:
# - LLaMA: [INST] format
# - WizardCoder: ### Instruction format  
# - StarCoder: # Task format
```

## 🧪 Examples and Demos

### Run Built-in Demos

```bash
# Test advanced generator
python models/advanced_generator.py

# Test ensemble system
python models/ensemble_generator.py

# Test cloud APIs (requires API keys)
python api_integrations/cloud_generators.py

# Test code evaluation
python evaluation/code_evaluator.py
```

### Custom Example Scripts

Check the `examples/` directory for:
- Basic code generation workflows
- Advanced ensemble usage patterns
- API integration examples
- Evaluation pipeline examples

## 📊 Performance Benchmarks

### Model Comparison

| Model | Size | Speed | Quality | Memory |
|-------|------|-------|---------|---------|
| CodeT5-Base | 220M | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| CodeLlama-7B | 7B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| StarCoder-15B | 15B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| GPT-4 (API) | - | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### Generation Speed
- **Local Models**: 10-50 tokens/second (depending on hardware)
- **Cloud APIs**: 5-20 tokens/second (network dependent)
- **Ensemble**: Parallel processing reduces effective time

## 🔒 Security Considerations

### API Key Safety
- Store API keys in environment variables
- Use `.env` files for local development
- Never commit API keys to version control
- Consider using key management services for production

### Generated Code Security
- Always review generated code before use
- Use the built-in security analyzer for vulnerability detection
- Be cautious with code that makes system calls or handles sensitive data
- Test generated code thoroughly before deployment

## 🚨 Troubleshooting

### Common Issues

**Out of Memory Errors:**
```python
# Use quantization
generator = AdvancedCodeGenerator(
    model_type=ModelType.CODE_LLAMA,
    load_in_4bit=True  # Reduces memory usage significantly
)
```

**Slow Generation:**
```python
# Enable optimizations
generator = AdvancedCodeGenerator(
    model_type=ModelType.STARCODER,
    use_flash_attention=True,  # Faster attention
    device_map="auto"          # Optimal device placement
)
```

**API Errors:**
```bash
# Check API keys
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# Test API connectivity
python -c "import openai; print(openai.__version__)"
```

**Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check Python version
python --version  # Should be 3.8+
```

### Performance Optimization

1. **GPU Setup**: Ensure CUDA is properly installed
2. **Memory**: Use quantization for large models
3. **Batch Processing**: Process multiple requests together
4. **Caching**: Cache model loading for repeated use

## 🛣️ Roadmap

### Upcoming Features
- [ ] **Fine-tuning Pipeline**: Automated fine-tuning on custom datasets
- [ ] **Code Completion**: Real-time code completion capabilities
- [ ] **Multi-language Support**: Extended language support beyond current set
- [ ] **Plugin System**: Extensible plugin architecture
- [ ] **Advanced Evaluation**: Runtime performance testing and profiling
- [ ] **Code Explanation**: Detailed code explanation and documentation generation

### Performance Improvements
- [ ] **Model Optimization**: Further quantization and pruning techniques
- [ ] **Distributed Inference**: Multi-GPU and multi-node support
- [ ] **Streaming Generation**: Real-time streaming of generated code
- [ ] **Smart Caching**: Intelligent result caching system

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** changes: `git commit -m 'Add feature'`
4. **Push** to branch: `git push origin feature-name`
5. **Submit** a pull request

### Development Setup

```bash
# Clone for development
git clone <repository-url>
cd gen

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black .
isort .

# Type checking
mypy models/ api_integrations/ evaluation/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for the transformers library and model hosting
- **OpenAI** for GPT models and API
- **Anthropic** for Claude models
- **Meta** for CodeLlama models
- **BigCode** for StarCoder models
- **Salesforce** for CodeT5 models
- **Microsoft** for WizardCoder models
- **Gradio** for the web interface framework

## 📞 Support

- **Documentation**: Check this README and inline code documentation
- **Issues**: Open an issue on GitHub for bug reports
- **Discussions**: Use GitHub Discussions for questions and feature requests
- **Email**: [Contact email if available]

## 📈 Statistics

![GitHub stars](https://img.shields.io/github/stars/username/repo.svg?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/repo.svg?style=social)
![GitHub issues](https://img.shields.io/github/issues/username/repo.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/username/repo.svg)

---

<div align="center">

**🚀 Built with modern AI • ⚡ Powered by transformers • 🌟 Made for developers**

[Website](https://your-website.com) • [Documentation](https://docs.your-website.com) • [Examples](./examples/) • [API Reference](./docs/api.md)

</div>