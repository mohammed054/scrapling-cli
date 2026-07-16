# phOhGqpXss4
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-05-11 |
| **Type** | Video |
| **Duration** | 11:59 |
| **Views** | 52,415 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/channel/UCKWaEZ-_VweaEx1j62do_vQ) |
| **Subscribers** | 1,740,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=phOhGqpXss4) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Learn more about Predictive AI vs Generative AI here → https://ibm.biz/BdpPNf

Predictive AI asks what will happen, while generative AI asks what it could look like. Martin Keen  explains how LLMs, machine learning models, and diffusion systems differ in outputs, data, and real use cases. Learn how to choose the right AI approach.

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdpPNq

#generativeai #llm #predictiveai
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
| **Characters** | `8508` |
| **Error** | `none` |


Predictive AI, generative AI, sometimes people use these terms interchangeably. They shouldn't because these are fundamentally different tools that answer different questions. So predictive AI, that asks the question specifically, what will happen? What's going to happen next? It looks at historical data, and it forecasts an outcome. Is this transaction fraudulent or how many units will we sell next quarter? So predictive AI is about making predictions about specific measurable things. Generative AI, that answers a pretty different question, which is what could this look like, which is fundamentally different to what will happen. Generative AI creates new content that resembles its training data. So write me an email or help me debug this code. So unlike predictive AI, it's not mapping to a specific label or value. Instead it's producing or you know generating something that didn't exist before. Now what do these things actually output? Well, predictive AI, that gives you perhaps a number, or it gives you a category, like put this thing in the right box. It gives you a probability, something you can measure and verify, like there's a 87% chance this customer will cancel their subscription. That's something you can check on later on. It can be right or it can be wrong. Generative AI gives you content. So the content that it gives you, might be some text like some sentences or a paragraph. It could be an AI-generated image. It could a piece of code. And in many cases, there isn't a single correct answer. If we ask a generative model to write a product description, well, there are thousands of valid ways to do that. It's subjective. And what about the data that these systems consume? Well, predictive AI largely consumes structured data. This is rows and columns or database tables or sensor readings, stuff with nice, clean labels. Generative AI, well, that largely consumes unstructured data. So this is kind of the messy stuff, billions of words scraped from the internet or pixels in photos or random code snippets. Generative AI takes this kind of chaos and finds patterns in it, which it can use to generate something new. So a question for you. Where do large language models fit into this picture? Generative, right? Well, right at this very moment, there's somebody tapping away in the comments section of this video saying large language models predict the next token, so LLMs are both generative and predictive. Well, first, thank you for commenting. Please also remember to like and subscribe. And technically, yes, at the mechanism level, an LLM is a next-token prediction engine. But that's a bit like saying a gasoline-powered car is a series of controlled explosions. That's technically true, but it's not particularly useful for understanding what a car does. So another way to see the difference is if we think about predictive AI. It is usually deterministic, deterministic at inference time. You feed in the same inputs, you get the same prediction every time. Generative AI, that is probabilistic. There's randomness baked in. If you ask it the same question twice and get, you might get, well, probably two different answers. And that comes down to the temperature setting, which controls how much randomness the model uses when picking the next token. So yes, LLMs predict the next token, but, uh their purpose, well, it's primarily generative, we'll put them under generative AI. So let's get into how predictive AI actually works. Even though generative AI seems to get all the hype, it is predictive AI that quietly runs most of enterprise AI today. Now predictive AI uses statistical and machine learning models trained on historical data. And there are a few main flavors. Depending on what you're trying to predict. So, if you are trying to predict a number, that's the point of your prediction. Like, I don't know, how many units you'll sell next month, or maybe what price a house will fetch. Well, what that is, as it comes down to regression. That's where the model learns the relationship between input variables and continuous numerical output. What if you're predicting category instead? Like whether an email is spam or not spam. Well, that is classification. The output is discrete. It's this thing or it's this. And if you're predicting a value that will change over time, well if you are doing that, you are time series. So this is where perhaps we're looking stock prices or server load or electricity demand. And these models pay attention to patterns like seasonality and trends particularly when we're looking at over time. Now the specific algorithms that are actually under the hood here, well they vary. There's a whole bunch. I mean you've got things like decision trees, you've got random forests, which are essentially a bunch of decision trees voting together. You've got gradient boosting, which builds trees sequentially with each correcting the errors of the last. And then for time series, you've got classic sacks like a reamer or you've got deep learning approaches like LSTMs Yeah, good stuff. Now how and where do predictive algorithms actually get used? Well, let me give you a few example use cases. And I think the one that most people think about first of all is usually fraud detection. Every time somebody swipes their credit card, a predictive model is asking, does this transaction look suspicious? That's classification, fraud or not fraud. Then there is demand forecasting, so retailers predicting how much inventory to stock or airlines predicting hammy seats they'll fill. Another common use case is predictive maintenance. So instead of replacing a machine part on a fixed schedule, you predict when it's likely to fail and replace it right before it does. And then credit scoring is another common use case of predictive AI as well. So should we lend money to this person? What's the probability they'll default? Now let's get back to generative AI. Most generative AI today is built on a particular architecture called the transformer architecture. That's the architecture behind large language models. Now transformers use something called attention, and they use attention to let the model weigh which parts of the input matter when generating each piece of output and these transform models, they're trained on massive data sets. And they learn patterns in that data well enough to produce new content. That's the generative part. That is generally for text. For images, you have a different type of model called a diffusion model. These are interesting because they work kind of backwards, so they're trained to remove noise from images. So during training noise is gradually added to real images and then the model learns to reverse that process. So then at generation time, they start with pure noise and the model progressively denoises it into a coherent image guided by a user's prompt. So where does generative AI generally get used? What are the use cases? Well, you know, the obvious first one is content creation, marketing copy, emails, LinkedIn posts that people are pretending to write themselves. You know, that's content creation. Another very popular one is code assistance. These are models that can write, explain and debug code. There is also, conversational AI, you've probably come across these. These are like customer service bots that can hold something of a conversation regarding customer queries. And there's summarization as well, which is to say, taking long documents and distilling them down to just the good stuff. And look, so far, I've been kind of pitting these two types of AI against each other, but I think if we think about generative AI and predictive AI, we can really think that they do work kind of hand in hand. So you might use a predictive model to kind of figure out which of your customers are likely to churn and then hand that list to a generative model to write personalized retention emails for each one of these potential churning customers. So the prediction identifies the problem and the generation that crafts the response. Or, and this is becoming ever more common, you could use the generative AI to create some amount of synthetic training data and then give that to a predictive model when the real data is scarce or sensitive. So predictive AI, that says what will happen. Generative AI asks, what could this look like? And my predictive model says, you're about to give this video a thumbs up. Don't make the model wrong. It's very sensitive.
