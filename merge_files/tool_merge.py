import gradio as gr
import zipfile
import os
import re
import shutil
import subprocess
import platform

# --- CẤU HÌNH ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = os.path.join(CURRENT_DIR, "workspace_temp")
EXTRACT_DIR = os.path.join(WORKING_DIR, "extracted")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "KET_QUA")
FINAL_MD_NAME = "KET_QUA_GOP.md"

# --- HÀM HỖ TRỢ ---
def open_folder(path):
    """Tự động mở thư mục trên Windows/Mac/Linux"""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except:
        pass

def numerical_sort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def process_zip_file(zip_file_obj):
    logs = []
    def add_log(text):
        logs.append(f"{text}")
        return "\n".join(logs)

    # 1. Clean up & Create directories
    if os.path.exists(WORKING_DIR):
        shutil.rmtree(WORKING_DIR)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    os.makedirs(EXTRACT_DIR)

    if zip_file_obj is None:
        return None, "⚠️ Please select a ZIP file to begin", 0, ""

    # 2. Extract
    try:
        add_log("🔄 Extracting ZIP file...")
        with zipfile.ZipFile(zip_file_obj, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
    except Exception as e:
        return None, f"❌ Extraction error: {str(e)}", 0, ""

    # 3. Find .md files
    md_files = []
    for root, dirs, files_in_dir in os.walk(EXTRACT_DIR):
        for file in files_in_dir:
            if file.endswith(".md") and "page_" in file:
                full_path = os.path.join(root, file)
                md_files.append(full_path)

    md_files.sort(key=numerical_sort)

    if not md_files:
        return None, "❌ No 'page_X.md' files found in ZIP", 0, ""

    add_log(f"✅ Found {len(md_files)} Markdown pages")
    add_log(f"📝 Merging content...")

    # 4. Merge content
    merged_content = "# MERGED DOCUMENT\n\n"
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                text = infile.read()
                text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
                merged_content += f"\n\n{text}\n\n---\n\n"
        except:
            pass

    # 5. Save file
    final_path = os.path.join(OUTPUT_DIR, FINAL_MD_NAME)
    with open(final_path, 'w', encoding='utf-8') as f:
        f.write(merged_content)
    
    file_size = os.path.getsize(final_path) / 1024
    
    add_log(f"✅ Merge successful!")
    add_log(f"📁 Location: {final_path}")
    add_log(f"📊 Size: {file_size:.1f} KB")
    
    open_folder(OUTPUT_DIR)
    
    success_msg = f"🎉 **Complete!** Successfully merged {len(md_files)} pages"
    
    return final_path, "\n".join(logs), len(md_files), success_msg

# --- GIAO DIỆN ---
custom_css = """
#header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 2rem;
}

#header h1 {
    font-size: 2.5rem;
    margin: 0;
    font-weight: 700;
}

#header p {
    font-size: 1.1rem;
    margin-top: 0.5rem;
    opacity: 0.95;
}

#submit_btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    font-size: 1.2rem;
    font-weight: 600;
    padding: 1rem 2rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

#submit_btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.stats-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin: 1rem 0;
}

.stats-number {
    font-size: 3rem;
    font-weight: 700;
    color: #667eea;
    margin: 0;
}

.stats-label {
    font-size: 1rem;
    color: #666;
    margin-top: 0.5rem;
}

#success_msg {
    text-align: center;
    font-size: 1.2rem;
    padding: 1rem;
}

.upload-area {
    border: 3px dashed #667eea;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    background: #f8f9ff;
    transition: all 0.3s ease;
}

.upload-area:hover {
    background: #f0f2ff;
    border-color: #764ba2;
}

#logs_box {
    font-family: 'Monaco', 'Menlo', monospace;
    background: #1e1e1e;
    color: #d4d4d4;
    border-radius: 8px;
    padding: 1rem;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="Markdown Merger Pro") as demo:
    
    # Header
    with gr.Row(elem_id="header"):
        gr.HTML("""
            <div>
                <h1>📚 Markdown Merger Pro</h1>
                <p>Professional Markdown Merging Tool - Fast & Convenient</p>
            </div>
        """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📤 Upload ZIP File")
            input_file = gr.File(
                label="Drag & drop or click to select file",
                file_types=[".zip"],
                type="filepath",
                elem_classes="upload-area"
            )
            
            gr.Markdown("""
            #### 💡 Instructions:
            1. Select ZIP file containing `page_X.md` files
            2. Click **Start Processing** button
            3. Wait for completion
            4. Download the result file
            """)
            
            submit_btn = gr.Button(
                "🚀 Start Processing",
                elem_id="submit_btn",
                size="lg"
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Results")
            
            success_msg = gr.Markdown("", elem_id="success_msg")
            
            with gr.Row():
                page_count = gr.Number(
                    label="Pages merged",
                    value=0,
                    interactive=False,
                    container=True
                )
            
            output_file = gr.File(
                label="📥 Download result file",
                interactive=False
            )
            
            gr.Markdown("### 📋 Processing Details")
            logs_box = gr.Textbox(
                label="",
                lines=8,
                max_lines=10,
                elem_id="logs_box",
                show_label=False
            )
    
    # Footer
    with gr.Row():
        gr.Markdown("""
        ---
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>💻 Developed with Python + Gradio | ⚡ Fast & secure local processing</p>
        </div>
        """)
    
    # Event handlers
    submit_btn.click(
        fn=process_zip_file,
        inputs=input_file,
        outputs=[output_file, logs_box, page_count, success_msg]
    )

if __name__ == "__main__":
    print("🚀 Starting Markdown Merger Pro...")
    demo.launch(inbrowser=True)
