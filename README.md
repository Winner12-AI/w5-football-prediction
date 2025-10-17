# W-5 Football Prediction Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17367739.svg)](https://doi.org/10.5281/zenodo.17367739)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A research implementation of the **W-5 Multi-Agent AI Consensus Framework** for football match outcome prediction, as described in our academic paper published on Zenodo.

## 📄 Research Paper

This repository accompanies the research paper:

> **"A Multi-Agent AI Consensus Framework for Football Match Outcome Prediction: Integrating Large Language Models with Traditional Machine Learning"**
> 
> WINNER12 AI RESEARCH TEAM
> 
> Published on Zenodo: https://zenodo.org/records/17367739

The paper demonstrates that the W-5 framework achieves **85.9% prediction accuracy** on a large-scale simulated dataset, significantly outperforming traditional methods and individual AI models.

## 🎯 What is W-5?

The W-5 framework is a hybrid AI system that combines:

1. **Traditional Machine Learning** (XGBoost, LightGBM) for quantitative baseline predictions
2. **Large Language Models** (LLMs) for qualitative contextual analysis
3. **AI Consensus Mechanism** - a novel multi-agent system where diverse AI personas debate and synthesize predictions
4. **Meta-Learning Fusion** - intelligent integration of quantitative and qualitative insights

### Key Innovation: AI Consensus Mechanism

Unlike simple model ensembles, our AI Consensus Mechanism simulates an expert committee where multiple LLM agents with different personas (statistician, tactician, sentiment analyst, etc.) engage in structured debate to arrive at robust predictions.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Winner12-AI/w5-football-prediction.git
cd w5-football-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from src.models import BaselinePredictor
from src.consensus import AIConsensusEngine
from src.utils import load_sample_data

# Load sample data
match_data = load_sample_data('data/sample/demo_matches.csv')

# Step 1: Get baseline prediction
baseline = BaselinePredictor()
baseline_probs = baseline.predict(match_data)

# Step 2: Run AI consensus (requires API keys)
consensus = AIConsensusEngine(num_agents=3)
consensus_result = consensus.debate(match_data)

# Step 3: Fuse predictions
final_prediction = consensus.fuse_with_baseline(
    baseline_probs, 
    consensus_result
)

print(f"Predicted outcome: {final_prediction}")
```

## 📊 Performance Benchmarks

Based on our research paper evaluation:

| Model | Accuracy | Brier Score | Log Loss |
|-------|----------|-------------|----------|
| ELO Rating | 51.2% | 0.231 | 0.985 |
| XGBoost Only | 58.1% | 0.205 | 0.899 |
| Best Single LLM | 73.2% | 0.189 | 0.721 |
| **W-5 Full Model** | **85.9%** | **0.152** | **0.673** |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    W-5 Framework                         │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Data Ingestion                                │
│    ├─ Historical match data                             │
│    ├─ Player statistics                                 │
│    ├─ Market sentiment                                  │
│    └─ News & media                                      │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Feature Engineering                           │
│    ├─ Quantitative features (structured)                │
│    └─ Qualitative features (unstructured)               │
├─────────────────────────────────────────────────────────┤
│  Layer 3: AI Core                                       │
│    ├─ Baseline ML Models (XGBoost, LightGBM)           │
│    ├─ LLM Cluster (Multi-agent)                        │
│    └─ AI Consensus Mechanism ⭐                         │
├─────────────────────────────────────────────────────────┤
│  Layer 4: Meta-Learning Fusion                          │
│    └─ Intelligent synthesis of predictions              │
├─────────────────────────────────────────────────────────┤
│  Layer 5: Output                                        │
│    ├─ Match outcome probabilities                       │
│    ├─ Confidence scores                                 │
│    └─ Explainable factors                               │
└─────────────────────────────────────────────────────────┘
```

## 📁 Repository Structure

```
w5-football-prediction/
├── src/                      # Core framework implementation
│   ├── models/              # Baseline ML models
│   │   ├── baseline.py      # XGBoost/LightGBM implementations
│   │   └── meta_learner.py  # Meta-learning fusion layer
│   ├── consensus/           # AI consensus mechanism
│   │   ├── agent.py         # Individual LLM agent
│   │   ├── debate.py        # Debate orchestration
│   │   └── synthesis.py     # Consensus synthesis
│   ├── data/                # Data processing
│   │   ├── loader.py        # Data loading utilities
│   │   └── features.py      # Feature engineering
│   └── utils/               # Helper functions
├── examples/                # Usage examples
│   ├── basic_prediction.py  # Simple prediction example
│   └── full_pipeline.py     # Complete W-5 pipeline
├── notebooks/               # Jupyter tutorials
│   └── tutorial.ipynb       # Step-by-step guide
├── data/                    # Sample datasets
│   └── sample/             # Demo data (synthetic)
├── tests/                   # Unit tests
├── configs/                 # Configuration files
├── docs/                    # Documentation
│   ├── api.md              # API reference
│   ├── setup.md            # Setup guide
│   └── contributing.md     # Contribution guidelines
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md               # This file
```

## 🔧 Configuration

The framework requires API keys for LLM access. Create a `.env` file:

```env
# OpenAI API (for GPT models)
OPENAI_API_KEY=your_key_here

# Anthropic API (for Claude models)
ANTHROPIC_API_KEY=your_key_here

# Google API (for Gemini models)
GOOGLE_API_KEY=your_key_here

# Optional: Other LLM providers
XAI_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
```

**Note**: The framework can work with fewer LLMs (minimum 3 recommended for consensus).

## 📚 Documentation

- **[Setup Guide](docs/setup.md)** - Detailed installation and configuration
- **[API Reference](docs/api.md)** - Complete API documentation
- **[Tutorial Notebook](notebooks/tutorial.ipynb)** - Interactive walkthrough
- **[Research Paper](https://zenodo.org/records/17367739)** - Full methodology and evaluation

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_consensus.py

# Run with coverage
pytest --cov=src tests/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/contributing.md) for details.

Areas where we especially appreciate help:
- Adding new baseline models
- Improving documentation
- Creating tutorials and examples
- Bug fixes and performance optimizations

## 📖 Citation

If you use this framework in your research, please cite our paper:

```bibtex
@article{w5_football_prediction_2025,
  title={A Multi-Agent AI Consensus Framework for Football Match Outcome Prediction: Integrating Large Language Models with Traditional Machine Learning},
  author={WINNER12 AI RESEARCH TEAM},
  journal={Zenodo Preprint},
  year={2025},
  doi={10.5281/zenodo.17367739},
  url={https://zenodo.org/records/17367739}
}
```

## 🔗 Related Projects

- **[WINNER12](https://winner12.ai)** - Commercial football prediction platform inspired by this research
- **[Zenodo Paper](https://zenodo.org/records/17367739)** - Full academic publication

## ⚠️ Disclaimer

This is a **research project** for academic and educational purposes. The framework is provided "as-is" without warranties. It is not intended for commercial betting or gambling applications. 

For production-grade predictions and commercial use, please visit [WINNER12](https://winner12.ai).

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- **Commercial Applications**: [WINNER12 Website](https://winner12.ai)
- **Issues & Bugs**: [GitHub Issues](https://github.com/Winner12-AI/w5-football-prediction/issues)

---

**⭐ Star this repository if you find it useful!**

**🔬 Built with passion for AI research and sports analytics**

