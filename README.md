# ⚡ LLM Router — System 1 vs. System 2 for AI

> *Not all questions deserve the same brain. This project makes sure they don't.*

Most AI apps send every single prompt — "hi" and "explain the thermodynamics of a black hole" — to the same expensive, slow model. That's like hiring a neurosurgeon to prescribe Tylenol.

**LLM Router fixes that.** It reads your prompt, classifies its complexity in milliseconds, and routes it to exactly the right model. Fast questions get fast answers. Hard questions get the heavy machinery. Automatically.

---

## 🧠 The Idea: Kahneman Meets LLMs

Psychologist Daniel Kahneman described human cognition as two systems:
- **System 1** — fast, instinctive, automatic
- **System 2** — slow, deliberate, analytical

This project applies the same architecture to AI inference:

| Your Prompt | Complexity | Routed To | Why |
|---|---|---|---|
| "Hey, what's up?" | Simple | Llama 3.1 8B ⚡ | No need to overthink a greeting |
| "Analyze the CAP theorem tradeoffs in distributed systems" | Complex | DeepSeek R1 70B 🧠 | This deserves real reasoning |

The router itself uses the *cheap* model to classify — because even the decision of "how hard is this?" doesn't need a genius.

---

## 🏗️ Architecture

```
User Prompt
    │
    ▼
┌─────────────────────────────┐
│        FastAPI Backend       │
│                             │
│  ┌──────────────────────┐   │
│  │  Complexity Router   │   │  ← Uses Llama 3.1 8B to classify
│  └──────────┬───────────┘   │
│             │               │
│      ┌──────┴──────┐        │
│      ▼             ▼        │
│  [Simple]      [Complex]    │
│  Llama 3.1     DeepSeekR1    │
│    8B ⚡         70B 🧠     │
└─────────────────────────────┘
    │
    ▼
Response + { model_used, complexity }
```

Everything runs through **Groq** — a hardware-accelerated inference provider that makes open-source models stupid fast. No GPU required on your end.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A free [Groq API key](https://console.groq.com) (takes 30 seconds)

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/llm-router.git
cd llm-router

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```
GROQ_API_KEY=gsk_your_key_here
```

### Run

```bash
uvicorn main:app --reload
```

Open `index.html` in your browser, paste your Groq key in the UI, and start chatting.

---

## 📁 Project Structure

```
llm-router/
│
├── main.py           # FastAPI server + routing logic
├── index.html        # Chat UI (zero dependencies, open directly)
├── requirements.txt  # Python dependencies
├── .env              # Your API key (never commit this)
└── .gitignore        # Keeps secrets out of GitHub
```

The entire backend is a single, readable `main.py`. No overcomplicated abstractions. No unnecessary frameworks. Just clean logic you can understand and extend.

---

## 🔌 API

### `POST /chat`

**Request:**
```json
{
  "message": "Explain gradient descent intuitively",
  "api_key": "gsk_..."
}
```

**Response:**
```json
{
  "message": "Imagine you're blindfolded on a hilly landscape...",
  "routed_to": "llama-3.3-70b-versatile",
  "complexity": "complex",
  "model_label": "Llama 3.3 70B 🧠 reasoning"
}
```

The response always tells you *which model handled it* and *why* — full transparency, no black boxes.

---

## 🌐 Deployment

This project is deployed on **Render**. The backend lives at a persistent URL; the frontend is a single HTML file that points to it.

To deploy your own instance:

1. Push to GitHub
2. Connect repo to [Render](https://render.com)
3. Add `GROQ_API_KEY` as an environment variable
4. Update `const API` in `index.html` to your Render URL
5. Done — your router is live

> ⚠️ **Heads up:** Render's free tier spins down after 15 minutes of inactivity. First request after idle may take ~30 seconds to wake up.

---

## 🛠️ Models Used

| Role | Model | Provider | Speed |
|---|---|---|---|
| Classifier + Simple | `llama-3.1-8b-instant` | Groq | ~100ms |
| Complex Reasoning | `DeepSeek r1 70b-versatile` | Groq | ~500ms |

Both are **fully open-source** models running on Groq's LPU (Language Processing Unit) hardware. No OpenAI. No vendor lock-in.

---

## 🔭 What's Next

A few directions this could go:

- **Scoring instead of binary** — rate complexity 1–10 and have 3+ model tiers
- **Cost tracking dashboard** — see exactly how much you're saving vs. always using the big model
- **Streaming responses** — start rendering output before the full response arrives
- **Custom routing rules** — override the classifier for specific topics or keywords
- **Multi-provider routing** — route to OpenAI, Anthropic, or Groq depending on the task type

---

## 💡 Why This Matters

The LLM industry has a dirty secret: **most tokens are wasted.** Enterprises run GPT-4 on queries that GPT-4o-mini would handle just fine. This router is a small proof-of-concept for a bigger idea — that intelligent infrastructure, not just intelligent models, is how we make AI efficient at scale.

---

## 📄 License

MIT — do whatever you want with it.

---

*Built with FastAPI, Groq, and the conviction that not every question needs a genius to answer it.*
