#!/bin/bash
# Git Commit Script for Download Options Feature
# Run this script to commit all changes

echo "🔍 Checking git status..."
git status

echo ""
echo "📝 Adding files to staging area..."

# Add modified files
git add README.md
git add demo/demo_gradio.py

# Add new files
git add dots_ocr/utils/merge_utils.py
git add scripts/

# Remove deleted files
git rm merge_files/README_MERGE_TOOL.md
git rm merge_files/tool_merge.py
git rm check_images.py

echo ""
echo "✅ Files staged successfully!"
echo ""
echo "📊 Changes to be committed:"
git status

echo ""
echo "💾 Creating commit..."
git commit -m "feat: Add Download Options feature with flexible export controls

✨ Features Added:
- Download Options UI with format (MD/JSON) and scope (Individual/Merged) selection
- Smart document merging with hyphenation removal
- Custom ZIP package generation based on user preferences
- Integrated merge functionality into main Gradio UI

📦 New Files:
- dots_ocr/utils/merge_utils.py: Merge and package creation utilities
- scripts/: Utility scripts folder with check_images.py and test_sorting.py

🗑️ Removed:
- merge_files/: Standalone merge tool (functionality integrated into UI)
- check_images.py: Moved to scripts/ folder

📝 Updated:
- demo/demo_gradio.py: Added download options UI and event handlers
- README.md: Documented new Download Options feature

🎯 Benefits:
- Users can choose exactly what to download (format + scope)
- No need for separate merge tool
- Seamless workflow within Gradio UI
- Clean merged documents without extra metadata"

echo ""
echo "✅ Commit created successfully!"
echo ""
echo "🚀 To push to remote, run:"
echo "   git push origin main"
