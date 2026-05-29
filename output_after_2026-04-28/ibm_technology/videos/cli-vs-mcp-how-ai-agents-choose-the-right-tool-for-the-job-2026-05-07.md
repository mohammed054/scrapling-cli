![Thumbnail](https://i.ytimg.com/vi/g9JIUM0MHgQ/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAma82fVhE9Xv1-5S4k2wJV-214fw)

# CLI vs MCP: How AI Agents Choose the Right Tool for the Job
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-07 |
| **Type** | Video |
| **Duration** | 14:06 |
| **Views** | 85,135 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=g9JIUM0MHgQ) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Learn more about MCP here → https://ibm.biz/~92j1qki7Y

Both CLI and MCP are ways for AI agents to interact with the world. Martin Keen explains how agents use CLI commands or MCP tools for tasks across real developer workflows. Learn how context windows, schemas, and practical examples shape smarter AI development. 🚀

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/~o4HUHwcNB

#aiagents #mcp #aidevelopment
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
| **Characters** | `10173` |
| **Error** | `none` |


Both CLI and MCP are ways for AI agents to interact with the outside world. Now CLI command line interface that's when an agent uses the CLI to run commands. It runs just regular terminal commands. What commands? Well commands like LS, like CAT, that's another one, Let's think of a few more grip, yeah, and... Let's say, curl. So these are the sort of commands it can run and they are the exact same commands a developer would type into a command terminal. Now MCP is a standardized protocol where dedicated servers expose structured tools. So these our tools, like let's one of them is read file, another one might be search files, and each tool has, well it has a name assigned to the tool like read file, it has a description which says what the tool does, written in English and then it has a JSON schema as well and that schema defines exactly what inputs it expects and what let's come back. There's a growing number of developers saying that MCP is an unnecessary complexity, that CLI tools can do the same job cheaper. And they do kind of have the numbers to back it up. So the argument goes a bit like this. AI models have been trained on millions of CLI examples, examples in their training data set from sources like stack overflow posts and man pages. So the model, it already knows how to use these commands and many more besides. I mean, we could just keep adding. Let's say we've got Git and then we've got Docker and then I could keep going on. It doesn't need a schema to tell it what flags to pass. That knowledge is baked in from the training. With MCP, every tool's schema gets loaded into the model's context window at the start of a conversation. And each one of those schema can cost hundreds of tokens. We're filling up a context window before the agent has even done anything useful. So, which side is right? Is MCP a useful abstraction tool or unnecessary context window filling bloat compared to the CLI? Let me show you two examples I carried out with an AI coding agent to illustrate the difference where the same operation was performed using CLI and MCP and you can try these very same exercises with the AI agent of your choice as well. So the first exercise is just simple file operations, so we've got a folder here with some markdown files and the agent has to do two things, it has to read one of the files notes.md And then it has to search both of them to try to find a specific word. Now I put in two separate requests to an AI coding agent, one requesting it use the CLI to do that task and the other requesting it use MCP. Now for the CL I approach, what happened was the agent ended up using two bash commands. So the first bash command it used was catnotes.md to dump the contents of a file to standard output. And then it used grep to search for the word agent across both Markdown files. Now, just a quick sidebar on these commands, if you're not a CLI person, cat, that's sure for concatenate. And here it's being used to print a single file and then grep that scans files line by line and spits out every line that matches the pattern and that minus N flag adds line numbers. So that's how the agent handled the CLI and it's worth pointing out the agent didn't need to look anything up to figure out which commands and flags to use. This was built into its training data. Now, when the agent adopted the MCP approach, it ended up using two tool calls from a particular MCP server called the file system server. Those two tools that it used from the MCP server were read file for reading from notes.md and then search files where we provided the string of the word that we wanted to search, which happened to be the word agent. Now, both approaches completed the task successfully and they both returned the same information, but the CLI commands, they were... They're a bit more compact and the model didn't need to know any schema to know that grep minus n was the right flag combination. Now the file system mcp server that advertises 13 tools, so I only actually used two. There were 11 more that weren't used and each one of those tools comes with a full JSON schema. That's a couple of thousand tokens of tool definitions loaded into the context window just so the agent could use two of them. So I think that is where some of the MCP is unnecessary complexity commentary kind of comes from, but honestly either would be fine in something this simple. It's when things scale up that the difference gets more notable. So let's think about something else. Let's think about Git, which is one of the most widely used developer tools on the planet. Now, an AI agent with Bash can run a bunch of Git commands, like it could run this command here to show the last 10 commits, and it could run Git status command to check the working tree. And the model knows Git cold, it knows the flags, it knows format strings, all from its training data. Now consider the MCP alternative, which this case, is the github mcp server. Now that... Doesn't ship 13 tools, that ships 80 different tools and every one of those tool definitions, the name, the description, the full JSON input schema with parameter types and descriptions, all of it, it gets injected into the model's context window at the start of the conversation and that adds up to approximately 55,000 tokens even if you only need one or two of those 80 tools and that. API pricing, those tokens are actual money. They eat directly into the context window space available for actual work and the model could have done those same Git operations with a couple of bash commands instead. So that is the CLI Camp's strongest argument. For local developer tools, MCP is paying a steep tax for knowledge the model already has. So is MCP Just dead weight. Well, let's try one more exercise. So this time, the task is to fetch a webpage at modelcontextprotocol.io and then just tell me what the main heading says plus a summary of the first few paragraphs. Now, first up was the... Approach and yes we're using MCP to fetch a page about MCP, a little meta. Now the agent used a single call to an MCP server and the server it used was called Fetcher. Now this is an MCP server built on a headless browser so it can render JavaScript and It made a single request using one tool that Fetcher has available. Which is just simply called fetch URL. And that had a link to the webpage, modelcontextprotocol.io. So the server launched a browser. It loaded this page, waited for it to render. It converted the result to readable text, and then it handed back the content. Now that used about 250 tokens and took but a couple of seconds. So that was MCP. The CLI approach started off good old simple curl, and this is where it gets painful. So the agent's first attempt was to use a curl minus s URL head minus 200 command, which is to fetch the raw HTML and just show the first 200 lines, but what came back was almost entirely JavaScript bundle code, because model context protocol dot is a next.js application. And the server doesn't send a finished HTML page. It sends a JavaScript application that builds the page in the browser and curl doesn't really run JavaScript. So all you end up getting is a skeleton and a pile of framework code. So at this point, the agent started improvising. It chained together text processing tools to try to strip the HTML tags and just filter out the JavaScript. That didn't work. So it tried to find page content embedded as JSON inside the source code that found fragments but it didn't find the full page. Then it wrote a Python script to reverse engineer the internal data format that Next.js uses to stream content to the browser. Reverse engineering a JavaScript's framework internals just to read a webpage. Now, when I ran this, it went through several more attempts before it finally got enough content to summarize the page. And it took several minutes and over 2,000 tokens, plus all that extra local processing on my poor laptop, all to get the same result. So what's the pattern here? Well, I think we can say that CLI, That wins when commands... Directly to jobs. So I'm thinking of jobs like file operations, like Git, like text processing and running scripts. Things where the command line has been solving the problem for decades and the model already knows the tools well. And also CLI tools they naturally compose with pipes so we can chain commands together in a single line which is something MCP can't do because each tool call is independent. But I think we can also make an argument for MCP. MCP wins when there is a gap between what the raw tool gives you and what you actually need, like my next.js web page example. And that extends to all sorts of other things as well. So for example, what about authentication? So authentication of Slack or Notion or databases? Well, with CLI... The agent is managing the OAuth tokens. It's looking up channel IDs. It's handling token refresh. Basically all of this stuff is quite manual. Now the AI agent is doing it, but it's still manually having to do so. Whereas MCP, the server, the MCP server takes care of all of that. So we could say this is actually server managed rather than the agent. Having to do it itself. The agent just says what it wants done. And I think also, if we look at this at an organization level, there are some differences as well. So MCP has some advantages here. When agents act on behalf of different employees, we might need per user access control. And we might need to not use share credentials. We, we may need audit trails. So we can actually track. What is being done. And those are hard things to bolt onto CLI after the fact, but MCP, that has it all built into the protocol. So MCP or CLI, you probably saw this coming, but the answer is to use both. The AI agent I tested uses both after all. It uses CLI and MCP side by side for differing tasks, CLI when the commands map to the job, mcp when the abstraction or the governance justifies it. The choice is up to the agent and the person prompting that agent and if the agent ever starts reverse engineering a javascript framework just to read a web page well that's a good sign it picked the wrong one
