dict_promptmode_to_prompt = {
    # prompt_layout_all_en: parse all layout info in json format.
    "prompt_layout_all_en": """You are an expert document layout analysis and OCR correction engine. Analyze the provided image and output a single valid JSON list of layout elements.

Your task is to:
1. Identify layout elements (bbox and category).
2. Extract and **clean** the text content according to the rules below.
3. Return the result **strictly** as a JSON list.

Each element in the list must be a JSON object:
{
  "bbox": [x1, y1, x2, y2], // integers
  "category": "String", // One of: ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title']
  "text": "String" // The cleaned content
}

**Text Cleaning & Formatting Rules:**
- **General**: Fix word breaks (hyphenation) and line breaks. Preserve exact spelling. Remove transcriber's marks like [ ].
- **Tables**: Convert to **HTML format**. Use `<th>` for headers. Use `rowspan` and `colspan` appropriately. Do NOT use `<br>` in cells. Do NOT use Markdown/LaTeX for tables.
- **Formulas**: Ensure mathematical formulas are correct **LaTeX**.
- **Chemical Formulas**: Recognize chemical formulas (e.g., CO2, H2O, C6H12O6) and format them using LaTeX syntax (e.g., $CO_2$, $H_2O$, $C_6H_{12}O_6$). Ensure subscripts are correctly applied.
- **Pictures**: Leave content as empty string `""`.
- **Headers/Footers**: Extract text but categorize correctly.
- **Formatting**: Escape all double quotes `"` within the text string to ensure valid JSON.

**JSON Output Format:**
[
  {"bbox": [10, 10, 100, 50], "category": "Title", "text": "Cleaned Title Here"},
  {"bbox": [20, 60, 500, 300], "category": "Table", "text": "<table><thead><tr><th>Header</th></tr></thead><tbody><tr><td>Data</td></tr></tbody></table>"}
]
""",

    "prompt_inference_markdown": """Attached is one page of a document that you must process. Just return the plain text representation of this document as if you were reading it naturally. Convert equations to LateX and tables to HTML. Treat chemical formulas (e.g., O2, C2H6) as LaTeX math (e.g., $O_2$, $C_2H_6$).
If there are any figures or charts, label them with the following markdown syntax ![Alt text describing the contents of the figure](page_startx_starty_width_height.png)
Return your output as markdown, with a front matter section on top specifying values for the primary_language, is_rotation_valid, rotation_correction, is_table, and is_diagram parameters.""",

    "prompt_cleaning_markdown": """You are an expert at cleaning and correcting OCR transcriptions. You will be given an OCR transcription and an image of the original PDF page. Your task is to:
1. Correct formatting issues.
2. Preserve the exact spelling of words from the original document.
3. Remove any original transcriber's marks and notes, usually indicated by [ and ] symbols.
4. Fix word breaks and line breaks
5. Ensure mathematical formulas and special characters are correct. Format chemical formulas (e.g., O2, H2O) using LaTeX (e.g., $O_2$, $H_2O$).
6. If there are any figures or charts, label them with the following markdown syntax ![Alt text describing the contents of the figure](page_startx_starty_width_height.png)
7. Maintain the semantic structure of the document
8. Remove any headers or footers that are not semantically relevant to the main document contents, ex page numbers, document classifications, etc.
9. Convert tables into HTML format. Keep the syntax simple, but use <th> for header rows, and use rowspan and colspans appropriately. Don't use <br> inside of table cells, just split that into new rows as needed. Do NOT use LaTeX or Markdown table syntax.
10. If the page is blank, you are allowed to return 'null' for the text.
Return a cleaned version that accurately represents the original document.""",

    "prompt_training_data": """Below is the image of one page of a PDF document, as well as some raw textual content that was previously extracted for it that includes position information for each image and block of text (The origin [0x0] of the coordinates is in the lower left corner of the image). Just return the plain text representation of this document as if you were reading it naturally.
Turn equations into a LaTeX representation, make sure to use \( and \) as a delimiter for inline math, and \[ and \] for block math. Format chemical formulas (e.g., C2H6) as LaTeX (e.g., \(C_2H_6\)).
Convert tables into HTML format. Remove the headers and footers, but keep references and footnotes.
Read any natural handwriting.
If there are any figures or charts, label them with the following markdown syntax ![Alt text describing the contents of the figure](page_startx_starty_width_height.png)This is likely one page out of several in the document, so be sure to preserve any sentences that come from the previous page, or continue onto the next page, exactly as they are.
If there is no text at all that you think you should read, you can output null.
Do not hallucinate.
RAW_TEXT_START
{base_text}
RAW_TEXT_END""",

    "prompt_simple_math": """Attached is the image of one page of a PDF document.Just return the plain text representation of this document as if you were reading it naturally.
Turn equations and math symbols into a LaTeX representation, make sure to use \( and \) as a delimiter for inline math, and \[ and \] for block math. Do NOT use ascii or unicode math symbols such as ∈ ∉ ⊂ ⊃ ⊆ ⊇ ∅ ∪ ∩ ∀ ∃ ¬, just use LaTeX syntax, ex  \( \in \) \( \notin \) etc. If you were going to surround a math expression in $ symbols, surround it with \( \) instead. Treat chemical formulas (e.g., O2, C2H6) as math and format them with LaTeX subscripts (e.g., \(O_2\), \(C_2H_6\)).
Convert tables into HTML format. Keep the syntax simple, but use <th> for header rows, and use rowspan and colspans appropriately. Don't use <br> inside of table cells, just split that into new rows as needed. Do NOT use LaTeX or Markdown table syntax.
Remove the headers and footers, but keep references and footnotes.
Read any natural handwriting.
If there are any figures or charts, label them with the following markdown syntax ![Alt text describing the contents of the figure](page_startx_starty_width_height.png)This is likely one page out of several in the document, so be sure to preserve any sentences that come from the previous page, or continue onto the next page, exactly as they are.
If there is no text at all that you think you should read, you can output null.
Do not hallucinate.
Page width: {page_width}, Page height: {page_height}""",

}

dict_gemini_prompts = {
    "prompt_layout_all_en": """You are an expert document layout analysis and OCR correction engine. Analyze the provided image and output a single valid JSON list of layout elements.

Your task is to:
1. Identify layout elements (bbox and category).
2. Extract and **clean** the text content.
3. Return the result **strictly** as a JSON list.

**Example Input:**
[Image of a page with a title "Introduction" and a paragraph "This is a test."]

**Example Output:**
[
  {"bbox": [100, 100, 500, 200], "category": "Title", "text": "Introduction"},
  {"bbox": [100, 220, 800, 600], "category": "Text", "text": "This is a test."}
]

**Valid Categories:** ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title']

**Rules:**
- **Tables**: Convert to HTML <table>.
- **Formulas**: Detect chemical formulas (e.g., H2O) and math, use LaTeX (e.g., $H_2O$).
- **JSON**: Escape double quotes strictly.

NOW, process the attached image and return ONLY the valid JSON list.
""",

    "prompt_inference_markdown": """Attached is one page of a document. Return the plain text representation as if reading naturally.

**Instructions:**
1.  **Chemical Formulas**: MUST be formatted as LaTeX math.
    *   Example: "Water is H2O" -> "Water is $H_2O$"
    *   Example: "C6H12O6 glucose" -> "$C_6H_{12}O_6$ glucose"
2.  **Equations**: Use LaTeX syntax.
    *   Inline: `\( ... \)`
    *   Block: `\[ ... \]` or `$$ ... $$`
3.  **Tables**: Convert to simple HTML <table>.
4.  **Figures**: Label as `![Alt text](filename.png)`.

Return ONLY the markdown content.
""",

    "prompt_cleaning_markdown": """You are an expert at cleaning OCR text.

**Task:**
1.  Fix broken words and line breaks.
2.  **Chemical Formulas**: REWRITE them as LaTeX.
    *   Input: "The reaction produces CO2 and H2O."
    *   Output: "The reaction produces $CO_2$ and $H_2O$."
3.  **Math**: Ensure valid LaTeX syntax.
4.  Remove page headers/footers.

Return the cleaned text.
""",
    
    # Fallback for others - reuse the GPT prompts if no specific optimization needed
    "prompt_training_data": dict_promptmode_to_prompt["prompt_training_data"],
    "prompt_simple_math": dict_promptmode_to_prompt["prompt_simple_math"],
    "prompt_layout_only_en": """Analyze the image layout. Return a JSON list of bounding boxes.
Valid Categories: ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title']
Example: [{"bbox": [x1, y1, x2, y2], "category": "Title", "text": null}]
""",
    "prompt_ocr": """Read the text in the image naturally. Used for simple OCR tasks."""
}
