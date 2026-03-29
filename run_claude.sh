# Read conversation file and send to Claude with BRD prompt
# Save the generated output into brd.md
#Conversation file -> (Pipe)->Claude + Prompt -> Generated BRD -> Saved to brd.md
cat Input/Requirements_Conversation.txt | claude -p "$(cat Prompts/1.brd_prompt.txt)" > Docs/brd.md
sleep 10
cat Docs/brd.md | claude -p "$(cat Prompts/2.Modules_prompt.txt)" > Docs/modules.md
sleep 10
cat Docs/modules.md | claude -p "$(cat Prompts/3.TechArc_prompt.txt)" > Docs/TechArc.md
sleep 10
cat Docs/modules.md | claude -p "$(cat Prompts/4.Resource_prompt.txt)" > Docs/Resource_Allot.md
sleep 10
cat Docs/TechArc.md | claude -p "$(cat Prompts/5.Devpipe_prompt.txt)" > Docs/DevPipeline.md
sleep 10
cat Docs/modules.md | claude -p "$(cat Prompts/6.Testing_prompt.txt)" > Docs/TestCases.md
sleep 10
cat Docs/TechArc.md | claude -p "$(cat Prompts/7.ProTip_prompt.txt)" > Docs/Proj_Optimization.md
sleep 10
PANDOC="${PANDOC:-/c/Users/Admin/AppData/Local/Pandoc/pandoc.exe}"
for f in Docs/*.md; do "$PANDOC" "$f" -o "${f%.md}.docx"; done
echo "Project documents created successfully"
