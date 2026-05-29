![Thumbnail](https://i.ytimg.com/vi/6l0x4qvrnqI/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBvKM9ALH73UeoOaO8NHTRGMHlFog)

# Can LLMs Learn Without Losing Their Minds? Exploring Generative AI!
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 6:42 |
| **Views** | 8,295 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=6l0x4qvrnqI) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx AI Assistant Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdnBi9

Learn more about Generative AI here → https://ibm.biz/BdnBiC

🐶 Can AI help you draw better dogs or swim like a pro? Aaron Baughman explains how LLMs evolve through self-learning, chain of thought reasoning, and machine unlearning. Learn how these models develop new skills while staying accurate, reliable, and aligned with user needs. 🤖✨

 AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdnBiQ

#llm #generativeai #selflearning
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
| **Characters** | `6702` |
| **Error** | `none` |


Generative AI algorithms, they're rapidly learning new domains. But as they do so, the big question is, are they going to lose their minds? Now, say for instance, I have a friend, Ravi. He has a swim meet coming up and he wants to use a large language model to get hints on how to better his butterfly. But perhaps these hints aren't the best. And then I have another friend named Kevin who's working on a dog artwork. And he wants a different style transferred into that piece. And he wants to use a generative AI system to help him out. Now both of these are really good ideas and use cases where we can use generative AI to help us out in our daily lives, but we need to make sure as we do this that they don't lose their minds. Well there's a lot of similarity between the human brain and large language models. Now both of them, they have these neurons that are deeply connected together. So in the brain, you have the prefrontal cortex and that's responsible for the different types of thinking that we have. Now over in LLMs, Within feed-forward neural networks, you have these densely packed regions that can propagate forward and infer an output. Now, the other part is called memory. So within the human brain, we have what's called the hippocampus. This is where we store our memories and we have to retrieve information in order to respond to our environment. Now, LLMs are kind of similar because they use what's called a vector database. So we can write vectors into it and then pull it out. Now the third aspect that are very similar between the two. or is what we call specialized regions, right? And we could think about this within the domain of generative AI as a mixture of experts. Now within the brain, we can also look at the cerebellum, a nd the cerebellum helps us with balance and movement and such, but each of these specialized areas have a certain function that can help us out. So I told you how they're all similar, but now, how is the brain different? Okay, so some of the differences here. is power, right? So the human brain, it only needs 0.3 kilowatt hours of power. Now an LLM, it needs thousands of kilowatt hours in particular to train it. And now the other difference between the two is also volume. Now the human brain takes up only 1200 cubic centimeters. And then when I compare that just to the cables alone to put these supercomputers and clusters that have GPUs together, right, the generative AI part could have miles of cables. Now the other biggest difference is the way in which each of them pass messages, right? So there's a complex series of messages. So one of them is chemical, the other is binary. So within the brain, we have this complex stew of neurotransmitters that relay messages back and forth, whereas in generative AI, we have encoded floating points that use ones in zeros to pass that said information back and forth. Now, say my friend Kevin, he's learning how to draw the better dogs. Well, we still need to take some of the similarities and the differences and train these LLMs to help him draw better dogs. Okay, why don't we jump into it? So at the foundational level, we can begin this phased training approach. Now, this training approach is broken down into two different components. The first one being unsupervised learning, where you don't provide any labels at all, but the model learns how to represent the data. And the second component of this is supervised learning. This is where you do provide the answer, and then it can back propagate the error in between the output and the answer so you change the gradients. Now the second area that I wanted to mention is called chain of thought. This is a step-by-step logical reasoning that can be used to even teach other models. And this also provides transparency so that we can understand what's happening. Now what you're seeing in the field that's beginning to emerge, it's called self-learning. Now the self learning aspect, this is where we can use a lot of these chain of thoughts and nest them together and have a mixture of experts learn them. So they become experts in their own little area, right? And what you can do is have each of those experts in the MoE vote, and the more votes you have for a particular answer, that is going to be the right answer, and that can be your quasi or meta ground truth that you then can send back right into the network so it learns. Now this helps the models to branch off and learn even new skills, it can learn new capabilities, and you'll even begin to see reinforcement learning that's being used within the field as well. Now you might be thinking that some of these models are losing their mind. Well, they're really not. So as these models begin to teach themselves, we really need to be careful that they do produce good results. Now, we try to use what's called a funnel of trust, and we can use this funnel to help minimize the hallucinations or incorrect skills that might be acquired through these three examples that I provided. Now, one of these areas that I would like to highlight is called a large language model as a judge. Now, this is where a model itself, it interprets the output of another model, and if we want to follow what's called a condorcet jury theorem, we can stack together lots of these judge models together to create a jury, right, and say if all of these jury members are more than half likelihood to get it right and you keep adding more and more and more, then your judge jury is gonna be more than likely correct as well. Now the other area is called theory of mind. And what we wanna do here is ensure that the output of these models, they match your expectations so that the models understand, wait a minute, my user or my agent that's trying to use me, they have their own expectations, and so we want to be able to meet these agent mental models or user mental models so that they begin to have an alignment of their output. Now the other area is called machine unlearning. With machine unlearning, we can begin to remove data in a systematic way. So we can have this where we can create virtual lesions within a MOE where one of the experts forgets the data that they were taught, right? This is called selective forgetting. And this is very powerful in MOEs, or even during retraining, we can shard the data and split it so that we don't want to train a certain skill anymore. Now you might think that all this is pretty interesting and it can help my friend Kevin draw better dogs or can help Ravi begin to understand how to get a different style of swimming for the upcoming meet that they might have, but as we do this, we can begin to help LLMs learn without losing their mind.
