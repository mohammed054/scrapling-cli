![Thumbnail](https://i.ytimg.com/vi/DCZZ3AJKzuc/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAr6MBYZG3ZN1YfExMbmDHjxwYaAA)

# Give Your Chat Agent a Voice — Luke Harries, Head of Growth, ElevenLabs
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-14 |
| **Type** | Video |
| **Duration** | 8:11 |
| **Views** | 3,934 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=DCZZ3AJKzuc) |
| **Category** | - |
| **Language** | - |
---

## Tags

`ai` `ai engineer` `ai engineering` `software development` `tech` `startups` `software architecture` `machine learning`
---

## Description

Chat agents dominated 2025. Every product either went AI-first or got left behind. But text-in, text-out is already starting to feel dated. Voice is faster, more accessible, and opens up interaction paradigms that chat just can't touch — phone lines, Zoom calls, screen readers, ambient interfaces. In this talk, Luke Harries from ElevenLabs argues that the next upgrade for every chat agent isn't better prompts or smarter RAG. It's a voice layer.

The problem is most teams have already built and tuned their chat agents. They don't want to throw that out. This session shows how ElevenLabs' Voice Engine wraps any existing agent in a few lines — handling turn-taking, speech-to-text, text-to-speech, and emotion-aware interruption detection — without touching the underlying logic. There's a live demo of converting a working chat support agent to voice in a single prompt, plus a look at the client and server SDKs, Shadcn-based UI components, and how tool calling still works through the wrapper.

Speaker info:
- https://www.linkedin.com/in/luke-harries
- https://harries.co/

Timestamps
0:00 Introduction to voice-first chat agents
0:20 The shift from text-based to voice-based interactions
1:43 Evolution of agent architecture and challenges of rebuilding
2:47 Introducing the ElevenLabs Voice Engine
3:32 Overview of the server and client SDKs
4:36 UI components and deployment demo
5:56 Summary of voice engine integration paradigms
6:37 Predictions for the future of AI agents
7:00 Q&A: Handling tool calling and integrations
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
| **Characters** | `7326` |
| **Error** | `none` |


[music] >> And so really excited to talk to you about giving your chat agent a voice. Um and 2025 was the year of the chat agents. And I think you either like died a SAS or you became AI first by adding a chat agent to your app. And so lots of you probably saw this tweet which went viral where it was linear post hog SEO where they all went and added their home screen is now the chat interface. And I actually really agree with this. It's like that's the default way that you want to now be interacting with AI. You can use the tool calling, you can use the rag. It's just very declarative. It's a great quick start. You even have the government doing the same. This is the gov.uk um approach into chat agents. Chat's cool, but it doesn't feel like you're building the future though. And I really think voice is this natural medium. It's way quicker, it's way more interactive. It's also much more accessible to lots of people who struggle with keyboards or dyslexia, voice is a much more natural medium. And it's also omni channel. As soon as you add voice, you unlock all these different type of interaction paradigms. So let's say you were post hog, well now your agent can actually join a zoom call and start like correcting you if you're saying wrong stats. Or if you're customer support, you can now add a phone line. And so what we really need to do is upgrade all these chat agents into voice agents. And oh. There's a there's some transitions. Um and what we found when we're building with companies is we first started 11 labs, we were like, "Okay, let's just build the best text to speech models in the world." And then we kind of got pulled into this big solution of how do you now build these agents? And we're working powering customers like Revolut's customer support. And all of them kind of end up looking like this where you have this voice engine where you do the text to speech, the turn taking, the speech to text. You then have this agent orchestration where you combine your LLMs, your rag, your different tool calling, your all your integrations. Probably a bunch of us in this room have either built the same system or pitched the same slide. But what we found is when we were starting working with these customers, loads of them went, "Yes, we're starting from scratch. That's great. Let's use this out of the box one." Um but for lots of them, they'd actually already built this. And they were like, "Well, hold on. I've already got my agent. I spent loads of time doing the evals, the transcriptions. Why would I need to completely replace and rebuild with what I have?" And so that's why we're I'm giving you an early preview of a new product which will be coming out in a couple of weeks where we've basically taken this voice engine bit and wrapped it up into its own first class primitive, which makes it really easy for you to add and wrap any existing agent. And so this is voice engine. We combine the best models, so speech to text with scribe, which is the most accurate model, as well as the text to speech models like V3. It's got this really advanced turn taking, which is emotion context aware. It can tell when you're pausing. The it does the semantic bad as well. As well as all the different thousands of different voices and languages. And really importantly for the folks in this room, we've really cared about what does the developer experience of this look like? And what's really cool about this is you've spent a ton of time building these complex chat agents. Um but to actually add voice to that is then remarkably simple. And so this is what the server SDK looks like. We basically have this uh you create your client, you then create your voice engine. And then you add this little wrapper to your existing chat agent where you basically attach it. And then each time there's a new session started, it will kick off this loop and just kind of proxy all the stuff to your to your existing chat agent. Additionally, with the server SDK, we also then have the client SDK. And so this is like super simple. It's basically three lines you can then add and you have a widget in your site. Uh one of the cool things you actually get for free as well is once you've started adding these client SDKs, you can then also add like telephony and C SAS. And all of this is like pretty much out the box once you've wrapped it. Um and finally we have a bunch of really beautiful well thought out UI components all based on the Shaan CN and Vercel style. So you can actually just point your coding agent and give it a go. Uh what's cool is you can literally in about one prompt actually convert an existing chat agent to a voice agent. So I'll give you a quick demo now. Um So this is like your generic chat support agent where we can go, "Hello, how are you?" Perfect. It replies. Uh so that works pretty well. And this is the code all running locally. And and where when we release this, it will come with a skill which basically has all the best in class stuff. And then it's literally one prompt which will then go analyze your code base, work out your chat agent, how to actually deploy it, work out how to wrap it. Um so it should be really cool and quick to do. I'll just show you some of the code that it ends up writing. So you can see here we've got the voice engine. You attach it with each new new session, it then starts proxying it. So it should be really simple and easy to add to your existing agents. All right. We can let it work in the background. Um Cool. So that's a that's an early glimpse of voice engine. I also think this is just like a really useful paradigm which one of the community should do where we start kind of moving to this higher abstraction bundles instead of just the pure text to speech speech to text. So to summarize the two different things we now have for developers building these different voice engines um or voice agents, you've either got voice engine, which is fantastic. You spend all your time building these excellent chat agents. You can just do this little wrapper with a nice SDK. Or if you want to use a full agents platform for conversational, we've got that out of the box. It's very easy, very quick to prompt. Uh ends with a um uh a prediction. I think these chat agents will either die chat agents or start adding voice. Um I'm excited to work with lots of people in the room. We're also looking for some design partners. So if you want to be some of the first people to do this, we'd love to chat. But thanks so much. >> [applause] >> Cool. Yeah. I have how do you handle tool calling? Yeah. The cool thing about this is um your chat agent actually normally does the majority of tool calling. So it's actually already built out on the back end here. And so you can have this wrapper without needing to deal with any of the issues of tool calling. We also um at 11 labs have the concept of either client side uh tools and server side tools. So you can do some pretty cool stuff where you then like expose the tools on the very front end to like manipulate the DOM. And we're going to add in a way where you can proxy some of these tool calls to the wrapped agent. But most folks will already have all the tool calling already handled with the chat agents. Cool. Nice. Thanks so much. Thank you. >> [applause] [music] >> Cool.
