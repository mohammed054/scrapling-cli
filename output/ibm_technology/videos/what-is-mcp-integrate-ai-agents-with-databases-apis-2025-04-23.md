![Thumbnail](https://i.ytimg.com/vi/eur8dUO9mvE/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCvGp1afWQjjvVd0iygr_JzFnTVsg)

# What is MCP? Integrate AI Agents with Databases & APIs
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2025-04-23 |
| **Type** | Video |
| **Duration** | 3:46 |
| **Views** | 548,523 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,660,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=eur8dUO9mvE) |
| **Category** | — |
| **Language** | — |
---

## Score

| Component | Raw | Normalized |
|-----------|-----|------------|
| Views | 548,523 | `0.4668` |
| Likes | 0 | `0.0000` |
| Comments | 0 | `0.0000` |
| Engagement rate | `0.000000` | `0.0000` |
| **Final score** | | **`0.085857`** |

> Ranked by: **weighted**
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified Architect on Cloud Pak? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdGhLq

Learn more about AI Agents here → https://ibm.biz/BdGhLf

Unlock the secrets of MCP! 🚀 Dive into the world of Model Context Protocol and learn how to seamlessly connect AI agents to databases, APIs, and more. Roy Derks breaks down its components, from hosts to servers, and showcases real-world applications. Gain the knowledge to revolutionize your AI projects! 🧠

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdGhLP

#aiagents #dataintegration #api
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
| **Characters** | `3012` |
| **Error** | `none` |


If you're building AI agents, you've probably heard about MCP or Model Context Protocol. MCP is a new open source standard to connect your agents to data sources such as databases or APIs. MCP consists of multiple components. The most important ones are the host, the client, and the server. So let's break it down. At the very top you would have your MCP host. Your MCP host will include an MCP client. And it could also include multiple clients. The MCP host could be an application such as a chat app. It could also be a code assistant in your IDE, and much more. The MCP host will connect to an MCP server. It can actually connect to multiple MCP servers as well. It doesn't matter how many MCP servers you connect to your MCP host or client. The MCP host and servers will connect over each other through the MCP protocol. The MCP protocol is a transport layer in the middle. Whenever your MCP host or client needs a tool, it's going to connect to the MCP server. The MCP server will then connect to, for example, a database. And it doesn't matter if this is a relational database or a NoSQL database. It could also connect to APIs. And also the API standard doesn't really matter. Finally, it could also connect to data sources such as a local file type or maybe code. This is especially useful when you're building something like a code assistant in your IDE. Let's look at an example of how to use MCP in practice. We still have the three components. We would have our MCP host and client, of course, we also have a large language model, and finally, we have our MCP servers, and these could be multiple MCP servers or just a single one. Let's assume our MCP client and host is a chat app, and you ask a question such as, what is the weather like in a certain location or how many customers do I have? The MCP host will need to retrieve tools from the MCP server. The MCP server will then conclude and tell which tools are available. From the MCP host, you would then have to connect to the large language model and send over your question plus the available tools. If all is well, the LLM will reply and tell you which tools to use. Once the MCP host and client knows which tools to use, it knows which MCP servers to call. So when it calls the MCP server in order to get a tool result, the MCP server will be responsible for executing something that goes to a database, to an API, or a local piece of code, and of course, there could be subsequent calls to MCP servers. The MCP server will apply with a response, which you can send back to the LLM. And finally, you should be able to get your final answer based on the question that you asked in the chat application. If you are building agents, I'd really advise you to look at MCP protocol. The MCP protocol is a new standard which will help you to connect your data sources via MCP server to any agent. Even though you might not be building agents, your client might be building agents. And if you enjoyed this video, make sure to like and subscribe.
