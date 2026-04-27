![Thumbnail](https://i.ytimg.com/vi/TjvT9sI5mLE/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLC9WtNYV9jKMcsg2pBM_PaCq1z-wQ)

# What Is Agentic Storage? Solving AI’s Limits with LLMs & MCP
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-03-29 |
| **Type** | Video |
| **Duration** | 7:45 |
| **Views** | 75,615 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,670,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=TjvT9sI5mLE) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified z/OS v3.x Administrator? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdpBkr

Learn more about Agentic AI here → https://ibm.biz/BdpBks

AI agents forget everything after a session, can they be smarter? 🤔 Martin Keen breaks down Agentic Storage, showing how it gives LLMs persistent memory using RAG and MCP. Learn how safety layers like sandboxing and immutable versioning make AI systems safer and more reliable. 🚀

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdpBki

#agenticai #llm #aiworkflow
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
| **Characters** | `5979` |
| **Error** | `none` |


What is agentic storage? And why do we need it? Well, agentic AI systems, they're powered by LLMs, large language models, but they're not chatbots. They're systems that actually go out and do work autonomously, like write code and remediate incidents. And LLMs are essentially stateless entities. When you spin up an AI agent, its entire memory exists inside what we call the context window. And the context window, well, it's a bit like RAM, like random access memory, in that it's volatile, temporary storage. The moment that session ends or the context window has filled up, well, the agent's memory effectively resets. It forgets what it did. And that can be a bit of a problem for agentic AI. Now, this lack of state is somewhat addressed with RAG, retrieval augmented generation. Because RAG lets you connect your large language model to a vector database. Now, that vector database might be full of documents or policies or historical data, whatever. And the agent can then query that database to perform a semantic search. And then, it can pull relevant information into its context window before generating a response, which is all good. But it doesn't really solve our stateless problem because RAG is fundamentally read only. It's a read-only operation. It solves the input problem of getting information into the model, but it doesn't really solve the output problem. So if your agent writes a Python script or it creates a remediation playbook, well, where does that work product? Where does that actually go? And that is what agentic storage is here to address. And it's, it's tempting to say that agentic storage is effectively giving an agent a hard drive instead of just RAM. So its work product persists between sessions. But I think it's a bit more than that. It's a bit more than a hard drive. It's where the storage layer is aware of and designed for autonomous agents. So how do we actually give an agent a file system? Well, one approach would be to write custom API integrations for every storage system you want the agent to interact with. So let's think about that. Perhaps we've got a storage system here that is for object storage. And we've got a another one here. And this one is for block storage. And perhaps we even have a third one here. This one is for now as network attached storage. Now each of these has different APIs, different data models, probably different authentication mechanisms. And you'd be writing and maintaining custom code integrations for each one And well, that doesn't really scale. So the industry is converging on a standard called the model context protocol, or MCP. And for our purposes, MCP is an interface that can be used by AI agents to work with, well, storage systems. So we have got here an MCP host. Now this is the AI application where the agent runs. And then below that, we've got the MCP server, which in this scenario is the storage layer. And whether the underlying system is object storage or block storage or NAS, the MCP server presents a uniform interface to the agent. Now connecting them is the MCP protocol itself, which uses JSON RPC. And what makes MCP useful here is how the server exposes capabilities through to primitives. Well, let's cover a couple of those. And the first of those are resources. Now these are passive data objects like file contents and database records. So when the agent needs context, it requests resources, which is pretty similar conceptually to RAG, but it's standardized. And then there are tools. Now with tools, the MCP server exposes executable functions that the agent can invoke. So things like list directory, read file, write file, create snapshot. The agent doesn't care what's underneath object storage, block storage, NAS doesn't matter. It calls the tool, and the MCP server handles the translation. Now, if my skeptical security focus buddy Jeff Crume here, I think he might take issue to giving AI right access to a company's storage infrastructure. Yes, Martin, I would. Yeah. And that is a fair concern because agents can hallucinate, they can misinterpret instructions. They can take actions that seem logical in isolation but are catastrophic in context. So agentic storage is not merely storage that agents can write to. It's storage designed for autonomous agents. And that means that we need to build in a series of safety layers into that storage. These are layers that might be a bit overkill for humans, but they're pretty essential for AI. And I've got three to consider. And the first of those is immutable versioning. It means that every write operation creates a new version rather than overwriting, and that means the agent can never truly delete data. It can really only archive it. A complete audit trail and the ability to roll back any action. Second is sandboxing, and you'll definitely want to implement sandboxing. Basically, this means the agent operates within a constrained environment. It has access to specific directories and specific operations and, well, nothing else. So if an agent is supposed to manage application logs, it has no path to, let's say, system binaries. This prevents the confused deputy problem, where an agent with broad permissions gets tricked into acting outside its intended scope. And then, number three is intent validation. So before executing high impact operations, the storage layer can require the agent to explain why. Why should this delete operation be performed? Come up with a reason. And generating reasoning chains of thought is right in the agentic AI wheelhouse. So perhaps the agent reasons that I'm deleting these files because they're older than 90 days and that much is the retention policy. So with that reasoning in place, the storage layer verifies that claim before proceeding. But with these and other safety layers in place, your agent gets persistent storage. And Jeff, well, Jeff gets an audit trail. You might even like that. Well, you're getting close. I did say might.
