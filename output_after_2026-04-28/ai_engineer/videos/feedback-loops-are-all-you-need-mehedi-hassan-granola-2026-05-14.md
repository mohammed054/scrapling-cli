![Thumbnail](https://i.ytimg.com/vi/ON5LIT0M4do/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBrg0ngfO_pcjdEMM9ubMVFLSxWxw)

# Feedback Loops are All You Need — Mehedi Hassan, Granola
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-14 |
| **Type** | Video |
| **Duration** | 10:11 |
| **Views** | 4,796 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=ON5LIT0M4do&pp=0gcJCQ0LAYcqIYzv) |
| **Category** | - |
| **Language** | - |
---

## Tags

`ai` `ai engineer` `ai engineering` `software development` `tech` `startups` `software architecture` `machine learning`
---

## Description

One-shotting is seductive. One line of code for web search. One prompt to serve every user. One deploy and you're done. Granola shipped a chat feature into their meeting notes app and found out what comes after that.

This talk is a product engineer's honest account of why the gap between "it works in the playground" and "it works in production" is so hard to close. Web search looks like a single tool call — until it blows up your context, bills you 10p per chat, and your provider ships an overnight update that silently degrades your results. Prompt personalization looks straightforward — until you realize that one prompt genuinely cannot serve the salesperson expecting a deal summary, the engineer expecting blockers and linear tickets, and the HR manager expecting something else entirely.

The response at Granola wasn't to prompt better. It was to build the machinery for iteration: custom internal tracing that exposes tool calls, search trails, reasoning traces, and cost in a UI built for everyone — not just engineers with CloudWatch access. And a move to run their Electron frontend as a web app, so every PR gets a preview link and Cursor can go test changes automatically. The point isn't any single technique. It's the feedback loop — and what happens to an AI feature when it actually has one.

Speaker info:
- https://x.com/mehedih_
- https://github.com/MehediH

timestamps:
0:15 Introduction to Granola and product engineering
1:08 Demonstration of meeting transcription and note-taking features
1:52 The challenges of shipping generic AI features
2:48 The difficulties of integrating web search tools
4:02 Why a single prompt cannot serve diverse user roles
4:40 Building custom internal tracing and observability tools
6:22 Enhancing developer experience for desktop applications
7:16 Refactoring Electron for web-based testing and CI/CD preview links
8:33 Automating feature verification with Cursor
8:46 Concluding thoughts on building iterative feedback loops for AI products
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
| **Characters** | `10459` |
| **Error** | `none` |


[music] >> Cool. How's it going, guys? I'm Maddie. We're going to talk about some product engineering stuff that we've been doing at Cronulla. This is not going to go deep into our engineering stuff. So, if you have for me to like go into LLMs and stuff, it's not going to happen. I'm warning you right now. So, you know what's coming. Cool. So, I'm a product engineer at Cronulla. I've been, you know, coding since jQuery was cool. I've seen React kind of change front-end engineering. And obviously now experiencing LLMs change engineering and everything else just like many of you. For those of you who don't know, Cronulla is an app for getting your work done. Essentially, we're a meeting notes app where we sit on your doc like it is doing right now. And it has access to your system transcription system audio as well as your microphone audio, which means we have real-time transcription. And then at the end of your meeting, we can give you really awesome notes. So, I'm just going to give you a quick demo. So, I was recording the previous um talk right here and you can see picked up literally everything the presenter said. And the cool thing about Cronulla is that you can also write your own notes on top of what the transcription is saying. So, the final result is more aligned to like what you'd normally actually write on a notepad. So, I'll go ahead and generate the notes here. And you'll see that this will go ahead and write a really good summary. And as you can see like I wrote down this 20% overlap thing and it focused more on the output, right? So, this is Cronulla. We have the best-in-class meeting notes no matter what role you're in and it doesn't get in your way. And that's been like our product philosophy since day one. So, we ship a lot of AI features in Cronulla and our product is known to be again not to get in your way. So, let's see what happens when you put a simple AI feature into prod. I'm going to kind of give you an example with this chat feature that we have. This is a feature that already exists in Cronulla. You can ask questions about a meeting that you just had and across a bunch of different meetings or like shared context as well. And Cronulla will try answer it to the best of your ability. So, let's say I built, you know, like a one-shot this chat system. It's very easy to do. And I put it into production in my fake Cronulla app. And then as soon as users hear, you know, it's like a call me in a minute. So, give me a list of cities. Web search is too slow. It's not writing follow-up emails how I normally write my emails. I asked it to coach me about my meetings and it's telling me meetings about my football coach. Obviously, these are very very common problems that you're going to run into when you make a generic chatbot. So, how do we get around this, right? So, what we've seen is like molding the LLM to work to your specific use case can be super hard. And one of the examples is is web search. So, web search for most LLM providers looks like a line of code. You simply add the web search tool and you expect it to just work. That's what the labs want you to believe, but once you get into it, there's lots of other complications. So, for example, the token usage and token cost can bubble up quite a lot, especially for complex queries. It's going to blow up your context. And each chat could be costing you like 10 pence. Obviously, at scale when you have millions of users, this is not really feasible. And then, you know, like the web search providers are also like completely up to the labs as well. So, for example, in in our development, what we see was like was we were using a model for a good amount of time. And then overnight, they shipped an update and for some reason web search degraded and it was completely out of our control. And we generally had no idea like what was going on apart from just like switching providers. But we want to have more control over that because it affects our user user experience. And you know, like there's literally billion-dollar companies who do web search. So, that kind of tells you that it's what's much more than just adding a web search tool to your LLM pipeline. The other thing that's super important for apps like Cronulla is the output. So, the summary that you saw was pretty good for what I would expect, but someone in sales might expect more of a deal focus. Someone in engineering might expect like action items, blockers, or like linear tickets. HR might want something completely different. And the thing is that one prompt can't generally serve everyone. And you know, LLMs are stubborn and we need to figure out how to get inside them and make them work how we want it to work. And yeah, as you as you know, like LLM behavior is largely seen as like a black box, but we want to kind of go very deep into the details and figure out exactly what's going on. So, what we did recently at Cronulla is we started building our own tracing tools. And obviously, thanks to LLMs, you can actually one-shot these things. And this is where one-shotting is kind of nice. And so, we built our tooling tracing tools here where we basically have complete visibility on the tool calls straight from the beginning to the end. So, we have full visibility over the individual tool calls, why it's making those tool calls, the search tools, the reasoning tools, the cost structured exactly how we want it. And the most useful part of this is that we structured the data exactly how we want it. And the UI is built to like serve our our employees internally, not just like engineers, but also product, data, and like CX, and everyone. So, you don't have to like, you know, go into CloudWatch and do like very complex queries to figure out why something failed. And that's been like the key for us in like figuring out this black box. And previously, obviously, building this kind of tools would be like up to using a SaaS provider. And it simply wouldn't you simply wouldn't have the time. But now you actually can spend time building this tracing tool that actually serves what you need. And this is obviously a very basic example, but obviously you can use OpenTelemetry or like other providers. But we essentially just like save things to a DB, wrap around like AI SDK, and then the front-end is like kind of like the most important part cuz that's what people are going to use to figure out what breaks and what doesn't. And we literally have like our founder literally goes into like the details like following the agent loop completely front to back to figure out exactly what went wrong. So, then at the end of this, you can actually figure out like, you know, this output feels off to like exactly what failed. And then when you iterate, you can improve on those things. But as I said earlier, this is going to be more more than just like basic LLM stuff. And LLM behavior is obviously part of the picture. The how users interact and experiences your product is also very important. So, with LLMs, you can one-shot more things and you can have more variants, which we like cuz we can experiment with different features. We can experiment with like one feature looking very different in four different users. But the problem for us specifically at Cronulla was that we are a desktop app, which means you can only run one instance of the app at a time. And there was a lot of friction when it came to like testing new features, different variants, and actually testing those in parallel. >> [clears throat] >> So, before, you know, before you'd have to like run the Electron app locally, install the dependencies, and test things. If you wanted a coworker to to test those changes, you'd have to get them to do those things as well. We We didn't have the same luxuries as like web apps do. So, essentially, what we did is we took our Electron app and we turned the front-end of the Electron app into a web shell. And this was deployed online. So, now our CI, whenever we open a PR, we get a preview link and we can go and test those things. And this generally sped up our development time so much more. And like the cooler part of this is that because LLMs can now self-verify their work, these guys are now like once we open a PR, Cursor goes and tests it, uploads a screenshot into our PRs, which speeds up the testing so much more. And again, this is like you might think that this is a lot of work, but it's actually quite simple. So, what we did is for those of you are not familiar with Electron, there's obviously a main process and a render process. The main process works with the system APIs and the render process is basically your front-end. And essentially, we abstracted our IPC APIs, which is the system APIs, to fall back to web standards when we're in the web environment. And similarly with React APIs as well, like routers, sessions, and query layer, we move those to the web standards. And essentially, this just made the render agnostic of of Electron. And we can just simply run it as a web app. So, this has helped us on top of the LLM improvements was like we were able to just like change and like test like one feature in like multiple different variants. So, like whatever the end product is actually feels super good cuz we know that we've tried so many different variants. And we actually felt those products in in like in practice rather than just like seeing it in Figma. So, essentially, this this is basically a long talk to tell you that the answer isn't to one-shot better. It's about figuring out how you can make that feedback loop where it kind of feels like playing a tennis game with LLM. So, the end product feels more like magic rather than just like a black box and hoping that the feature that you're going to release works well with customers and having that conviction that what you're shipping is actually going to connect to the users. Thank you. Any questions? >> [applause] >> What do you think about re-platforming from Electron to Tauri? We've thought about moving to Tauri a couple times. Um I think the way Electron serves us right now has been super nice. Like the APIs changing quite a quite a lot. We've tried Tauri before as well and we didn't really see massive performance gains, which we which is what we care about the most. So, yeah, it's been discussed before. We've played around with it, but haven't shipped it. Cool. Thank you, guys. >> [applause] >> Yay! >> [music]
