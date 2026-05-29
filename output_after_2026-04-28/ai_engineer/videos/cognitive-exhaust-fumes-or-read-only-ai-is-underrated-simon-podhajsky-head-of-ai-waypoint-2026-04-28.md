![Thumbnail](https://i.ytimg.com/vi/u0TOSBbAw7c/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBfLTkQ16BQ1A2jJIdDQoW7svFX8w)

# Cognitive Exhaust Fumes, or: Read-Only AI Is Underrated — Šimon Podhajský, Head of AI, Waypoint
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-04-28 |
| **Type** | Video |
| **Duration** | 11:30 |
| **Views** | 1,848 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=u0TOSBbAw7c) |
| **Category** | - |
| **Language** | - |
---

## Tags

`ai` `ai engineer` `ai engineering` `software development` `tech` `startups` `software architecture` `machine learning`
---

## Description

Every other personal AI demo has agents sending emails and managing calendars. I built the opposite: a read-only system that queries my data sources (email, journal, tasks, CRM, browser sessions, notes) but can't modify any of them. This is an intentional limitation. I'll cover why trust asymmetry matters (read is safe, write is dangerous), how cross-source pattern detection beats task automation, and why ""exhaust fume analysis"" of one's cognition is more valuable than yet another AI assistant trying to act on your behalf.

Šimon Podhajský - Head of AI, Waypoint AI

I'm Head of AI at Waypoint and a full-stack builder with a background in data science and data engineering. I built this personal AI system to scratch my own itch -- and discovered that the ""read-only"" constraint led to better architecture than the agent-first approaches I see everywhere.

I made a Github repo with a template for people to try out the read-only AI / personal intelligence system: https://github.com/shippy/personal-intelligence-kit 

Socials:
https://linkedin.com/in/simonpodhajsky
https://x.com/sim_pod
https://simon.podhajsky.net

Slides:
https://slides.podhajsky.net/read-only-ai
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
| **Status** | `available` |
| **Source** | `youtube_transcript_api` |
| **Language** | `en` |
| **Characters** | `9371` |
| **Error** | `none` |


Hi, my name is Shimon. Today, I'll talk about a personal AI system that knows you, but won't do anything instead of you or on your behalf, and won't blow up your life. So, that's good. In the process, I'll talk about the risks of personal AI and how read-only AI systems like this one mitigate them. Let's get started. The whole personal AI space is obsessed with agents that act on your behalf. I built something different. The starting point, six sources, read access only, no write permissions. The limitation is fully intentional. But first of all, what are cognitive exhaust fumes? What are they? It's my term for the digital activity that is a byproduct of your cognition. Like exhaust fumes for a car engine, individually, it's just waste, but if you analyze the exhaust, you can diagnose the engine. So, let's see some examples of what the exhaust reveals. What does this enable you to do? Three top uses I've found, intention action gaps, attention drift, and relationship decay. No single source tells you any of this, and the cross-source ability is what these have in common. Your email client doesn't know what you journaled. Your task manager doesn't know what you're browsing. The cross-source signal is the product. Let's take a closer look at the system. Here it is, Fulan. Three zones. The sources are read-only. The AI never writes back to them. The workspace is where the analysis happens. The outputs land in a separate Obsidian vault for me to review, but it doesn't have to be a separate Obsidian vault. It could be separate Notion, separate text files, separate anything. Could be any other system. And that's the whole thing. So, what about applications? Let's start with a David Allen style getting things done like spin on the weekly reflection. Based on the six sources, the AI synthesizes an occasionally brutal reflection on how you spent your week. Let's look at a real example. Everything runs in Claude. I've stored this logic in the weekly reflection {slash} command {slash} skill. And what it does is it launches a Python script that gets all the data that come from the read-only sources, and looks through them, and creates structured outputs with specified prompts that I've prepared. This takes a little bit of a while. It pings the Anthropic API to get those structured outputs back. And [snorts] once it does, it will create a markdown document that I will be able to review. This is now uh finished running, so it gives me an overview, and I can open it back up in Cursor, and I'll convert it to a preview that's more readable, and see that in fact, it does hit the themes of the week. It does hit some of the tensions and conflicts that I need to think about. Talks about my commitments and relationships, which is mostly notable by its omissions, and highlights the notable moments as well as reflection questions that I like to think about. In short, this is not a productivity report. It's a reflection on how you're thinking, assembled entirely from exhaust. Let's take another example. I like to discuss what I'm reading with others, but sometimes I think I shouldn't keep messaging the same three people about it. So, I asked the AI, "Given my recent reading, who in my network should I be discussing this with?" This is the cross-source magic. Four data sources, none of which were designed to talk to each other, combined into an insight you'd never get from any single tool. And all read-only. Nothing was sent. Nothing was scheduled. Just a suggestion for me to act on if I choose. Let me once again show you the demo. Once again, this is a Claude skill, >> [sighs] >> but in this case, I've hidden most of the guts of the Claude skill into the cross-origin query, and ask for the specific question uh in plain language. The plain language knows that it will auto that it will activate the specific skill for the cross-source queries, and it now goes through the databases that I've curated that I have regular interest for, looks through the Vivaldi SQLite database for the articles that I've been reading the most, and after a while, it will figure out which of these articles um are most read, still open on tabs, and which people might be curious about it based on the profile. Now, this is probably the weakest part. The Clay MCP takes forever to run, but it searches my CRM, or my friend relationship system, I suppose, so FRM, for people who might be interested in articles of on these topics. Um In this case, it's people interested in AI, or people in European tech, or people in education, which coincidentally are three things that I also am. Now, as you might notice, this takes up a lot of tokens in the context window, so you probably don't want to do this in a session that is not clean, but it's not a problem if it messes up a little bit of the 1 million context window for 4.6, and then you clear it again. So, at this point, it's getting the responses from all of the Clay searches. It synthesizes the people that I should talk to, and it maps them to one article each. That's what the or it's about to map them to one article each. Uh this requires a little bit of uh bash sorcery on behalf of Claude code, but if you're running it with auto to auto mode, or dangerous disk permissions, you can get rid of that as well. And indeed, when I take a look at the first results, those look like the people that I might want to talk to that I haven't talked to yet about the kinds of articles that I've been reading. So, thank you, Claude. Right, in this case, it even found the author of the article that I was reading that's in my network, so I should give them a whirl. In short, no source knows the whole of this. Your browser doesn't know your contacts. Your CRM doesn't know what you're reading. The exhaust does. So, why keep it read-only if it's so useful, after all? Here's the thing about the risk involved. It's asymmetric. The downside of a read-only error is zero. I just ignore it. The downside of a write error is unbounded. And personal AI operates in the high-stakes environment. Your relationships, your career, your reputation. I'd rather miss out on automated emails than have a misfire nuke my life. But there's also a subtler philosophical argument, almost a matter of taste. Read-only isn't just safer, it produces better analysis. The moment your AI writes to your data sources, the exhaust fumes are contaminated. You're no longer observing your cognition. You're observing a human-AI hybrid, and you can't tell which patterns are yours. Sure, the observer changes your behavior, too, but the feedback loop is mediated by you, not automated. You read the reflection. You decide what to do. That's a different thing from the AI writing your draft. And there's an argument to be made that you don't want the AI to write your draft in the first place, that you should reclaim your agency. Might be a hard sell for this crowd, I think, but worth considering. At this point, you might be asking, "Why not throw all this into open Claude on a read-only mount?" Which I have. Here's the thing. The producer The observer produces more value per interaction by a wide margin. The agent saves me 30 seconds on a weather check. The observer shows me I've been avoiding my most important project for 2 weeks. Not to mention that there's less risk of exfiltration and cognitive pollution. The argument I'm making here is that read-only isn't a stepping stone to {quote} real agents. It helps you do things well, yes, but it fits a different gap, serves a different need. It's a different product category. The industry frames read-only as a limitation you graduate from. I think that's wrong. Observers and agents are different tools, and mayor isn't a broken butler. So, that's the value proposition. But I'd be doing you a disservice if I stopped here. Let's put on the paranoid hat. What keeps me up at night? Let's start with the mosaic effect. There's something called the mosaic effect, where you put together a lot of small pieces of information and you get a picture. My own slide copy describes the security risk perfectly. The same cross-referencing that makes the system useful makes it a devastating target. So, careful there. The other side of the coin, Simon Willison's lethal triquetra. In case you don't know the lethal triquetra, it's a security risk model that combines three factors: private data, untrusted content, and external communications. I initially thought we only broke the lethal triquetra, and it doesn't, not fully. It removes the natural exfiltration circle channels, but the third leg is any ability to communicate externally, and shell access still has that. In short, the system isn't fireproof, and I'm not claiming that. Even in the best-case scenario, I'm still sending data to Anthropic on a network that's mostly open, with a lot more information lying around that is strictly speaking required. I'm not claiming the system is secure. I'm claiming that I've thought about where it isn't, and I've decided which risks I'm willing to carry. It's different from not knowing. The worst security posture is the one you haven't examined. With that said, I still think there's something worthwhile to be learned from all this. Your digital exhaust is the most underused data set you own. Reflect on it and use it to make yourself better. Thanks for listening.
