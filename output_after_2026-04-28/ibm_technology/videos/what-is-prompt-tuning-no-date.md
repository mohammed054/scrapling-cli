![Thumbnail](https://i.ytimg.com/vi/yu27PWzJI_Y/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBCiBnZj7Z6vmVHSqyGdg2Oiup8jQ)

# What is Prompt Tuning?
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2y ago |
| **Type** | Video |
| **Duration** | 8:33 |
| **Views** | 304,574 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=yu27PWzJI_Y) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud` `LLM` `Large Language Models` `AI` `Artificial Intelligence` `Prompt Tuning` `Prompt Engineering`
---

## Description

Explore watsonx → https://ibm.biz/BdvxRp

Prompt tuning is an efficient, low-cost way of adapting an AI foundation model to new downstream tasks without retraining the model and updating its weights.  In this video, Martin Keen discusses three options for tailoring a pre-trained LLM for specialization, including: fine tuning, prompt engineering, and prompt tuning ... and contemplates a future career as a prompt engineer.

Get started for free on IBM Cloud → https://ibm.biz/sign-up-now
Subscribe to see more videos like this in the future → http://ibm.biz/subscribe-now

#ai #watsonx #llm
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
| **Language** | `en-US` |
| **Characters** | `6682` |
| **Error** | `none` |


Large language models like ChatGPT are examples of foundation models, large reusable models that have been trained on vast amounts of knowledge on the Internet, and they're super flexible. The same large language model can analyze a legal document or write a poem about my soccer team. But what if we want to improve the performance of pre-trained LLMs, or Large Language Models, to address a specialized task? Well, until recently, the best way to do that was using a method that is known as "fine tuning". Now with fine tuning, you gather and label examples of the target task. Lots and lots of examples, and you fine tune your model rather than train an entirely new one from scratch. But there's a simpler, far more energy efficient technique that has emerged in place of fine tuning, and that is known as "prompt tuning". So what is prompt tuning? Well, prompt tuning allows a company with limited data to tailor a massive model to a very narrow task. And there's no need for gathering thousands of labeled examples like we have to do with fine tuning. In prompt tuning the best cues, or front end prompts, are fed to your AI model to give it task-specific context. The prompts can be extra words introduced by a human or more commonly, an AI generated number introduced into the model's embedding layer to guide the model towards a desired decision or prediction. Now, if all this sounds a little bit familiar using prompts to guide the output of an LLM, that's because it most certainly is. That is an example of something else called "prompt engineering". Now, prompt engineering is the task of developing prompts that guided LLM to perform specialized tasks. Honestly, it sounds like a lot of fun. I think I'd quite like to be a prompt engineer one day. So if I want my LLM to specialize as an English to French language translator, I might engineer a prompt to do so. So my prompt might start with, let's say, translate. And we want to translate English to French. That's the task description of my prompt. Then I'm going to add some few short examples. So let's let's add those now. So here's the English word "bread" into the French word "pain". That's one short example. Let's add another, "butter". We're going to turn that into "beurre". And then the next part of my prompt, I'm going to add to what that I wanted to translate next. So, "cheese". And that's it. Now prompts like this written by a human, me, Mr. Want-to-be-prompt-engineer himself, they prime the model to retrieve the appropriate response from the LLM's vast memory. In this case, specifically for other words in French. And the model's output is its prediction. What is this model going to output? "Fromage", that worked! We used prompt engineering to train a model to perform a specialized task with just a single prompt introduced to inference time without needing the model to be retrained. But if the task is more complex than this, it may require dozens of these prompts. And so these hand-crafted prompts have begun to be replaced by AI designated prompts known as "soft prompts". Now, soft prompts have been shown to outperform human engineered prompts, which we can know now as "hard prompts". These were hard coded by a human. This is not good news for my prompt engineering career because, you see, unlike hard problems, AI designed soft prompts, they're used in prompt tuning and they are unrecognizable to the human eye. Each prompt consists of an embedding or strings of numbers that distill knowledge from the larger model. And these soft prompts can be high level or task specific and act as a substitute for additional training data and are incredibly effective in guiding the model towards the desired output. But do keep in mind that one drawback of prompt tuning and soft prompts in general is its lack of interpretability. That means that the AI discovers prompts optimized for a given task, but it often can't explain why it chose those embeddings. Like deep learning models themselves, soft prompts are opaque. All right, so let's consider we have here a pre-trained model. So this might be a large language model or something like that. Okay, now let's consider three options for tailoring this pre-trained model for specialization. I'm going to talk about the three that we've covered here. So first of all, fine tuning. Fine tuning. So with fine tuning, we take this pre-trained model and we supplement it. We supplement it specifically with tunable examples. These are the thousands of examples that I talked about right at the beginning. Once we've done that, we can then provide input data into the model and it should now be able to perform a specialization. So that's fine tuning. What about prompt engineering? How is that different? But with prompt engineering, we take the model as it is, we haven't tuned it, and then we add in an additional prompt. So we have our input prompt. But we also add in to that input prompt, an engineered prompt which sits in front of it. So we effectively provide two prompts here for the specialization. That's what we did with our language translator. So we provided this prewritten engineered prompts, and then we provided our input, which was cheese. So that's prompt engineering. What about prompt tuning? How is that different? Well, with prompt tuning, again we use the pre-trained model as it is, and we again provide an input. But we also provide something in front of that input. And that is the tunable soft prompt that is generated by the AI itself. And it's the combination of these two things that allow us to use the model in a specialized way. Prompt tuning is proving to be a game changer in a variety of areas. For instance, in multitask learning where models need to quickly switch between tasks, researchers are finding ways to create universal prompts that can be easily recycled. Techniques like multitask prompt tuning allow the model to be adapted swiftly and for a fraction of the cost of retraining. Prompt tuning is also showing promise in the field of continual learning, where AI models need to learn new tasks and concepts without forgetting the old ones. Essentially, prompt tuning allows you to adapt your model to specialized tasks faster than fine tuning and prompt engineering, making it easier to find and fix problems. My career as a prompt engineer might be over before it started. So I guess it's back to the drawing board, or rather back to the embedding layer, because in the world a string of numbers is worth a thousand words. If you have any questions, please drop us a line below. And if you want to see more videos like this in the future, please "like" and subscribe. Thanks for watching.
