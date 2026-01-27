<div align="center">

<p align="center">
    <img src="https://raw.githubusercontent.com/rednote-hilab/dots.ocr/master/assets/logo.png" width="300"/>
<p>

<h1 align="center">
dots.ocr: Document Layout Parsing with LLMs (API Version)
</h1>

<div align="center">
  <p><strong>Supports Google Gemini & OpenAI GPT-4o Integration</strong></p>
</div>

</div>

## Introduction

**dots.ocr** is a streamlined document parser that leverages powerful Vision-Language Models (VLMs) to analyze document layouts and extract structured content. This version is optimized for API usage, supporting:

*   **Google Gemini** (e.g., `gemini-2.0-flash-exp`)
*   **OpenAI GPT-4o**

It provides a user-friendly Web UI via Gradio for interactive document parsing.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rednote-hilab/dots.ocr.git
    cd dots.ocr
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements_lite.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

### 1. Web Interface (Gradio)

Start the user-friendly web interface:

```bash
python demo/demo_gradio.py
```

Open your browser at `http://localhost:7860`.

**Key Features:**
*   **Upload PDF/Image:** Drag and drop your documents.
*   **Model Selection:** Choose between Gemini and GPT-4o engines.
*   **Advanced Prompts:** Select specialized prompts for Markdown extraction, Layout analysis, or Data cleaning.
*   **Rate Limiting Control:** Adjustable delay settings to prevent API rate limits.
*   **Interactive Preview:** View parsed results and original layout side-by-side.
*   **Export:** Download results as JSON or Markdown.

### 2. Command Line Interface (CLI)

You can also run the parser directly from the terminal, which is useful for batch processing or automation.

**Basic Command:**
```bash
python -m dots_ocr.parser input.pdf --output ./output
```

**Common Arguments:**
*   `--model_name`: Model to use (default: `rednote-hilab/dots.ocr`). Use `gemini-pro`, `gpt-4o`, etc.
*   `--num_thread`: Number of concurrent pages to process (default: `3`).
*   `--request_delay`: Delay in seconds between API requests (default: `2.0`).

## Optimization & Rate Limiting

When using API-based models (Gemini, OpenAI), you may encounter `429 Rate Limit` errors. `dots.ocr` provides built-in tools to handle this:

1.  **Request Delay (`--request_delay` / Web UI Setting)**:
    *   Adds a pause before every API call.
    *   **Recommendation:** Start with `2.0` seconds. Increase to `5.0` or higher if you see frequent 429 errors.
    
2.  **Concurrency (`--num_thread`)**:
    *   Controls how many pages are processed in parallel.
    *   **Recommendation:** Reduce this value (e.g., to `1`) if rate limits persist, as processing multiple pages simultaneously consumes quota faster.

3.  **Automatic Retries**:
    *   The system automatically uses **Exponential Backoff** (waiting longer after each failure) with **Jitter** (randomized wait times) to recover from temporary rate limits.


