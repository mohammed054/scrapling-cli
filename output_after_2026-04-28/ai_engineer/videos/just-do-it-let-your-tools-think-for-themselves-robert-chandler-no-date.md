![Thumbnail](https://i.ytimg.com/vi/lp0pswT_FEI/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLDo5DeaAcLpEgcwlG1NURHzu9j2SA)

# Just do it. (let your tools think for themselves) - Robert Chandler
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 11mo ago |
| **Type** | Video |
| **Duration** | 6:50 |
| **Views** | 1,415 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=lp0pswT_FEI) |
| **Category** | - |
| **Language** | - |
---

## Tags

_No tags._
---

## Description

There's a new type of wrapper in town. The MCP API wrapper. 

Make them thin and you'll be wondering why your chatbot is struggling to even send a Slack message (true story). But make them _agentic_ and the world is unlocked. 

In this talk I'll demonstrate the drawbacks using low level APIs as MCPs and show the magic that happens when your 'tools' are actually other agents. It's prompts all the way down baby!
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
| **Characters** | `7216` |
| **Error** | `none` |


Hi, I'm Robert. I'm the co-founder and CTO at Wordware. And at Wordware, I've personally helped hundreds of teams build reliable AI agents. I'm here to share a few of the insights that we got, especially when it comes to tools. Um, really agentic MCPs, giving your tools time to think. Before I worked on uh LLMs and agents, I used to work on self-driving cars, and really, you know, building high reliable systems is in my blood. So, uh, yeah, here we go. The promise of agents are automated systems that can take action in the real world on your behalf. They have all the context they need about you and your team and they have the ability to actually interact with the tools you use and output kind of data where you need it. Unfortunately, most of the time they don't really work. They're often slow, expensive, and unreliable. Um, I remember an example when MCP first came out and we hooked up Slack and it spent a bunch of time, you know, I just want to send a Slack message to Philip being like, "Hey, I'm using MCP. It's super cool." Um, unfortunately, it then like listed all the users in the Slack channel, got confused, tried listing all the channels, tried sending a message, actually finally found Philillip. Uh, it ended up resorting to sending a message in the general channel being like, "Hey, could someone tell Philip MCP is awesome?" um which I thought was kind of amusing but also really not what I wanted as a user. It also took about 5 minutes to do that. Um and the real problem is that these MCPs are often low-level wrappers around APIs that were not designed for language models. You know, you get these messy responses that have huge blobs of JSON which are great for like deterministic state machines but kind of suck and are kind of context pollution for agents. You get tools that are these tiny scope. You know, most of the MTP tools are just a wrapper around a function and functions designed for the programmatic world where you want to compose a lot of these uh tasks together into like sequences of function calls. That's really hard for an LM to continue reasoning over multiple calls and like polluting that context with all different outputs. It's also a problem when you've got multi-ool pageionation. You know, when the API responds and you need to kind of loop over the results until you get the data you're looking for. This really pollutes the context window, but it also means that the LLM has to reason over more and more uh longer chains of of requests. Authentication is a pain. You know, it's got a little bit easier with these hosted MCPs, but still a lot of the time you need to have your own API keys. You need to be like modifying like creating bots and things. Um I'm sure that will go away over the next few months, but right now it's a bit of a pain. And uh yeah, just in general the agents struggle when there's many tools or kind of sequences of tools to perform. Um it's really hard. You know, every tool you adds more noise to the context window. A lot of instructions. Even just adding a Slack MTP adds eight different tools. If you add notion, you add another like 20 different tools. Um and those two together sort of you can do a lot, but it's not like the be all end all of automation. So how do we solve this? Well, in my opinion, we add more agency to the tools. Rather than making these tools very small, um, think a bit like, you know, a T-Rex holding a little tiny spanner. Um, uh, or like inspect a gadget with like a thousand different tools. Think of it a bit more like a team of Avengers where, you know, you've got specialized people for different tasks. you know, you got the Hulk to smash. You've got uh the Hawkeye to fire the arrow off and uh really do high precision tasks. Um and you know, obviously we all love Iron Man. He's the best and he's just pretty good at a lot of things. Um maybe that's the main agent. Who knows? I'm not sure where this analogy is going, but I'm sure it's an entertaining one. Uh but really what we want to do is blur the line between what's a tool and what's an agent. Um when is an agent just a tool for another agent? and you know give tidy simple natural language APIs to these agents such that they get reliable reusable highquality outputs. What I'm going to do is I'm going to demonstrate Wordware's new MCP toolbox. And this allows you to build uh agentic MCPs. You can turn your Wordwares into tools for your agents. Um and so I'm just going to grab one from the landing page as an example. Um, and I'm picking this kind of uh competitor analysis because um that's a a flow that requires quite a lot of taste, quite a lot of reasoning and also integration into both Twitter and notion. Um rather than you know finding a Twitter MCP um I just use the kind of Twitter scrape tool but into Wordware and then I've described what I really want from my competitor analysis. It's not just a generic whatever the LM thinks. um it's kind of gone into detail about what I care about and I could add even more details about my company and try and work out you know where do we where do we differ it then creates this analysis writes the output to notion and then returns the URL in the output and so uh I can easily do this I can go to mcpbeawordware.ai AI. So, um, still in the early days, but, um, yeah, we are rolling this out beyond beta fairly soon. And, uh, here's a toolbox I created earlier. I just added the competitor analysis after publishing this app earlier. I connect that to Claude. And now I can, uh, use this tool inside my Claude. And what's nice about Wordware is you can add multiple tools into this toolbox. So you can have a bunch of different tools that are grouped together that are all related or entirely disparate, but you can switch on and off different toolboxes for different tasks. But maybe let's do something like create a competitor analysis for anthropic AI. I hit this and now you can see it's going to use the wordware tool. I can allow it once. We can allow it always. You know, there's nothing too bad that can go wrong here. So I'm just going to let it go. And now it's going to perform this competitor analysis. Here's one I made earlier. Cool. So, now that's done. I can grab the link to the notion page on the competitor analysis. Open that up and we'll see a nicely formatted summary based on all the tweets from Anthropic and we can see they care a lot about how they're tweeting and so we can learn from their style. Um, and it's all in my notion page, nicely formatted. Um, and exactly where I'd want to find it again so it's not just lost in the chats. So, pretty exciting. We managed to build a highly reliable, highly repeatable, and highly aligned tool that allows our generic agent to be very specific and very uh powerful for doing that task that we wanted it to do. And so we've really blurred the line between what's an agent and what's a tool and allowed our agent to offload tasks to something that's more powerful. Exactly how you know we do this already in teams and you have specialists for people you know whether it's the Avengers or your team in a company. You can use web toolbox to build these flows. You can use anything to build agentic MCPS.
