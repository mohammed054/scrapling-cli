![Thumbnail](https://i.ytimg.com/vi/D37Ijn2o5U0/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBQgpvEFRxTGuBqkB9IVJXGuhmzvQ)

# Why Agentic AI Fails: Infinite Loops, Planning Errors, and More
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-14 |
| **Type** | Video |
| **Duration** | 12:45 |
| **Views** | 29,735 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=D37Ijn2o5U0) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Learn about Agentic AI here → https://ibm.biz/~7tIAS4ONO

Agentic AI failures aren’t random—they happen for clear, predictable reasons. Meenakshi Kodati explains the top failure modes in agentic AI systems, from infinite loops to hallucinated planning and unsafe tool use 🤖. Learn how better design, constraints, and monitoring improve reliability.

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/~AONs89iwu

#ai #agenticai #aisystem
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
| **Characters** | `10010` |
| **Error** | `none` |


When an agentic AI system fails, the most common reaction we get is the model probably hallucinated. Now it's quite understandable why we come to that conclusion. Because in the past, the large language models have been known to be extremely inconsistent. They are probabilistic models. They're not deterministic. But in the last couple of years, there has been a lot of improvement in the architectures of these models. And today, we are able to get consistently good outcomes from them. So today, when an agent-ic AI systems fails, is it's less likely because of model failure or prompt quality. It's more likely that there are flaws in the system design. Now there's this common perception that agentic AI system is nothing but a large language model with access to tools. When in fact the definition is that it's a much bigger system that can Observe. And it does this in a cyclical or iterative format in order to drive more consistent results. So because of this complex system, we see more types of failures today than we did in the past with just simple chatbot applications. In this video, let's dive in and understand what are three most common failure modes of Agent AI systems. Let's understand why these failure modes happen. What we might be able to do to mitigate or prevent them in real world scenarios. Let's start off by understanding the most common failure mode, which is the infinite loop. Like the name suggests, this is a scenario where the agent repetitively performs similar or same tasks without making any meaningful progress towards the completion of its goal. Let's understand with an example. Let's say you task an agent to find a document for you. The agent starts by configuring the search. It's gonna call a search tool and word the search in a certain way so that it can get relevant results. So firstly, it's gonna start searching. Then once it gets the results, it's going to evaluate those results. If this results could look good, it's going to give you the answer. If this don't look good it's gonna start planning again on how to do this better. It goes back to searching. It might word it in a slightly different way to do the next retry. And then it's gonna evaluate, and if it's not looking good, it's going to plan again. Now let's assume that this document that you requested does not exist in the system. Now the agent does not know that. So each time it does the search, it is getting results, but the results are pretty vague. So it's gunna replan and retry again and again until it gets the answer. But here, the truth is it cannot get the answer because the document is non-existent. So basically, the agent is stuck in an infinite loop of retrying and planning, evaluating, and searching. So this is what we call the infinite loop. And one main reason this happens is that there is no proper termination condition. Meaning that the agent doesn't know when to stop trying. Another reason this happens is with each retry, we don't know whether the agent is actually searching differently. Has it fundamentally changed its approach in searching? If we are not tracking the action of the agents, then we wouldn't know that. So not tracking actions. Is another reason. The third reason is not tracking the progress of the agent. Now with each retry, is it getting better results? Now if you're not tracking that, there is no way that we know whether the retries are successful or not. So the agent keeps trying and getting the same results and not making any progress. So lack of progress tracking. One way to mitigate this, and the most simple way, is by setting the termination conditions. So set up a max retries, or it could be max number of steps that the agent can take before it decides that it cannot find the answer for you. It could also be the max runtime usage. So that way, you're not stuck in this loop where you're wasting resources like compute and the API costs are going up. Secondly, you can also start doing the action tracking, where you actually look at the actions that the agent is taking, compare them with previous actions and see if they're significantly different. If the search is similar across all the retries, then there's no point wasting your compute to search with the same criteria. So that can help you mitigate the infinite loop scenario. Progress tracking will ensure that you are getting better outcomes with each retry. So when you track progress, let's say in this example, you will know whether you're getting better results with a retry or not. So that way you can mitigate this infinite loop scenario if you're not getting better result with each retry. That is how you can Mitigate Infinite Loop. Now, this is not a super serious failure mode, but it will lead to wastage of resources and increased costs. And it is important that we account for it and design the systems to mitigate this particular failure mode. The second failure mode that we are going to talk about is called hallucinated planning. Now like the name suggests, this is a scenario where the agent is gonna come up with a plan that's plausible versus possible. In other words, it's gonna come with a plane that looks great on paper, but fails at execution. Let's understand with an example. Let's say you ask an agent to book you flights to Milan that are under $500. The agent is going to take the task and come up a very beautiful plan. It's going to say, hey, I'm gonna. Use the travel booking API and search for flights. I'm gonna set a filter for flights that are under $500. I will book them and I will send you a confirmation email. Now that looks like a great plan, but it will fail at execution because you probably did not configure that agent with access to the travel API. You also probably did no provide your email address for it to actually send an email to you, or it probably does not even have access to an email tool. Now, this is a classic scenario where the agent is assuming things and assuming capabilities instead of relying on what it actually has access to. Now, let's look at why that might happen. Firstly, it can happen because your tool capabilities are not well-defined. So the agent doesn't know what your tools can and cannot do. It can also happen because you're asking this agent to plan and execute without separating those two things out. So basically there is no validation. Of the plan that's happening before the plan gets executed. So you are hit with errors because the agent executes things that cannot be done. It can happen because the agent is assuming capabilities instead of checking for constraints. Constraint shape. So how might we go about mitigating this? Firstly, you should start describing your tools very clearly to the agent. Clearly describe what the tools can cannot do. Clearly define the tool schema and let the agent understand the capabilities and limitations of your tool. Next, you can go with architectures such as multi-agent. Where there is a verifier agent in between planning and executing. So the verifier agents could look at the plan and say, hey, this cannot be done, or this can be done. You could also have a human in the loop instead of a verifying agent for more serious and high-risk plans. So that way, your plan is validated before it goes on for execution. And thirdly, make sure that you clearly specify the constraints. So let the agent know that it's- can do these things and cannot do a certain set of things. And instruct the agent to ask for clarification before making assumptions. The agent could say, do you want me to use a travel API instead of just straight away making up a travel api by itself. So by setting those things in place, you will ensure that your agent does not get stuck in the hallucinated planning failure mode. Let's jump into the final failure mode, which is the unsafe tool use. This is a scenario where an agent executes an action that is technically valid, but could be risky, destructive, or unintended. This happens mainly because the tools are overprivileged. Let's understand with an example. Let's say you have an agent that is supposed to go and delete outdated records from a database. But instead of deleting outdated records or archived records, it's going ahead and deleting active records that are important to you. Another example is that of an agent that sends autonomous emails or automated emails to recipients with content that has not been reviewed. So this also happens when there is no proper approval workflow in place. It also happens when there is no clear distinction between the read and write axis that you give these tools. How might we go about mitigating that? Firstly, it's important to give only those privileges that are needed to the tools. So it's always good to adopt a principle of least agency. With the tools because mitigation starts with permission design in this scenario. Also create a proper approval workflow for high-risk tasks. If needed, have a human in the loop to review the task before it's sent for execution. So having an approval workflow is extremely helpful. Third, separate the tools into tiers based on the kind of access. So, print out. The tools based on whether they have the read axis or write axis or a delete axis. That will ensure that one tool doesn't go ahead and commit actions that it's not supposed to be doing. By following these principles, you will be able to mitigate the unsafe tool use, which actually could be pretty damaging to the reputation of the company. So it's very important to actually design your system to account for this failure mode. Agentic AI failures are not random occurrences, they are very much predictable. And they happen for a reason. They happen because of too much autonomy or too little constraint. Or they also happen because there is no proper monitoring or tracking in place. Let's remember that engineering discipline is key to building reliable agents. I hope you found this information helpful. Thank you so much for your time.
