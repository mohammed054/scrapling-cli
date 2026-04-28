![Thumbnail](https://i.ytimg.com/vi/TqC1qOfiVcQ/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCziamQZEJJVIdkfFQBR2c74pF19A)

# Claude Agent SDK [Full Workshop] — Thariq Shihipar, Anthropic
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-01-28 |
| **Type** | Video |
| **Duration** | 1:52:25 |
| **Views** | 104,823 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 428,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=TqC1qOfiVcQ) |
| **Category** | - |
| **Language** | - |
---

## Score

| Component | Raw | Normalized |
|-----------|-----|------------|
| Views | 104,823 | `0.3472` |
| Likes | 0 | `0.0000` |
| Comments | 0 | `0.0000` |
| Engagement rate | `0.000000` | `0.0000` |
| **Final score** | | **`0.135650`** |

> Ranked by: **weighted**
---

## Tags

_No tags._
---

## Description

Learn to use Anthropic's Claude Agent SDK (formerly Claude Code SDK) for AI-powered development workflows!

https://platform.claude.com/docs/en/agent-sdk/overview
https://x.com/trq212

**AI Summary**
This workshop by Thariq Shihipar (Anthropic) details the architecture and implementation of the **Claude Agent SDK**. The session moves from high-level theory—defining "agents" as autonomous systems that manage their own context and trajectory—to a live-coding demonstration. Shihipar builds an agent "Harness" from scratch, implementing the core **Agent Loop** (Context  Thought  Action  Observation), integrating the **Bash tool** for general computer use, and demonstrating **Context Engineering** via the file system to maintain state across long tasks.

**Timestamps**

00:00 Introduction: Agenda and the "Agent" definition
05:15 The "Harness" concept: Tools, Prompts, and Skills
10:10 Live Coding Setup: Initializing the Agent class and environment
15:45 implementing the "Think" step: Getting the model to reason before acting
25:20 The Agent Loop: connecting `act`, `observe`, and `loop`
33:10 Tool Execution: Handling XML parsing and tool inputs
42:00 The "Bash" Tool: Giving the agent command line access
49:30 Safety & Permissions: "ReadOnly" vs "ReadWrite" file access
58:15 Context Engineering: Using `ls` and `cat` to build dynamic context
01:05:00 The "Monitor": Viewing the agent's thought process in real-time
01:12:45 Handling "Stuck" States: Feedback loops and error correction
01:21:20 Multi-turn Complex Tasks: Building a "Research Agent" demo
01:35:10 Refactoring patterns: "Hooks" and deterministic overrides
01:48:39 Q&A: Reproducibility, helper scripts, and non-determinism
01:50:31 Q&A: Strategies for massive codebases (50M+ lines)
01:52:00 Closing remarks and future SDK roadmap

* **Evolution of AI Capabilities:** Shihipar argues we are shifting from **LLM Features** (categorization, single turn) to **Workflows** (structured, multi-step chains like RAG) to **Agents**. He defines agents as systems that *"build their own context, decide their own trajectories, and work very autonomously"* rather than following a rigid pipeline.
* **The Claude Agent SDK Architecture:** The SDK is built directly on top of **Claude Code** because Anthropic found they were *"rebuilding the same parts over and over again"* for internal tools.
* **The Harness:** A robust agent requires more than just a model; it needs a "Harness" containing Tools, Prompts, a **File System**, Skills, Sub-agents, and Memory.
* **Opinionated Design:** The SDK bakes in lessons from deploying Claude Code, specifically the "opinion" that general computer use (Bash) is often superior to bespoke tools.


* **The Power of the Bash Tool:** A key technical insight is that the **Bash tool** is often the most powerful tool for an agent. Instead of building custom tools for every action (e.g., a specific API wrapper for a file conversion), giving the agent access to the shell allows it to use existing software (like `ffmpeg`, `grep`, or `git`) to solve problems flexibly, similar to how a human developer works.
* **Context Engineering:** Shihipar introduces the concept of **Context Engineering** via the file system. Instead of just "Prompt Engineering," the agent uses the file system to manage its state and context.
* **Files as Memory:** The agent can write to files to "remember" things or create its own documentation (e.g., `CLAUDE.md`) to ground future actions.
* **Verification:** The file system serves as a ground truth for the agent to verify its work (e.g., checking if a file was actually created).


* **The Agent Loop & Intuition:** Building a successful agent loop is described as *"kind of an art or intuition"*. The loop generally follows a **Gather Context  Take Action  Verify Work** cycle. Shihipar emphasizes that this loop allows the agent to self-correct, a capability missing from rigid workflows.
* **Strategies for Determinism (Hooks):** During the Q&A, a technique for controlling agent behavior is discussed: **Hooks**.
* If an agent hallucinates or skips a step (e.g., guessing a Pokemon stat instead of checking a script), a hook can intercept the response and inject feedback: *"Please make sure you write a script, please make sure you read this data."*
* This enforces rules like "read before you write" without retraining the model.


* **Scaling to Large Codebases:** For massive codebases (50M+ lines), standard tools like `grep` or basic context window stuffing fail.
* **Semantic Search Limitations:** Shihipar notes that while semantic search is a common solution, it is *"brittle"* because the model isn't trained on the specific semantic index.
* **Solution:** He recommends good **"Claude MD"** files (context files) and starting the agent in a specific subdirectory to limit scope, rather than trying to index the entire 50M lines at once.
---

## Chapters

_No chapter markers._
---

## Top Comments

_No comment data available._
---

## Transcript

| Field | Value |
|-------|-------|
| **Status** | `unavailable` |
| **Source** | `none` |
| **Language** | `en` |
| **Characters** | `0` |
| **Error** | `youtube_transcript_api: Could not retrieve a transcript for the video https://www.youtube.com/watch?v=TqC1qOfiVcQ! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

Ways to work around this are explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).


If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!; yt_dlp: [0;31mERROR:[0m [youtube] TqC1qOfiVcQ: Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies; openai_asr: missing_OPENAI_API_KEY` |


> No transcript text was recovered for this item.
