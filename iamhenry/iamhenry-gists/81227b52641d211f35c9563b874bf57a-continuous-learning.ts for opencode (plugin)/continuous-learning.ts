/**
 * Continuous Learning Plugin
 *
 * Analyzes coding sessions for learnings and proposes updates to instruction files.
 * Triggers on session.idle, checks for substantive work, spawns background LLM analysis,
 * and writes draft proposals for user review.
 *
 * TODO v1.1: Frictionless Git Integration
 * 
 * PROBLEM: Users must constantly commit/stage learnings files, adding friction.
 * 
 * SOLUTION: Add config option to auto-add learnings directory to .gitignore
 * 
 * IMPLEMENTATION:
 * 1. Add config option: { "gitIgnore": true } (default: true)
 * 2. On first draft creation, check if .gitignore exists
 * 3. If gitIgnore enabled and learnings path not in .gitignore, append it
 * 4. Create learnings/ directory at runtime if it doesn't exist (remove .gitkeep dependency)
 * 5. Learnings stay local-only, no commit noise
 * 
 * CONFIG EXAMPLE:
 * {
 *   "model": "opencode/big-pickle",
 *   "toast": true,
 *   "gitIgnore": true  // NEW: auto-add learnings/ to .gitignore
 * }
 */

import type { Plugin } from "@opencode-ai/plugin"
import fs from "fs"
import path from "path"

// Track substantive work per session
const sessionState = new Map<string, {
  hasSubstantiveWork: boolean
  skillsUsed: Set<string>
}>()

/**
 * Get or create session state
 */
function getSessionState(sessionID: string) {
  if (!sessionState.has(sessionID)) {
    sessionState.set(sessionID, {
      hasSubstantiveWork: false,
      skillsUsed: new Set()
    })
  }
  return sessionState.get(sessionID)!
}

/**
 * Clean up old session state (prevent memory leak)
 */
function cleanupOldSessions() {
  // Keep only last 10 sessions
  const sessions = Array.from(sessionState.keys())
  if (sessions.length > 10) {
    const toRemove = sessions.slice(0, sessions.length - 10)
    toRemove.forEach(id => sessionState.delete(id))
  }
}

/**
 * Extract short session ID for file naming/matching
 */
function getShortSessionID(sessionID: string): string {
  return sessionID.slice(-8)
}

/**
 * Map learning target to appropriate file
 */
function resolveTargetFile(target: string, skillsUsed: Set<string>, directory: string): string {
  const normalized = target.toLowerCase()
  
  // Check for skill-specific targets
  for (const skill of skillsUsed) {
    if (normalized.includes(skill.toLowerCase())) {
      const skillPath = path.join(directory, `.claude/skills/${skill}/SKILL.md`)
      if (fs.existsSync(skillPath)) return skillPath
    }
  }
  
  // Map by content area
  if (normalized.includes("convex") || normalized.includes("backend")) {
    const convexPath = path.join(directory, "convex/CLAUDE.md")
    if (fs.existsSync(convexPath)) return convexPath
    const docsConvexPath = path.join(directory, "docs/convex/CLAUDE.md")
    if (fs.existsSync(docsConvexPath)) return docsConvexPath
  }
  
  if (normalized.includes("route") || normalized.includes("routing")) {
    const routesPath = path.join(directory, "src/routes/CLAUDE.md")
    if (fs.existsSync(routesPath)) return routesPath
  }
  
  if (normalized.includes("ui") || normalized.includes("component")) {
    const uiPath = path.join(directory, "src/ui/CLAUDE.md")
    if (fs.existsSync(uiPath)) return uiPath
  }
  
  // Default to root CLAUDE.md
  return path.join(directory, "CLAUDE.md")
}

/**
 * Find existing draft file for this session
 */
function findSessionDraft(learningsDir: string, sessionID: string): string | null {
  const shortSessionID = getShortSessionID(sessionID)
  
  try {
    const files = fs.readdirSync(learningsDir)
    const sessionFile = files.find(f => f.includes(shortSessionID) && f.endsWith(".md"))
    return sessionFile ? path.join(learningsDir, sessionFile) : null
  } catch {
    return null
  }
}

/**
 * Generate a URL-safe slug from text
 */
function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 30)
}

/**
 * Generate draft filename with session ID and topic
 */
function generateDraftFilename(sessionID: string, learnings: Array<{ title: string }>): string {
  const now = new Date()
  const date = now.toISOString().split("T")[0]
  const shortSessionID = getShortSessionID(sessionID)
  
  // Extract topic from first learning title
  const topic = learnings.length > 0 ? slugify(learnings[0].title) : "session"
  
  return `${date}-${shortSessionID}-${topic}.md`
}

/**
 * Format learnings into draft markdown
 */
function formatDraft(
  learnings: Array<{
    title: string
    category: string
    target: string
    evidence: string
    instead_of: string
    do_this: string
  }>,
  sessionID: string,
  directory: string,
  skillsUsed: Set<string>
): string {
  const now = new Date().toISOString()
  
  // Group by category
  const byCategory: Record<string, typeof learnings> = {
    "Anti-Patterns": [],
    "Missing Context": [],
    "Success Patterns": [],
  }
  
  learnings.forEach(l => {
    const cat = l.category in byCategory ? l.category : "Missing Context"
    byCategory[cat].push(l)
  })
  
  // Build markdown
  let md = `---
created: ${now}
session: ${sessionID}
status: pending
applied: []
dismissed: []
---

`
  
  let learningId = 1
  
  for (const [category, items] of Object.entries(byCategory)) {
    if (items.length === 0) continue
    
    md += `## ${category}\n\n`
    
    for (const item of items) {
      const resolvedTarget = resolveTargetFile(item.target, skillsUsed, directory)
      const relativePath = path.relative(directory, resolvedTarget)
      
      md += `### L${learningId}: ${item.title}\n`
      md += `**Target**: \`${relativePath}\`\n`
      md += `**Evidence**: ${item.evidence}\n\n`
      md += `**Instead of**: ${item.instead_of}\n`
      md += `**Do**: ${item.do_this}\n\n`
      
      learningId++
    }
  }
  
  return md
}

/**
 * Append learnings to existing draft
 */
function appendToDraft(
  existingPath: string,
  learnings: Array<{
    title: string
    category: string
    target: string
    evidence: string
    instead_of: string
    do_this: string
  }>,
  sessionID: string,
  directory: string,
  skillsUsed: Set<string>
): void {
  const existing = fs.readFileSync(existingPath, "utf-8")
  
  // Find highest existing L number
  const lNumbers = existing.match(/### L(\d+):/g) || []
  const maxL = lNumbers.length > 0
    ? Math.max(...lNumbers.map(m => parseInt(m.match(/\d+/)![0])))
    : 0
  
  let appendContent = `\n---\n\n*Session: ${sessionID} (appended)*\n\n`
  
  let learningId = maxL + 1
  
  // Group by category
  const byCategory: Record<string, typeof learnings> = {
    "Anti-Patterns": [],
    "Missing Context": [],
    "Success Patterns": [],
  }
  
  learnings.forEach(l => {
    const cat = l.category in byCategory ? l.category : "Missing Context"
    byCategory[cat].push(l)
  })
  
  for (const [category, items] of Object.entries(byCategory)) {
    if (items.length === 0) continue
    
    appendContent += `## ${category} (continued)\n\n`
    
    for (const item of items) {
      const resolvedTarget = resolveTargetFile(item.target, skillsUsed, directory)
      const relativePath = path.relative(directory, resolvedTarget)
      
      appendContent += `### L${learningId}: ${item.title}\n`
      appendContent += `**Target**: \`${relativePath}\`\n`
      appendContent += `**Evidence**: ${item.evidence}\n\n`
      appendContent += `**Instead of**: ${item.instead_of}\n`
      appendContent += `**Do**: ${item.do_this}\n\n`
      
      learningId++
    }
  }
  
  fs.appendFileSync(existingPath, appendContent)
}

/**
 * Extract titles from existing learnings file for deduplication
 */
function extractExistingTitles(filePath: string): string[] {
  try {
    if (!fs.existsSync(filePath)) return []
    const content = fs.readFileSync(filePath, "utf-8")
    const titles = content.match(/### L\d+: .+/g) || []
    return titles.map(t => t.replace(/### L\d+: /, ""))
  } catch {
    return []
  }
}

/**
 * Build LLM analysis prompt
 */
function buildAnalysisPrompt(messages: string, existingTitles: string[] = []): string {
  const deduplicationSection = existingTitles.length > 0 
    ? `\nDEDUPLICATION:\nThe following topics are already documented. Skip any learnings covering these concepts:\n${existingTitles.map(t => `- ${t}`).join("\n")}\n`
    : ""
  
  return `Analyze this coding session for learnings that should be added to instruction files.

SCOPE - Only PROJECT-SPECIFIC learnings:
✅ User explicitly corrected the agent (indicates missing project context)
✅ Same mistake repeated across multiple turns (pattern worth documenting)
✅ API quirks, library behaviors, architecture specific to this codebase
❌ General agent behaviors (verification, mode constraints, tool restrictions)
❌ Agent environment behaviors (plan mode, permission errors)
❌ Single-occurrence mistakes agent self-corrected

FILTER - Skip learnings that are:
- Minor impact (optimizations, preferences, nice-to-know)
- User-facing only (UI shortcuts, TUI commands agent cannot execute)
- Too vague to be actionable
- Duplicates of common knowledge
- Agent environment behaviors all agents know from system prompts

Only include CRITICAL (causes failures) or MODERATE (causes friction) learnings.
${deduplicationSection}
CATEGORIES:
- Anti-Patterns: Counterintuitive behavior, traps, things that will fail unexpectedly
- Missing Context: How systems actually work, discovered via research or trial/error
- Success Patterns: Effective approaches to problems, process improvements

For each learning, specify:
- title: Specific topic with core insight (e.g., 'Plugin Files - must be flat in plugin/*.ts')
- category: "Anti-Patterns" | "Missing Context" | "Success Patterns"
- target: Path to instruction file (e.g., "CLAUDE.md", ".claude/skills/gitingest/SKILL.md")
- evidence: WHY - what specifically happened that revealed this? Be concrete.
- instead_of: The wrong approach that was tried
- do_this: WHEN [scenario], DO [action]. Include a concrete example.

BAD example:
  evidence: "User had to repeat information"
  instead_of: "Not checking documentation"
  do_this: "Review session transcript for context"

GOOD example:
  evidence: "Agent placed plugin in subdirectory index.ts, but opencode only scans flat plugin/*.ts files. User had to spawn research agent to discover this."
  instead_of: "Creating .opencode/plugin/my-plugin/index.ts (subdirectory structure)"
  do_this: "WHEN creating opencode plugins, place file directly in .opencode/plugin/*.ts. Subdirectories can hold config/data but main plugin must be flat. Example: continuous-learning/index.ts → continuous-learning.ts"

Only extract genuine, impactful learnings. If nothing significant, return [].

Return ONLY valid JSON array:
[{"title":"...", "category":"...", "target":"...", "evidence":"...", "instead_of":"...", "do_this":"..."}]

Session transcript:
${messages}`
}

/**
 * Parse LLM response defensively
 */
function parseLearnings(response: string): Array<{
  title: string
  category: string
  target: string
  evidence: string
  instead_of: string
  do_this: string
}> {
  try {
    // Try to extract JSON array from response
    const jsonMatch = response.match(/\[[\s\S]*\]/)
    if (!jsonMatch) return []
    
    const parsed = JSON.parse(jsonMatch[0])
    if (!Array.isArray(parsed)) return []
    
    // Validate each learning has required fields
    return parsed.filter(l => 
      typeof l.title === "string" &&
      typeof l.category === "string" &&
      typeof l.target === "string" &&
      typeof l.evidence === "string" &&
      typeof l.instead_of === "string" &&
      typeof l.do_this === "string"
    )
  } catch {
    return []
  }
}

/**
 * Format session messages for analysis
 */
function formatMessagesForAnalysis(messages: any[]): string {
  const formatted: string[] = []
  
  for (const msg of messages) {
    const role = msg.info?.role || "unknown"
    const parts = msg.parts as any[] || []
    
    for (const part of parts) {
      if (part.type === "text" && part.text) {
        // Truncate very long text parts
        const text = part.text.length > 2000 
          ? part.text.slice(0, 2000) + "...[truncated]"
          : part.text
        formatted.push(`[${role.toUpperCase()}]: ${text}`)
      } else if (part.type === "tool-invocation") {
        formatted.push(`[TOOL]: ${part.toolName || "unknown"}`)
      } else if (part.type === "tool-result") {
        // Skip large tool results, just note they happened
        formatted.push(`[TOOL RESULT]: (output omitted)`)
      }
    }
  }
  
  // Limit total size
  const joined = formatted.join("\n\n")
  return joined.length > 50000 ? joined.slice(-50000) : joined
}

/**
 * Main plugin export
 */
export const ContinuousLearningPlugin: Plugin = async ({ client, project, $, directory }) => {
  const pluginDir = path.join(directory, ".opencode/plugin/continuous-learning")
  const configPath = path.join(pluginDir, "config.json")
  const learningsDir = path.join(pluginDir, "learnings")
  
  // Ensure learnings directory exists
  if (!fs.existsSync(learningsDir)) {
    fs.mkdirSync(learningsDir, { recursive: true })
  }
  
  // Load config
  let config = { model: "opencode/big-pickle", toast: true, enabled: true }
  try {
    if (fs.existsSync(configPath)) {
      config = { ...config, ...JSON.parse(fs.readFileSync(configPath, "utf-8")) }
    }
  } catch {}
  
  // Exit early if disabled
  if (!config.enabled) {
    return {}
  }
  
  return {
    /**
     * Track skill usage (before hook has args)
     */
    async "tool.execute.before"(input, output) {
      if (input.tool === "skill" && output.args?.name) {
        const state = getSessionState(input.sessionID)
        state.skillsUsed.add(output.args.name)
      }
    },

    /**
     * Track file edits (after hook confirms completion)
     */
    async "tool.execute.after"(input) {
      const state = getSessionState(input.sessionID)
      if (["write", "edit", "patch"].includes(input.tool)) {
        state.hasSubstantiveWork = true
      }
    },
    
    /**
     * Analyze session on idle
     */
    async event(input) {
      if (input.event.type !== "session.idle") return
      
      const sessionID = input.event.properties.sessionID
      const state = sessionState.get(sessionID)
      
      // Skip if no substantive work
      if (!state?.hasSubstantiveWork) {
        return
      }
      
      try {
        // Skip subagent sessions
        const sessionResult = await client.session.get({ path: { id: sessionID } })
        if (sessionResult.data?.parentID) {
          return
        }
        
        // Fetch messages
        const response = await client.session.messages({ path: { id: sessionID } })
        if (!response.data || response.data.length === 0) {
          return
        }
        
        // Format for analysis
        const transcript = formatMessagesForAnalysis(response.data)
        if (transcript.length < 500) {
          // Too short, likely not enough context
          return
        }
        
        // Load config
        let config = { model: "opencode/big-pickle", toast: true }
        try {
          config = JSON.parse(fs.readFileSync(configPath, "utf-8"))
        } catch {
          // Use defaults
        }
        
        // Check for existing session file and extract titles for deduplication
        const existingSessionFile = findSessionDraft(learningsDir, sessionID)
        const existingTitles = existingSessionFile ? extractExistingTitles(existingSessionFile) : []
        
        // Build prompt with deduplication
        const prompt = buildAnalysisPrompt(transcript, existingTitles)
        
        // Create a sub-session for LLM analysis (will be a child session)
        const analysisSessionResult = await client.session.create({
          body: { parentID: sessionID }
        })
        if (!analysisSessionResult.data) {
          return
        }
        const analysisSession = analysisSessionResult.data
        
        // Send prompt to LLM and wait for response
        await client.session.prompt({
          path: { id: analysisSession.id },
          body: {
            parts: [{ type: "text", text: prompt }]
          }
        })
        
        // Fetch the response messages from the analysis session
        const analysisMessages = await client.session.messages({
          path: { id: analysisSession.id }
        })
        
        // Extract LLM response text from messages
        let llmResponse = ""
        for (const msg of analysisMessages.data || []) {
          if (msg.info?.role === "assistant") {
            for (const part of (msg.parts || []) as any[]) {
              if (part.type === "text" && part.text) {
                llmResponse += part.text
              }
            }
          }
        }
        
        // Parse learnings from LLM response
        const learnings = parseLearnings(llmResponse)
        
        // Only write if we found learnings
        if (learnings.length === 0) {
          return
        }
        
        // Check for existing session draft
        const existingDraft = findSessionDraft(learningsDir, sessionID)
        
        // Write or append draft
        if (existingDraft) {
          appendToDraft(existingDraft, learnings, sessionID, directory, state.skillsUsed)
          
          if (config.toast) {
            try {
              await client.tui.showToast({
                body: {
                  message: `Appended ${learnings.length} learnings to today's draft`,
                  variant: "info",
                  duration: 5000
                }
              })
            } catch {
              // Toast failed, continue silently
            }
          }
        } else {
          const filename = generateDraftFilename(sessionID, learnings)
          const draftPath = path.join(learningsDir, filename)
          const content = formatDraft(learnings, sessionID, directory, state.skillsUsed)
          
          fs.writeFileSync(draftPath, content)
          
          if (config.toast) {
            try {
              // Extract topic (max 3 words) from first learning title
              const topic = learnings[0]?.title
                ?.split(/\s+/)
                .slice(0, 3)
                .join(" ") || "New Learnings"
              
              await client.tui.showToast({
                body: {
                  message: `New learning: ${topic}`,
                  variant: "info",
                  duration: 5000
                }
              })
            } catch {
              // Toast failed, continue silently
            }
          }
        }
        
        // Clean up session state
        sessionState.delete(sessionID)
        cleanupOldSessions()
        
      } catch {
        // Silent fail - don't break OpenCode
      }
    }
  }
}