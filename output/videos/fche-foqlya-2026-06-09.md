# fCHe_fOqlYA
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-06-09 |
| **Type** | Video |
| **Duration** | 13:05 |
| **Views** | 57,046 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/channel/UCKWaEZ-_VweaEx1j62do_vQ) |
| **Subscribers** | 1,740,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=fCHe_fOqlYA) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Learn more about Agentic AI here → https://ibm.biz/~6aANCV7hW

Scaling AI agents sounds easy - until everything breaks. ⚠️ Sam Anthony explains why scaling agentic AI systems increases cost, latency, and failure risk. Learn how multi-agent design, coordination, and system architecture shape real-world scalability.

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/~c87KW8VoF

#aiagents #agenticai #scaling #aisystems
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
| **Characters** | `9969` |
| **Error** | `none` |


Agents are easy to demo and surprisingly hard to scale. It's now easier than ever to build a working demoable agent that can complete meaningful tasks end to end, which naturally leads to the next obvious question, why not just scale it? More steps, more tasks, less supervision. But before we push that further, we need to take a closer look at what actually changes when you start scaling agentic systems. And how scaling agents is not quite as simple as it seems. In traditional software systems, scaling is a well-understood problem. As demand grows with more users, more requests, more data, you add. This can happen in many ways, such as horizontally by adding machines or containers, or vertically by increasing CPU, memory, and storage. But fundamentally, more users means more infrastructure, which results in the same behavior. Agentic systems break this pattern. Yes, they require infrastructure scaling, but when people talk about scaling agents, they're often mixing two different ideas, traditional scaling of handling more requests and expanding capabilities to enable the system to do more. And it's the second one that changes everything. The scaling we're going to talk about here is making these AI systems work reliably across wider scopes and more complex tasks. To understand why this matters, let's look at how agents actually operate. Most agents follow a simple loop. They plan the tasks into steps, execute by using tools to act, remember and store relevant context to memory. And reflect on any actions to evaluate what worked and what didn't. For narrowly-scoped tasks, this works remarkably well. The problem is bounded. The system makes a few decisions and completes the task and stops. With this success, we naturally decide to scale it. Maybe you want to expand into another domain or to a new suite of features users have been requesting. At first glance, this seems like a straightforward extension. Just give the agent more tools, more knowledge, and broader responsibilities. That's where we hit the first large challenge. While the agent loop doesn't change, the cost of each execution does. For a narrowly-scoped task, the agent might plan a few steps, make some tool calls, and complete in a handful of seconds. Token usage is small, and latency is not very noticeable. But as you scale, planning takes longer. Execution becomes more demanding as the agent has to decide between more possible tools and actions. Memory grows, increasing the context passed into every step and requiring more effort to fight through the noise. Reflection also becomes more expensive and less reliable as more context begins to dilute useful signals. What used to be quick, cheap interactions no longer scale cleanly. Latency and costs scale non-linearly, as each decision requires more context, more reasoning, and more careful selection between actions. It's not just that we have added more features, we've multiplied the complexity of decisions the agent has to make to complete even simple tasks. The immediate consequence is simple. Scaling agentic systems increases the cost per decision, and ultimately, the cost per successful. outcome. Now let's assume you're willing to pay these costs. You are still not in the clear. Something more subtle and more dangerous happens next. Let's illustrate this with a simple example of a travel agent. You say, book me a trip to Washington. The agent gets started by building its plan for your upcoming trip to Washington, DC. It executes tools to find flights, book hotels. And organize transportation. And all of these execute successfully. A few minutes later, we have this great trip fully planned and ready to go. But the initial assumption was wrong. The model misinterpreted the request Washington as Washington, DC when you actually met Washington State nearly 3,000 miles away. And now that assumption drives the plan, influences the execution, and gets written into memory. This tiny error... poisoned the entire interaction, not just wasting money, but wasting your time. This is the key shift. Failures are not isolated, they propagate. The system didn't just make a silly little mistake, it spread that mistake across time. This is dangerous because as agents scale, they make more decisions under uncertainty, not less. And because the system is operating autonomously, there may be no natural checkpoint where a user could come in and easily correct it. So let's take a step back. As we've discussed, scaling agents is not something we can treat as simple extension. It requires architectural changes. A single agent doesn't scale well because it owns everything, every decision, all memory. As that scope grows, the context becomes noisy, state becomes hard to manage, failures cascade easily and per task cost continues to rise. This is not a model limitation, but rather a consequence of how responsibility is distributed. The core issue here is ownership. When a single agent is responsible for everything, every decision becomes more expensive, more complex and more fragile. There are no clear boundaries or separation of concerns. The limiting factor is less the capability of the model. And more how much each agent is responsible for. That's what determines whether the system scales. In other words, it's a systems design problem, not a model capability problem. Imagine a company where every single decision, let's say engineering, marketing, hiring, support, all has to go through one person. As the company grows, even simple decisions take longer and longer because the person has to understand more context, consider more factors, and switch between specialized domains. Agents are the same way. When responsibility is centralized, the bottleneck isn't the effort but the growing cost of making each decision. So what do we actually do about this? Moving away from a single agent, We decompose the system. Into multiple components with bounded and distributed responsibility. Each component operates with less context, makes fewer decisions, and has a narrower scope. Together, they form a system where individual decisions are cheaper, faster, and easier to reason about, while complexity and failures are contained rather than compounded. This is where multi-agent systems begin, as a consequence of scaling correctly. By distributing responsibility and decomposing components, we begin to regain control over decision size, cost, latency, and failure propagation. Once we move into the multi-agent design space, we introduce a central challenge of managing how agents coordinate, share work, and manage dependencies. As systems grow and evolve, you must decide how to scale their capabilities. One path is horizontal, introducing new agents to take on distinct responsibilities. This makes new capability easier to access and reuse, but as the system grows, coordination becomes the limiting factor and communication overhead increases quickly. The other path is vertical, increasing the capability of individual agents through additional tools or subagents. This reduces the need for coordination but can increase latency and complexity concentrated in each agent. Realistically, this shows up as a question of capability placement. Should a new capability live as its own agent or be embedded within an existing one? Let's consider a research assistant agentic system. We have a central coordinator agent and sub-agents for retrieving documents, refining search queries, and finally for synthesizing the results. If we want to introduce fact checking, one option is a dedicated agent that evaluates outputs across the system. This works well because fact checking is a distinct reusable capability with its own logic and policies. Separating it keeps responsibilities clear, but requires an additional coordination step. In contrast, consider adding the capability rank and filter retrieved results to get more relevant documents. This is best embedded within the existing retrieval agent because the capability is tightly coupled to the existing agent's retrieval process and depends on shared context across steps. Splitting it into a separate agent would introduce unnecessary coordination and kind of fragment the decision process. So there's a trade-off. Systems that scale more horizontally must invest more effort at the coordination layer. Systems that scale vertically must manage growing complexity and cost of these individual agents. In both cases, complexity from scaling to new capabilities is shifted. The decision really comes down to how expensive coordination will be versus how much complexity an agent can reasonably absorb. A useful rule of thumb is to split capabilities when they are reusable and independent, and embed them when they're tightly coupled and context-dependent. In practice, agentic systems that will actually scale are those that balance these forces and deliberately choose where the complexity accumulates in coordination, in individual agents, or in the structure that connects them. At every stage, scaling introduces a new constraint. Cost rises, latency increases, failures propagate, and coordination becomes harder. Scaling AI agents doesn't just amplify capability, it amplifies everything in the system at once. The teams that succeed are those who understand these challenges and constraints and make deliberate architectural decisions about what is allowed to scale and what is kept bounded. All of this might sound like a lot of problems. But it's actually where the opportunity lies because once you understand how decisions flow through your system, you can shape how those decisions behave at scale. The teams that win won't be those with the most capable agents. They'll be the ones that design systems where decisions are bounded, costs are intentional, and intelligence compounds instead of collapsing. The goal in scaling agentic AI is to design systems that can survive. And benefit from their own successes.
