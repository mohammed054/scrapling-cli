![Thumbnail](https://i.ytimg.com/vi/SbrEk_tXZaE/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLDviDjoNUsDNW7xWYf5CQu_3Yo0LQ)

# Why AI Agents Break Zero Trust at the Last Mile
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-17 |
| **Type** | Video |
| **Duration** | 13:14 |
| **Views** | 19,267 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=SbrEk_tXZaE) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Learn more about AI agents here → https://ibm.biz/~U3UAW2b58

AI agents fail where legacy systems begin. Grant Miller explains the agentic last mile identity problem and why it creates serious security risks. Learn how identity, context, and delegation protect enterprise systems in real deployments.

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/~NUDoEEkHl

#aiagents #zerotrust #aiarchitecture
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
| **Characters** | `10771` |
| **Error** | `none` |


Howdy everyone. In this video we're going to investigate the agentic last mile identity problem. This is the critical gap between an AI agent's high level reasoning and its ability to reliably integrate and execute in real world fragmented systems, which open security risks. We'll look at the last mile challenge. And discuss how to address it. Before we dive into this, let's start with what is a last mile problem? One of the most traditional ones that we've have come across was actually around internet providers trying to get high speed access to people's homes. Now, they were able to build very big and fast trunk lines, which were super fast, but the challenge they had was, how do I connect this to homes that have been built years ago, if not hundreds of years ago that have existing infrastructure. They have high speed trunks. But how do I get it to an old existing infrastructure and get those high speeds in? That was the problem that internet providers were faced with. How do we get that last mile to the house to get them the high speed access that was available? And these are the kinds of things that we're looking at in the agentic world. When we think about agentic and the last mile challenge, let's start with by reviewing an AI and agentic system. Let's start with, we have a user, they're happy AI user, and they're going to connect with a chat or some application that's AI enabled, and they are going to ask questions. That's going to go off to an agent, we'll call this A1. There's likely an LLM in here that's interacting and providing reasoning and intelligence. That's getting to in turn talk to possibly an MCP server, and behind this, we're going to have either some processes that we want to run, or we're gonna have possibly data that we wanna connect to. So we're to have these connections. Now, when we think about this system, this part is where we're really emerging today. We're building these agentic systems that know how to talk, know how to reason, know how to execute, know-how to communicate, whether it's 808 or some way. This is all pretty new and we're building this out and we know how to do this. This piece that we're connecting back here, this is actually our last mile. These are systems a lot of times in companies that have been around for a long time. They're, at least in the agentic sense, legacy systems. They were not built with agentic in mind. They were built with applications trying to talk to them. So this is how do we connect this world, this emerging world of agentic to the last mile, to our systems that have been around for a long time within an enterprise. All right. So when we're thinking about this, the first thing we want to talk to, okay, so we have our last mile. Why? Is this a challenge? Alright. The first thing when we look at this whole system is that the end of this is not verifying the user. In other words, we have a person here. They come in. They log in. We know who they are. We know in the chat. We know when the agent. We know all through this flow. We know exactly who that person is. When we get to here, a lot of times these systems may be running and connecting with like an API key or they have some sort of shared credentials. In other words, you've got, traditionally, we've got two applications that are trying to talk to each other and they have their own credentials between the application and data or processes that they're trying to connect to. None of that really contains any information about who that user is. So we lose verifying at the very end who it is that's initiating the prompt into this agentic system. So that's the first thing that that we need to think about or why we have a challenge with the last mile. The next thing is that the end is not checking a certain set of things that we think about in an agentic world. So the first thing that it's not checking is the specific intent. And that really gets to, all right, we have a user and they intend to change a password or change some data at the very end. That's their intent. When we're dealing with an API key or just credentials between applications, that intent gets completely lost. The same thing is true for context. We lose the context. What is the environment that we're working in? What are the systems in this agentic system that we are talking about? That gets lost when we get down to this point. The other thing that we lose or is not available is delegation. Again, if we're dealing with our backend legacy applications and they're dealing with certain ways to connect, when we're looking at agent one has been working on behalf of the user, we've delegated our work to this agent and that's coming and doing something, we lose that. We don't know that an agent has had its, is working on the behalf of a user. So that's another piece that we lose into this. And at the end of this, because of this if we leave this whole last mile challenge alone what happens is what's left unguarded then is that we break zero trust. First thing we do is we lose our ability to have zero trust because we now have lost everything from the left to the right behind and now we don't have zero of trust. The other thing... that happens, if we leave this alone, is it allows agents actually to chain tools. And what this really says is that, now that these are just connected through kind of you know, traditional connections. An agent can say, I want to call this API key. I've got another one. I can just start chaining all these processes together because we don't have the context. We don't the intent. We don't have a lot of that. So now we can chain this. And ultimately, what happens is that this whole system, because of the last mile challenge, becomes a target for attackers. In other words, we could have a rogue agent, here's rogue one, and it's connecting, it's trying to infiltrate into our system, and it is actually connecting to MCP and says, hey. I am a good agent, and please connect me to these backend processes and these backend data systems. And yes, use whatever it is you need to connect. So this is ultimately what happens is we really open ourselves up to a lot of risk. All right, so now when we kind of know how what the last mile problem is, we know what the challenges are. Let's start talking about the last mile and what to do, how do we fix this? First thing that we need to do is we really need to validate. Identity. Context. And delegation. When we get to the end, we're going to need to know who the person is, what the context is, and what the delegation is. Now, you can say, okay, that's a lot easier said than done because these are systems that are operating off of a different environment and a different way of connecting. So how do we actually validate this? Well, one part of this is to use policies. Via ABAC. And PBAC. Okay, so this is attribute based access controls and this is policy based access control. So we want to actually start adding that in back here. Whatever we're connecting to... we want to make, start having our access control set up here. So they actually take the attributes. Attributes, one attributes are, is the environment. Another attribute is the subject, the user. And so we can bring that together and have policies then on our legacy systems that take into account different ways of doing access control and can start applying things that we need to understand what's the context, what's they user and how are they trying to access stuff. The next thing that we can do, and this is where this really starts bringing in how to achieve the last mile problem, is we can connect the last miles via a vault. So this is now we're going to bring into the middle here, we're gonna bring a vault. And this is a place to store and control operations. So instead of going this path, we will actually go to a vault and the vault will connect off to our tools. Now, with our vault, we can do a handful of really powerful things. One, we can we can the validation that we talked about. We can look at, so now this is really kind of part, it's kind of bridging between our agentic systems in our our legacy enterprises so we can actually know who the user is, who the audience is, what are the claims that are coming in. So we can bring this all into the vault and understand those things that we need to do to validate all this information, identity, delegation, all that stuff we can do here. The next thing is that we can make this policy-based. So we bring in these policies in into the vault and say, okay, if we understand the identity, delegation, all that, what policies can we implement then to connect to our enterprise and back-end systems? And the nice thing with this is we can actually now start issuing short-term credentials. In other words, Instead of having long-lived API keys or long-live shared credentials on the back end, we can actually start doing credential management and access management, bring those in. And do a rotational thing where we can actually now assign a new credential to access the back. These are things that enterprise systems know how to do and make them very short lived. So we bring in the user, the user says what they wanna do, we understand the context, we understand intent. That then says, the vault then says okay, I'm gonna take a credential, swap that out, so we store this with all in the vault and we swap out a short term credential then that now connects to these backend systems. And by using this, we kind of set up ourselves a little bit of an abstraction layer that, like I mentioned, bridges between the new evolving agentic world and our legacy backend system, allows us to interact and integrate with the backend while not losing many of these things, you know, the risks and challenges that we identified. The last thing that we kind of want to do then is we also want to have telemetry. That we can use to deny. Or narrow. Our permissions. In other words, we want to start collecting and storing telemetry. And this is what's happening. As users start interacting, as agents start interacting with the system. We start having our policies in place, we have the vault in place. Now we start collecting the behaviors, seeing what's actually happening, and that telemetry can then feed back into our policies. These policies feed back in to our vault so that now we can remove access or the next time somebody comes in we can actually restrict the privileges that are coming in. All right, as discussed, while many companies are currently exploring and employing these agentic systems. The last mile identity problem remains a challenge. So what kind of challenges and solutions are you looking at to solve this problem? Please comment below and thank you for watching.
