![Thumbnail](https://i.ytimg.com/vi/pN-LfxNFiTc/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLDJRjJUNvnagLFs1W5zTVJLQNfJrQ)

# How RAG, GraphRAG, and Context Engineering Improve AI Performance
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-07 |
| **Type** | Video |
| **Duration** | 10:49 |
| **Views** | 48,269 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=pN-LfxNFiTc) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Learn more about GraphRAG here → https://ibm.biz/BdpyvE

Context is the biggest bottleneck in getting AI to do what you want. Martin Keen explains how context engineering, RAG, GraphRAG, and precision retrieval improve relevance, governance, and AI performance. Discover how to build more reliable, context‑aware systems. 🤖

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdpyvX

#agenticai #aiinfrastructure #aisystems #contextengineering
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
| **Characters** | `8345` |
| **Error** | `none` |


What's one of the biggest inhibitors in getting an AI model to do what you want it to do? Well, it may not be the model itself. It might actually be something else. And that something else is context. Now, the frontier AI models that we have today, I think you could argue that, well, they're they're pretty great. I've spent this week vibe coding all sorts of applications that I've had on my to-do list but didn't really have the time or the skills to create up until now. And these frontier coding AI models have been nailing these tasks. If you if you ever need an app that indexes B-roll footage for coffee videos, give me a shout. I've vibe coded just the thing. But while the raw intelligence of AI models is clearly there, they can still get things wrong, confidently wrong. And that's often not so much a failure of basic model reasoning. In fact, I would say that model reasoning these days, it's pretty good. So, it's more a failure of knowing specifically what is relevant. the relevancy of information and that well that comes down to context. Now the term for this is context engineering which is the ability of an AI system to discover the right data, understand what it means and apply it correctly in real time within the constraints and governance of the environment's operating system. So let's say I'm an analyst and I ask an AI assistant to give me everything I need to prepare for the big important client meeting that I have got tomorrow. So I basically want it to create a document for me with all the scoop. Now, a model with no context is going to give me a beautifully structured meeting template with just lovely formatting, but it's going to be totally generic. But an AI system with good context engineering that would know which client I'm meeting and it would pull in things like well recent support tickets would be pulled in because well there happens to be an ongoing issue with that client. It might also check the deal history and discover that the renewal is coming up. So that's contextually relevant. And then just as importantly, it does not pull in the internal pricing discussion. It found no thank you because my role doesn't have access to that. It's taken governance into account. And and now we've got a pretty decent meeting prep dock that is actually of some use. And that's not because the model that made it had superior reasoning. It's because context engineering has given the model relevant contextual intelligence whereby the model has access to appropriate context. Now, you might be thinking that adding context to a model, well, that sounds a lot like rag, retrieval, augmented generation. Or maybe it sounds like just some some really good prompt engineering thrown into the model as well. And and yeah, I mean, that is part of it. In fact, context engineering is indeed stuff like this. It's the practice of designing and building systems that deliver the right context to AI models at runtime. But context engineering also has to consider where all of this contextual data comes from. And this is where things can get a little bit tricky. And that's because that the data that an AI model needs doesn't sit in one place. I mean, some of that data is probably in databases. Some of it is in document stores. You might need APIs to access some of it. Some of it might be on SAS platforms. Some of it's in the cloud. Some of it is on premise. And some of this data is nicely structured. Some of it's a mess, some of it changes hourly, and depending on who you are and what role you have, you might not even be allowed to access certain parts of it. So getting the right context to the AI model at the right time with the right permissions is an infrastructure problem. It's context that's the bottleneck here. So if context is the bottleneck, what does it actually look like to fix that? Well, I think there are four things that a system needs to get right for a good context engineering solution. And the first one is connected access. AI needs to be able to see across the data estate. And I say data estate because in many large organizations the data is everywhere. So rather than copying the data all to one place, zero copy federation is where the AI queries data where it lives, which means it's always fresh and the original access controls, they will stay intact. That's number one. Now second is the knowledge layer because raw data on its own isn't necessarily useful context. So the knowledge layer can apply things like entity resolution across systems and then it can map out relationships and hierarchies to give that raw data some meaning. And beyond just semantics, a knowledge layer can also add things like decision traces and institutional knowledge. Number three, I'm going to say is precision retrieval. Because as my English teacher used to tell me, making your essays longer doesn't necessarily make it better, Martin. Right on, Mrs. Potter. I still remember that. So, so better context is not more context, it's more precise context. And that means documents filtered by intent. It means documents filtered by role and time and policy. And not bothering the AI model with stuff. it actually doesn't need. And then finally is number four, runtime governance. Now governance has to be enforced live at retrieval time and also at response time. Can this agent query this data source and should this result be included given who is asking that sort of thing. So those are the four pillars. connected access the knowledge layer precision retrieval and then runtime governance and well connected access that is really giving the AI visibility across the data the knowledge layer that's giving the data some meaning the precision retrieval delivers only what's relevant and then governance makes this whole thing defensible Now I want to focus on one of those pillars in particular, precision retrieval. Most people's first experience with giving an AI model external context is basic rag retrieval augmented generation. We talk about rag all the time on this channel for many good reasons. One of which, I'm not going to lie, is that when we do, people tend to watch those videos. So I think that tells us that rag is pretty popular. It's where you take your documents and then you kind of chunk them up and you embed them into vectors and then at query time you do a similarity search to find the closest matches. And rag works great for simple lookups. But what else is there? Well, there's another type of rag. There's several in fact and one of those is called aentic rag. Now in agentic rag, the AI agent makes a first pass request for data. It looks at what it got back and then maybe decides it doesn't have enough to work with. So, it goes back for more. It's iterative. And that's a bit of a a step up from oneot rag retrieval. Another type of rag is called graph rag. Now, graph rag uses a graph structure to navigate context. So, instead of just asking what documents are semantically similar to my query, that's that's what standard rag does. Graph rag asks what entities are connected to this client and what documents relate to those entities. So the graph gives you a bit more in the way of precision and structure and then vector search fills in the detail within that scope. And then there is also something called context compression. There's a limit basically to how much a model can process at inference time. And even when a context window is large, which most Frontier models have really large context windows, it's still the case that more noise means worse results. So systems can compress and prioritize. That means they summarize long documents or they rank what's most relevant to the specific task. all to maximize the signal and minimize the noise for a given context. So we've got aentic rag deciding what context to go after. We've got graph rag that's working through relationships to find it. And we've got compression that is making sure that what arrives at the model is lean and useful. That is a system with contextual intelligence. I think it's fair to say that model intelligence and reasoning are not the bottlenecks anymore in many cases. Getting good context to the model is a model is only as good as the context it can access. And a contextually intelligent system means better decisions and better outcomes with agentic AI.
