![Thumbnail](https://i.ytimg.com/vi/WRBNDpUhsJQ/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBkvSPWkiVk7flaGfC02TdoY4LYZQ)

# On Heterogeneous Intelligence — Adrian Bertagnoli
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-25 |
| **Type** | Video |
| **Duration** | 15:13 |
| **Views** | 3,369 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=WRBNDpUhsJQ) |
| **Category** | - |
| **Language** | - |
---

## Tags

`ai` `ai engineer` `ai engineering` `software development` `tech` `startups` `software architecture` `machine learning`
---

## Description

A mixture of Qwen 3 VL8B and Kimi K2.5 beat the state of the art on Video Web Arena, outperforming the leading GPT and Gemini models by 18 and 25 percent while costing 3.7 times less and running 3 times faster. The reason it worked is that visual web navigation decomposes into subtasks that do not all need a frontier model: routing zoom and visual parsing to a smaller model alone produced 11x speed and 43x cost improvements on those steps.

Adrian Bertagnoli from Callosum makes the case that the GPU cluster era of identical hardware and monolithic models is ending. Heterogeneous intelligence treats model architectures, chip types, and workflows as variables to optimize together. A second result: running recursive long context reasoning tasks on Cerebras instead of a frontier model cuts cost by 7x and latency by 5x while matching accuracy. Callosum is building the automation layer that routes tasks to the right chip and model without bespoke decisions for each subtask.

Speaker info:
- https://www.linkedin.com/in/adrian-bertagnoli-bb3467178/

Timestamps
0:14 Introduction and definition of heterogeneous intelligence
0:56 Limitations of the current homogeneous intelligence paradigm
1:36 Evolution toward mild heterogeneity (MoE, multi-agent systems, hardware disaggregation)
3:24 The rationale for heterogeneity: complexity and multi-step problem solving
4:26 Mathematical formalization of the production function and skill distribution
5:56 Practical implementation of heterogeneous workflows
6:55 Case study: Recursive language models and context management
9:05 Results on Ulong benchmarks (Cerebras/Sambanova performance)
10:20 Case study: Visual web navigation and Video Web Arena performance
12:02 Offloading subtasks to smaller models for speed and cost efficiency
12:38 The future of compute: Moving to a heterogeneous, multi-agent stack
13:10 Partnership with the UK's Arya institute
13:31 Closing summary and outlook on hardware/software co-evolution
14:01 Q&A: Automation layer for task routing
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
| **Characters** | `11686` |
| **Error** | `none` |


Thank you for coming to my talk. My name is Adrian Bertagnoli. I'm a founding engineer at Colossyan and today I'm going to be talking about scaling the next paradigm of heterogeneous intelligence. So, I'm going to start um with explaining why we care about heterogeneity in the first place, what particular aspect make it very conducive for scaling AI, um how it is actually used in practice today, and how we can use utilize it in the future um to actually scale the next paradigm of intelligence. So, to give you an intuition about what I mean with heterogeneous intelligence, I want to take a step back and um explain the current prevailing paradigm of homogeneous uh intelligence. So, homogeneous intelligence in in terms of AI mainly refers to scaling single models on a fleet of identical chips. So, this was largely this era was largely brought about by the discovery of neural scaling laws, which showed us that more data and more parameters leads to better models. However, this is primarily rooted in a training domain and while we move towards an inference domain, this becomes less and less relevant. So, it's already changing um and we already see some level of heterogeneity in um going into our current systems. So, on the architecture level, we see that mixture of experts are replacing large dense models. On the workflow layer, we see that single LLM calls are being replaced by uh multi-agent systems. And finally, on the hardware level, single chips are being replaced by pre-fill decode disaggregated systems. So, given that we are currently at the state of mild heterogeneity, how can you imagine um a greater level of heterogeneity? How will that appear? So, initially, we'll be what we currently are experiencing is mild heterogeneity. So, everything is still running primarily on on homogeneous clusters, but we have some variety in the prompts. When we run uh multi-agent systems, we might use different LLMs for different sub-agents. Um again, we have mixture of experts. Uh when we increase the heterogeneity, we might start to use different chips um for different models. So, different LLMs might be put on different GPUs. Uh they might be interacting. We might be using different models completely. So, we have a increase of state-space models, diffusion models, all interacting with each other, all on optimal hardware that exists currently. In the last stage, uh where we really see the the heterogeneous paradigm unfolding, is when we have a co-evolution of systems uh hardware and software. So, there will be a unification where you'll have um a complete vertical integration of intelligence and hardware. So, why heterogeneity? Why is it a good thing in the first place? So, real-world problems are complex, multi-step, and open-ended. They decompose into sub-problems, which require vastly different types of intelligences. So, scaling a singular type of intelligence to solve these is very inefficient and and not optimal. So, how do we solve them? Solving these actually requires models of different architectures and sizes working together um uh acting together in long horizons, something we like to call multi-agent heterogeneous intelligence. Furthermore, new generations of silicon is coming towards the market, but currently, there's no interface which allows it to um this new hardware to be unified and and constructively um help the current compute stack. And so, this is what we aim to change. So, heterogeneia heterogeneity, the benefit is not simply a belief that we have. We actually formalize it and proved it mathematically um on the right on the left, you see a figure outlining uh the principle of maximum heterogeneity. So, these are heterogeneous agents, where the color indicates um a distribution over a skill space. Um if you take if you have a communication between these, here indicated by a ring topology, you can have a what we like to call a production function. And the production function is simply the demand uh can can be well suited for the demand of one problem, but ill suited for another problem. So, here we have a a production function that's well suited for demand A and ill suited for demand B. If you want to do this in a homogeneous fashion, you would either be able to only scale one peak or in the optimal case to match this demand function, you'd have only generalists, so as broad as possible the skill set, but then ultimately you'd have a very short cylinder that does not meet the production function readily. So, we formalize this and we um saw that across many domains, including neuroscience, economics, and ecology, these these trends hold and under any reasonable amount of constraints, heterogeneous systems outperform homogeneous ones. So, how do we use this in practice? Like, I've been telling you about the benefits of heterogeneity, but I've not told you anything about what it actually means in terms of AI. So, we optimize um multi-agent systems at three different parts of the workflow. So, all the way from the hardware, where agents run on, we choose different hardware depending on the computational demands on the agents, and then how agents interact and what workflow they construct. Um so, we have already demonstrated multiple uh benefits of of uh this type of orchestration and I want to go into a couple ones um main namely in the workflow, something a primitive we like to call heterogeneous recursion, and in the agent layer, I want to talk about multimodal multimodal video action language models. So, heterogeneous recursion. This is something um who's here heard of recursive language models? Okay. So, for those of you who um know don't know recursive language model, it's kind of a seminal paper that came out of MIT uh last October. And they basically showed that even if you only occupy a small um percentage of the context window, you still can have dramatic context rot depending on the information complexity you want uh from the prompt. So, if you're doing a needle in a haystack task, that is O of 1. The the information requirement scales is constant throughout regardless of how big the prompt is. And then you can imagine adding up the rows. You you you give uh rows and columns. Adding up the rows would be O of N, because as the prompt increases, the inform- informational requirement increases linearly. So, if the if you have a constant information requirement, it scales well. You you can occupy the full context window and actually get a a good answer. However, when you go to linear or quadratic, uh it degrades at around 60 to 30%. So, recursive language models solve this problem by actually treating the context as a um environment, rather than putting it all into the prompt. So, in practice, this looks like you present the context in a file, and then the a coding agent interacts with it programmatically through Python REPL, um basically doing keyword searches, regex, and other tricks to extract sub-context, and this sub-context is then passed off to an identical recursive agent. So, this agent then can answer the question or spawn another recursive agent. And and that's why it's called recursive uh language model. So, we simply extended this concept um instead of using a single model on a single chip, we map based on the sub-context generated towards different chips and different models to emulate the performance while drastically um being cheaper and faster. So, here are results. Um you can see this is on the Ulong benchmark. This is basically um the benchmark they used in the paper um and GPT-5 GPT-5.2 was the um most recent one when we produced this work uh sits around here, where it takes around 2,000 seconds um to run through the the benchmark and it costs around uh $3.75 for one task. Our system, when we go on Cerebras, we are seven times cheaper and five times faster. So, you save incredibly much time, are a lot cheaper, so it's basically like having your cake and eating it, too. Um with SambaNova, we even get uh further. We push the price down even further at the cost of some latency. So, we're 12 times cheaper and three times faster. So, these are like making architectural decisions that are not like simply based on the hardware. You can make huge impactful um price differences and and and while emulating the intelligence you would have from frontier models. So, the next problem we wanted to address is basically um visual web navigation. So, we used a mixture of open and closed uh video action language models. Um and we managed to beat uh the state-of-the-art of video web arena beating GPT 5.2 and Gemini uh 2.5 by 18 and 25% respectively. And not only this, the way we did it is instead of treating the problem as a homogeneous one, we we acknowledge that the problem is heterogeneous uh it itself. It it decomposes into multiple steps of visual reasoning of of textual reasoning and each of these subcomponents requires different models to be um completed successfully. So, here you see a fundamental shift of the Pareto frontier where you see singular models like Kimik A uh 2.5 and GPT 5.2 are outperformed by mixture, a heterogeneous set of of models. So, when we use Quant 3 VL8B-Instruct and Kimik A 2.5, we're 1.3 times faster than using Kimi Kimi alone. We're 18 times cheaper than using uh GPT 5.2 alone. Um and if we use uh Quant 3 um plus GPT, we're actually three times faster and 3.7 times cheaper. So, this is only benefit. There's no downside uh in in constructing this in a heterogeneous manner. So, one part of of our differentiating factor, why how we were able to beat the state-of-the-art, is that we mapped certain subtasks like zooming and and creating a different visual um reasoning for the agent, we offloaded that into less intelligent models because you don't need GPT to zoom for you. So, alone on these subtasks, we're able to be 11 times faster and 43 times cheaper than using ChatGPT. And so, this is what overall overall accumulates towards these 3.7 times cheaper and three times faster. So, looking ahead, how do we view the future of compute? The first era of scaling compute was dominated by the CPU where compute got quicker. The second era was making compute massively parallel. This is dominated by Nvidia. And the third paradigm, compute is going to become heterogeneous mapping onto multi-agentic workloads and optimally um mapping these workloads onto different chips. We are actually um working with Aria, the UK Institute. Um we got a 3 million grant for the first for operating the first heterogeneous collocated cluster in the UK. So, we really want to make a difference and and spearhead this new era of innovation. So, the era of homogeneous scaled delivered extraordinary progress. We should be grateful for it. What comes next is heterogeneous intelligence where models, workflows, and silicon co-evolve and every new source of diversity makes the whole system smarter, faster, and cheaper. This is the worst our infrastructure will ever be. Thank you. How do you define which task to run on the faster uh cheaper model? Like for instance, is zooming that something that's hardcoded like oh, if you have to zoom, use this model or if you have like the smarter model, use that type of model? So, it is um initially we started doing bespoke decisions on mapping uh certain simple subtasks to simple models, but since then, we have um created an automation layer that detects the task complexity and automatically predicts the best model uh the best suited model and hardware. Any other questions? Great. Thank you so much for your attention. My name is Adrian Berczynski and if anyone is interested, uh we are hiring, so yeah. Great. Thank you very much.
