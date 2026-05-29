![Thumbnail](https://i.ytimg.com/vi/7CrPrHgoEYk/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCIEXrzZ8khmNn5xV9dYvJIscqK3Q)

# What the Best Agents Share — Mardu Swanepoel, Flinn AI
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-27 |
| **Type** | Video |
| **Duration** | 10:21 |
| **Views** | 2,753 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=7CrPrHgoEYk) |
| **Category** | - |
| **Language** | - |
---

## Tags

`ai` `ai engineer` `ai engineering` `software development` `tech` `startups` `software architecture` `machine learning`
---

## Description

Harvey, Cursor, Manus, and Claude operate in completely different domains but share four patterns: focus modes that constrain the action space to improve output quality, transparent execution that surfaces tool calls and reasoning to build user trust, personalization that optimizes for speed to understanding rather than just speed to output, and reversibility that bounds the downside of mistakes so users take on higher value tasks.

Mardu Swanepoel from Flinn AI breaks down how each company puts these into practice. Cursor lets you roll back changes at the line, file, or conversation level and run multiple model outputs in parallel from the same input. Harvey builds playbooks from a firm's legal methods so the agent works the way the firm would. Claude surfaces a live task list alongside every tool call's inputs and outputs so users can intervene before the agent goes further in the wrong direction.

Speaker info:
- https://www.linkedin.com/in/mardu-swanepoel-000/
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
| **Characters** | `9804` |
| **Error** | `none` |


[music] >> All right. Um so, before I jump into sharing with you what I believe the best agents share, um I actually want to share a quote with you. And this is a quote that I actually keep quite close to me when I personally develop um agents. It's a quote that maybe a lot of you might be familiar with, although I do want to dive into a little bit of what Pablo Picasso meant when he said "steal" um in this quote. He didn't necessarily mean stealing in the sense of taking something physically that is not your own and presenting it as your own. Um but instead, he referred to going and looking at something, studying it deeply, really understanding it, and making it your own, and then using that to come up with something better and something unique that you wouldn't have been able to come up with have you not done this process. And that is really what I want to do today in this talk. I want to have a look at four of what I believe potentially to be some of the best agents that we have access to at the moment. Um go and study them deeply, understand what they do, and see what we can learn from them in order to ourselves actually build agents in a much better way. I'm going to have a look at four specific patterns that these agents use. Uh for each of these, I'm briefly going to touch on what exactly this pattern entails, importantly what is the value that it adds to you using them, and then thirdly, show you quickly how does that actually look in real life in these agents. The first one is what I call focus modes. And focus modes is really where we put the agent in a specific mode where we constrain the action and the input space. So, we go into a planning mode or a research mode. Um what do we get from this? Well, first of all, the biggest benefit is for us as engineers, we get the ability to improve the agent's output quality on the smaller constrained action space. Um we really can potentially go and say, "Let's drop a bunch of tools. Let's really refine our system prompt. Let's optimize our e-vals to do really well on this small space first before we just do anything." Secondly, what is also really valuable actually is from a user perspective. Um one thing in these kind of do anything, ask me anything agent um UIs is the fact that the user doesn't necessarily know what to do to get the best result out of the agent, and they also have very big expectations. So, by going into a specific mode, we actually say, "Let's align a little bit the user's expectations and also tailor their inputs and behavior um specific to this mode." Cursor does this really well. So, on the right-hand side, you can see the cursor chat interface, and you can very easily switch between different modes by simply selecting a drop-down. Um and each of these modes then has specific behaviors and expectations that it sets for the user. Um it then does very specific things. So, in the middle, we see planning mode. It actually doesn't write any code. It just comes up with a plan, and it asks you questions, and you should be fine with it because that's what you signed up for. In debug mode, it has a very specific like hypothesis-driven approach towards, "Okay, what are the potential issues with your with your code? Uh let's spin up a dedicated debug server and push logs there and actually figure it out." Um so, in my opinion, a really, really powerful way in which Cursor is using modes to actually do certain things really, really well. The second pattern is transparent execution. And what we're trying to do in this instance is really trying to make what the agent is doing and using and thinking extremely clear to the users. And the crux of what we're trying to achieve here is to shift from uh delegation to collaboration. To really making the user part of the process um and not just letting the agent come up with the end result. The benefits we're getting here is first of all, trust in the output. If I give you a task and you come back with just simply the results, I will have less of trust in the results than if you were to actually share with me your process, share the thoughts you had, what did you read, what did you assume, what were the things you actually aren't certain about. Um so, we really use this process of transparency to build trust in the eventual outcome that the agent comes up with. Um additionally, it also enables the user to intervene at an earlier point in time if it sees the agent is really doing the wrong thing, and thereby reducing waste. If at step two of the agent, we saw the agent has just read from, I don't know, Notion uh docs A and B, and I shouldn't have I wouldn't have done that, then we can very easily say, "Hey, I think let's stop and take a different approach." This is something that Claude co-work for me does quite well. Um top right, it has like a progress list or a to-do list of things that it has done and will be doing, so it makes it clear what's the step that it's about to take. It gives you a good idea of the context that it's using, the skills that it's drawing from. Um in terms of cool tool calls, it's actually showing you all of the tool calls that it's making and also the inputs and the outputs of those tool calls. Um and this really makes it quite clear to the user what is actually going on from an execution perspective of the agent. Manifold does something very similar. Uh you also have your task progress where you can see the tasks completed and to be done, and it also gives a very good idea of what it actually looked at and what it made of those things. The third pattern is personalization. Um and this is really where we try and give the agent the thoughts and systems and knowledge and principles and patterns that we would have used if we were to do the task ourselves. And fundamentally, what we're trying to get here is to optimize or rather increase the speed of understanding of the agent. And this is a point that I think quite a few agents doesn't really get right in the sense that they optimize for speed to outcome, but not speed to understanding in the sense that it's very easy to just generate an output for a user, but if it's not really in line with what the user wants in terms of how they wanted it, it's going to be useless. So, optimizing for speed to understanding in the sense of really understanding all of the nuances and implicit things from the user, how it would have approached it, is really critical for agent to do the right thing and not just something. Um personalization is for us a way of enabling a quicker speed to understanding for the agent and doing the right thing and not just something. This is something we get in various flavors in different agents. Um for me too, which is quite nice, is the one is Harvey. Harvey has this idea of a playbook, and a playbook is for legal firms um typically kind of the I'm not a legal expert, but as I understand, the methods and principles that they use to, for example, uh review a certain contract. And you can create these playbooks in Harvey, and the agent would then do it in the same way as what your legal firm would have done it. >> [snorts] >> Harvey also uses fairly common concept, which is memory, so it actually creates memories as we go along and as we instruct the agent, and it can then draw from that in subsequent interactions. Um Claude, like many others, also has the idea of skills and connectors and systems that you can connect to in order to um increase this knowledge base and and improve the personalization of your agent. And the last one is then reversibility. And reversibility is really the ability for the user to be able to reverse or undo the actions that the agent has done. Um and basically, the big thing that we are achieving from this is we're binding the cost of our mistakes. So, if we know what the worst-case outcome is or at least what the downside cost could be for me, it makes the ROI calculation much easier for me to actually say, "Happy if you go and do that" versus there could be fairly big consequences. This number one then results in users being bolder and much more prone to actually taking risks and tackling higher value um tasks and use cases for the agent to actually do. This is done really, really well for me by Cursor as well. Um Cursor actually enables this reversibility on different levels of granularity. So, top left, you can actually roll back or or choose on a line level what you want to accept or reject based on what the agent did. Bottom left, you can accept on a file level. Um bottom right, you can actually go back into certain points of your conversation state, so you can say, "We've now had this conversation, but actually the last three messages, all of the changes you've done, undo those and jump back." And then also, it actually gives the ability to really do multiple outputs with the same input in parallel using different models. And thereby, the user basically is knowingly saying, "We will undo all but ideally one of our outputs um in order to actually reach something that is valuable." So, Cursor makes it really, I would say, easy for you to not have many like much downside and experiment with things and try things out knowing that you can worst case just undo and and carry on. Um Harvey also does this quite well, and they actually use So, this product, it's a Microsoft Word add-in that runs in Microsoft Word, and they actually integrate with the native Word API in order to have this um change, you could say, doing of your changes and viewing of your changes in Microsoft Word as a reviewer or editor would natively using using Word. All right. Um thanks a lot. That was I think quite a lot for a short amount of time. I hope it was useful. Please reach out if there's more questions. >> [applause] [music]
