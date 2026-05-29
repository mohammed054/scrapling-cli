![Thumbnail](https://i.ytimg.com/vi/kqj22mWIdjU/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLDdqZ1OoetOLOwC77P_Y1TvN7OuWQ)

# Building a Team of AI Agents: Roles, Feedback, & Teamwork Explained
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-04-28 |
| **Type** | Video |
| **Duration** | 9:58 |
| **Views** | 46,355 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=kqj22mWIdjU) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx AI Assistant Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdpZBd

Learn more about How To Build an AI Agent here → https://ibm.biz/BdpZBD

🚀 Can AI agents work like human teams? Lauren McHugh Olende dives into AI teamwork, explaining how planners, tool operators, and critics collaborate for smarter workflows. Learn how collaboration, the ReAct pattern, and feedback loops optimize AI workflows for solving complex tasks.

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdpZBR

#aiagents #react #promptengineering #aiteam
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
| **Characters** | `7597` |
| **Error** | `none` |


AI agents are meant to solve tasks that are complex, tasks that a stand-alone LLM cannot solve with just its pretrained knowledge. But in artificial intelligence, just as in human intelligence, more complex tasks require teams of collaborators. Each contributor has a unique role and those contributions come together into a single output. In fact, building a team of collaborators within your agent looks surprisingly a lot like building a team of collaborators in a human team. You'll have doers, thinkers, supervisors, communicators, other roles that increase brain power and bring in special skills and knowledge. Understanding these diverse roles and how they fit together will help you build the right team for your agent. Let's take an example of an agent that develops a mobile app. The agent takes input from the prompt, creates a set of user requirements, plans app architecture, generates the code, tests it and ultimately publishes it. There are two questions to ask about the team design, which is "What are the roles that you need within your agent?" and "How will you make each of those roles especially good at their job?" Every agent team design will be a little bit different, but there are several types of roles or subagents to think through. The first is present in any agents and that is a doer. In a human team, these would be equivalent to your junior workers, and they do things like write or code. On their own, they can't do a more complex task like build an entire mobile application but they can handle individual steps if someone else has a view of the bigger picture. And that brings us to the planner agent, who takes the input from the user and creates a plan for how to break that input into smaller steps. So in the mobile app example, that might actually mean two planning steps. First is a plan around what the user requirements are, and a second is a plan of the app architecture before the coding even begins. So the skill of this role is to break down a complex problem into smaller pieces, determine the skills and knowledge that are needed to execute those, and come up with a documented plan, but just the plan. Next is a tool operator. This role involves interacting with tools, like APIs or discrete pieces of Python code or web services. This team member creates a structured tool input or a tool call with the required arguments and then outputs the tool results. Your agent may also need a learner. So just as a human team might hire someone who likes to read a lot and stay up to date on the current trends in the market, in an agent, you also need a role to gather input from the outside world. In our mobile app development example, this agent might retrieve info on potential competitor applications or user requirements gathered from blogs or social media to deduce what features users would like to see. The skill here is in retrieving information from the outside world, determining what is relevant and then feeding that back into the planning or doing steps. As you may have guessed, this role often is your basic RAG flow, but it could also be a more rules-based information or data retrieval step instead of something that's strictly AI-driven. Next is your feedback or critic role. So, just as many human teams have that person on the team that can be quite blunt, agent teams also rely on feedback. So a critic subagent might do something like review the responses to check for hallucinations or write and execute QA tests for the generated code. Alternatively, just as in human teams, you might foster healthy competition among team members. A critic agent might also score multiple inputs and choose the best one for the job. Next is a supervisor agent or subagent. And this can be a agent or a subagent that supervises at the task level, embedded in each role checking progress, or at the project level. So making sure individual roles are not getting stuck or helping to identify where a step in the agent fails. And then just like at the end of a group project with a human team, you have to pick someone to present the group's work. So the final role is the presenter. In the agent context, you need this role to bring the pieces together to communicate back to the user. In our mobile app development example, this role might summarize the user requirements that were created, explain the code base that was generated and what it does, to report back to the user what app it actually built. You might note that some of these roles, such as the tool operator and the learner are themselves in some ways considered stand-alone agents in the sense that they are an integration of multiple LLM calls and a tool call or a step to do retrieval and embeddings. Some combinations of these roles have become quite popular, so you may have heard of the ReAct pattern, which includes an action step, which is a tool operator role; a reasoning step, which is a planner role; and an observe step, which is a feedback or critic role. These then come together into an answer, which is a presenter role. These are great simple starter examples, but as you scale and need your agent to perform more consistently over a wider variety of tasks, that's where your team will grow too, to give better-quality outputs through more planning, more focused execution and its own internal feedback loops. The next question is "How do you make a role or a subagent good at the job it's supposed to do? ' There are a few different ways of doing that. And the first is prompting. So the same as you would give instructions to a member of your human team, you need to give instructions as well through the prompt to your agent collaborators. That could be as simple as things like, if you get stuck, retry and try again, which is something that you might also have to tell members of your human team if they're just getting started. The second is model selection. So the same way that it's important to hire the right human collaborators from the get-go, it's important to select a model that fits the role. And that can be in terms of the model's specialization, the model size, whether it's a thinking or reasoning model or not, the persona and the character of the model, all matter as factors you can take into account when seeing if the model you selected fits the role. The third is model tuning. This would require giving the model both good and bad examples of what success looks like in their task. This is a more resource-intensive way to make a model good at its job because it requires both the human resources to create that ground truth dataset, which often requires many examples and input data points, and the computational resources to be able to retrain or fine tune a model and change its weights towards the desired behavior. And fourth is the context. So in the same way that onboarding a new team member often means giving them access to the right systems, the right files, the right databases, the right subscriptions and not giving them, not overwhelming them with too much, you have to choose wisely about what context your agent may need and then what might just be a distraction. Just as a startup can launch with a few smart, hardworking teammates solving a simpler problem, an agent can also begin by pulling together just a few key roles to quickly get to a working solution. But just as a startup team eventually starts to expand, to fill in weaknesses, to fix bugs and polish up the product, the team within your agent will need to grow as well, across various roles and specializations to create a stronger and better solution.
