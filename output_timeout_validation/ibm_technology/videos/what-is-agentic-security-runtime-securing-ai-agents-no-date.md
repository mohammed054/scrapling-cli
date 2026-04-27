![Thumbnail](https://i.ytimg.com/vi/NH0plIdqDMk/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLDwqZ3IMmN26uluLXxKhnCQQwMgEw)

# What is Agentic Security Runtime? Securing AI Agents
---

## Info

| Field | Value |
|-------|-------|
| **Date** | Unknown |
| **Type** | Video |
| **Duration** | 4:59 |
| **Views** | 15,911 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 0 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=NH0plIdqDMk) |
| **Category** | - |
| **Language** | - |
---

## Tags

_No tags._
---

## Description

_No description provided._
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
| **Characters** | `4731` |
| **Error** | `none` |


Engineers are being tasked to build AI for their companies, but they're not identity experts, and that's a real problem. Today, we want to talk about agentic runtime security and how you can implement it safely and securely in your organization. What's that look like? It starts with an AI agent. This can be a Python application, a TypeScript application, but it can also be .NET, Java, really doesn't matter. That AI application is going to be running somewhere, generally in a cloud. Maybe it's on AWS Lambda or a virtual machine or running a container. But these by themselves don't provide any value. They have to make external connections to things. And that could be a database. That could be connecting to an LLM provider of your choice. Likely. That could also be a SaaS application. Like a Salesforce or something else. We think about these external connections. How do we govern access to those? Traditionally, we would have our workload would hard code a static credential to a database or an API key to an LLM or an API key to SaaS. We actually recommend against that. And this is what we call non-human identity. What we recommend is you start to build out what these connections are dynamically at runtime per session. What's that look like in practice? So we have an AI agent that's authorized to do read and write to a PostgreSQL database. If I was jailbroken or at prompt injection, they can read or write anything from the database. And so we want to strip that standing privilege. What we really want is for this AI agent, at the time of the session and at the time of evaluating an action, to know what it's gonna request access to and get dynamic credentials into each one of these that is session bound and intent bound. How do you do that? The first is dynamic creds. This is the practice of creating just-in-time credentials for anything you need that are time-bound and automatically revoked at the end of the session. That can be two minutes, two seconds, whatever really matters. But now we need to think about the users on top of this. AI agents are generally used by users. While there are completely autonomous agents that are operating by themselves, today what we normally see is a user in front of it. So this user interacts with your AI agent, usually via HTTP or some other interface. What about using the user identity? How do we understand who that user is and the context? Well, this is where you layer in your IDP. This can be an Okta, this can be an IBM Verify, it really doesn't matter. And AI agents will work with an IDP to understand who you are. That IDP works with you. This is how we do things like single sign-on. This is predicated on a standard called OAuth, typically OAuth 2.0, and it's Authorization code flow. You've likely seen this interaction. When you go to click log on with Google, log on with Microsoft, you'll see a redirect, and that redirect page will ask you: do you authorize this application to access your portfolio, your profile, your email address, or act on your behalf? That is the OAuth standard implemented here. But what about sensitive operations? If you're building an HR application internally, and that HR application, the AI agent, can onboard off-board employees, those are sensitive operations that can have real world impacts to your risk and to your employees and even financial security. When we have those higher-level operations that need to have additional scrutiny, this is when we recommend something called OAuth 2.0 CIBA. And what that means is this is like passkeys for agents. This will actually hit a prompt to the user's phone, completely outside of the browser context. So when a user makes a call to an AI agent, the AI determines that they want to do something sensitive. The AI agent will call the IDP, will initiate this third-party CIBA, Client-Initiated Backchannel Authentication, and prompt the user's phone and say: do you want to off-board this employee with the details? That is a really powerful mechanism around security to make sure that the operations and actions being taken are authorized by the user. It's also another layer of protection against jailbreaking and prompt injection on that AI agent. If there was a prompt injection that said off-bored all employees, I would get a notice for each one of those to my phone. To tie together the dynamic credentials with OAuth 2.0 and now adding in CIBA, Client-Initiated Backchannel Authentication, we put that code into our AI agent. That's where we do the work inside our Python or our TypeScript. We evaluate the JWTs, we create the dynamic credential, we access them, and then we automatically revoke them. And that's how we provide agentic runtime security today.
