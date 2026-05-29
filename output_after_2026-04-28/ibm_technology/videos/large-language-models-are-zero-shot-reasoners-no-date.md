![Thumbnail](https://i.ytimg.com/vi/T-w_5T-j-dA/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLARhFFEOXpd68391bouuUopsVnkMQ)

# Large Language Models Are Zero Shot Reasoners
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2y ago |
| **Type** | Video |
| **Duration** | 7:46 |
| **Views** | 49,533 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=T-w_5T-j-dA) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Explore AI built for business: watsonx → https://ibm.biz/meet-watsonx 

When you create a prompt for a large language model, are the answers sometimes wrong or just plain weird? It may be you! Or more accurately, the way you are formulating your question. In the video, Martin Keen explains why LLMs are led astray and offers suggestions on prompting techniques to reduce these mishaps.

Get started for free on IBM Cloud → https://ibm.biz/buildonibmcloud
Subscribe to see more videos like this in the future → http://ibm.biz/subscribe-now

#llm #ai #watsonx
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
| **Characters** | `6504` |
| **Error** | `none` |


If you're not getting the responses you want from LLMs, or "Large Language Models", like the model that powers chatGPT, I may know what's wrong. It might be you. No, no, no. Hear me out. Look, you see, the way that we prompt these large language models is very important. So prompting plays a significant impact in the quality of the response that the LLM will generate. Let's take a look at an example. I'm working on a homework assignment for my Econ 101 class, and I need some help. So, I issue the following prompt to a large language model. Question: "explain the different types of banks." The LLM responds with this, "Banks along a river can take various forms depending on whether they are natural or artificial". Whoa ho, hang on there! Here I am trying to understand the difference between a credit union and an investment institution and it's talking to me about river banks! This is an example of a particular type of prompt, and that is called "zero-shot" prompting. You're providing the model with a single question or instruction without any additional context, examples, or guidance. The model is expected to understand and answer the prompt without that context, and to do so, it relies solely on its preexisting knowledge and its ability to generalize from that knowledge to generate a relevant and accurate response. And as you can see, it can lead to some suboptimal responses. Now, "bank" is a homograph. It has multiple meanings. One method to clear that ambiguity up is to employ a different type of prompting called "few-shot" prompting. Now, here is an example of few-shot prompting. So, we've got a question: "what is the primary function of a bank?" Answer: "A bank's primary function is to accept deposits, provide loans and offer other financial services to individuals and businesses." Question: "explain the different types of bank." With few-shot prompting, the model is provided with one or more examples to help guide its understanding of the task at hand. By providing an example related to financial institutions, the LLM is more likely to understand that you are asking about types of bank in the context of finance... ...rather than the stream at the bottom of your garden. Now, in this example, we could probably just have used a better zero-shot prompt. Like, "explain the different types of banking financial institutions." That probably would have worked. But few-shot prompting has other advantages too. It can help an LLM understand the expected format a response should take. Like this, so we've got question: "create a title from my web page, then a title tag with all of our banks". Then, question: "create a heading for my article." Then we have an H1 title pair with types of banks in those tags, and then we say, "question: list the types of banks." And here the LLM may derive "we are looking for answers in HTML notation" and respond accordingly like this. Now there's another way that few-shot prompting can help, and that is to aid reasoning. So let's take an example from the paper, "Large Language Models Are Zero-Shot Reasoners" which was written by the University of Tokyo and Google Research. And they issued this zero-shot prompt to a large language model. Question: "a juggler can juggle 16 balls. Half of the balls are golf balls, and half of the golf balls are blue. How many blue golf balls are there?" The answer is... now, can you figure this out? It's not too tricky, but it was for the LLM. "8" Wrong! So next in the paper they tried a few-shot prompt. So we start off with a sample question and a sample completion. So, question: "Roger has five tennis balls. He buys two more cans of tennis balls. Each can has three tennis balls. How many tennis balls does he have now?". Answer: the answer is 11. Question: "a juggler can juggle 16 balls..." and so forth. Now we've shown the model of what a right answer looks like by applying addition and multiplication to a sentence. So, did the a few-shot prompt get us the right answer? Eight, again! No! But by making a slight change, we can improve the reasoning of the LLM and get the right answer. And we can apply that change to either few-shot prompts, or to zero-shot prompts. So, what is this mysterious addition? Well, it's called "chain of thought", or CoT, and to invoke it, just add wording such as, "let's think step by step." Effectively, we've asked the LLM to document its thinking. We're asking to see its chain of thought. And here's what we get. So the LLM responds to us with, "there are 16 balls in total. Half of the balls are golf balls. That means there are eight golf balls. Half of the golf balls are blue. That means there are four golf balls." Four golf balls! That is the right answer! Now, this particular test was applied to the InstructGPT model, which is a couple of years old. Newer models like GPT-4 can invoke mathematical reasoning without the "let's think" step-by-step chain-of-thought prompting. But chain-of-thought prompting remains a valuable tool in prompt engineering for a number of reasons. Reason number one is it encourages the model to provide a more detailed, and specifically, a more transparent response. And an explanation of that response and its reasoning process. And this helps users better understand how the model arrived at a particular answer, making it easier for them to evaluate the correctness and relevance of the response. And that's all an important part of XAI, or "Explainable AI". And then reason number two for chain-of-thought prompting is that it can be used to improve the quality of a model's response by encouraging it to consider alternative perspectives. Or different approaches. And by asking the model to think through various possibilities, it can generate more well-rounded and comprehensive answers, which can be particularly valuable when dealing with open-ended or subjective questions. Look ultimately few-shot prompting and chain-of-thought prompting are powerful techniques that can be employed to improve the quality of responses generated by large language models. By providing the model with additional context, examples or guidance, users can help the model better understand the task at hand and generate more accurate, relevant and well-reasoned responses. And not to mention, keep better track of how many golf balls we're juggling. If you have any questions, please drop us a line below. And if you want to see more videos like this in the future, please like and subscribe. Thanks for watching.
