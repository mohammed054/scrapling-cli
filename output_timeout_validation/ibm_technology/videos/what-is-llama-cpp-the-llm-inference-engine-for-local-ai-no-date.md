![Thumbnail](https://i.ytimg.com/vi/P8m5eHAyrFM/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBXjApMaioWjK5IgX8imBx7qUp5mg)

# What Is Llama.cpp? The LLM Inference Engine for Local AI
---

## Info

| Field | Value |
|-------|-------|
| **Date** | Unknown |
| **Type** | Video |
| **Duration** | 9:14 |
| **Views** | 130,780 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 0 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=P8m5eHAyrFM) |
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
| **Characters** | `8771` |
| **Error** | `none` |


Have you ever wondered how to run a large language model on a small machine like a laptop or a Raspberry Pi? I'm talking about AI that has no subscription cost, AI that no usage limits, and you also get full control of your data. Well, my friend, stick around because I want to introduce you to a project that's called Llama C++ and show you how you can run your own local AI models with complete privacy, data control, and benefit from all of this. Let's get started. So if you think about most large language models, well, they're designed to run in huge data centers that are both expensive and power-hungry. But let's walk through this. Say, for example, that we're making a request to our model and we're gonna say something like, hey, based on these documents, I want you to answer this specific question. And we're going to add in our document sources here that might be PDFs, they might be different types of spreadsheets and file types using a method that's known as retrieval augmented generation or RAG. Which takes our original question, right, and adds in some context from those documents into the context window of the model. So this is the context right here. And it might not just be documents, right? It might be data sources, like a database or something. So we can connect those various data sources using a standard that's called model context protocol. So this going to fetch out to our different CRMs and sources in order to bring that information into the context window, just like how we do with retrieval augmented generation. Then from here, as we've got all this information into one prompt, we're going to pass that along to our large language model. So here he is over here, and this is our LLM that's running, but the thing is, whether we're using RAG or just asking questions, doing vibe coding, using model context protocol in order to do perhaps agentic functionality, so we have our agent right here doing some reasoning back and forth with the data. Well, no matter what we're using at the end of the day or doing to the prompt to get our response back, it's always going to go to an LLM endpoint. So by default, a lot of developers kind of start off using some type of proprietary model, maybe it's an API, and it's really easy to send that request to some type of server, as I mentioned before, that's running in the cloud. The trick is that can get pretty expensive very fast because you're being charged by how many tokens you use. And the more information that you're putting in your prompt as your prompt gets bigger, the more that's going to cost you and your organization. And at the same time, well, if you have secure and private data that's being sent, well, it's also a concern for governance and compliance there. So what's happening now, and because of this situation, well, a lot of developers are starting to look towards running their own large language models on their own device. Because you don't have to worry about cost, because you already have that hardware, or the data leaving your premise. And that's the idea behind Llama C++ is to be able to run these local large language models on your own hardware, not have to worry about sending things to the cloud here, because we already have our own machine that has capabilities to run at these models locally. And so what we can do is we can take this entire kind of AI application that we're already have set up, and we can start to send those requests to a local model. And if you've ever heard of Ollama or Jan or GPT4All, all of these tools are using Llama C++ under the hood to run those LLMs. But how does that happen? Well, we're gonna talk about a few optimizations that Llama C++ does in order to run them on small amounts of hardware. So how does Llama C++ work? Well, let's start with the model itself. So I want you to think of open models that you've heard of, for example, DeepSeek perhaps, or maybe you've heard of the Llama family of models, or maybe Qwen, perhaps, and many, many more that all come from typically one place, like Hugging Face or other repositories that have open-source models you can use. Now, what Llama C++ does is it uses a specific format called GGUF. So it takes the model weights, and here we have the weights, and it also puts together the metadata, all together in one place, and stores it as this GGUF file, so GGUF. And this makes it really easy to do quick loading and swapping of models. So, say for example, I'm starting off with DeepSeek, but I need, say, for example, Qwen in order to do some retrieval augmented generation tasks, or maybe the Llama family of models to do something. This allows me to easily swap and switch because this is all together in one format. Now when models are released, they're typically released at a format or precision that's known as 32-bit or 16-bit. So let's say this is 16-bit, and we've got a high accuracy for this model. But the thing is, at the same time, this requires a large amount of RAM in order to store this and run this model. So the idea with Llama C++ and these GGUF formats is that you can shrink the model down to a lower precision. So, instead of 16- bits, we're going to store this as 4-bits. So we still have pretty similar capabilities and maybe a high degree of accuracy still, but instead of needing that huge amount of RAM, we only need, in this case, 25% of the hardware capabilities to run this model. So what's great is that we can use less hardware and we can run these models on smaller machines because of this model quantization, and that's what this process is called— going from high precision to low precision when we store the weights. So, for example, you might see situations for these open models where they're released as, for example, DeepSeek, and they're named in this format as well. So it would be something similar to quantize, Q for quantize, and then at 4-bit precision. And then we're also going to refer to a specific compression algorithm and type. So we're going to do underscore K and M. And I won't get too into the depths here, but this is just the variant that's tuned for quality that you'll typically see when you're searching open-source models online. And that refers to the model compression that's being used in order to save perhaps 75% on hardware usage and capabilities needed to run the model, but also giving you much higher throughput when you are actually running this for various tasks. Speaking of speed, I wanna talk a little bit about Llama C++'s optimized kernels for nearly every platform. So maybe you're using Mac, so there's support for Metal there, or you have an NVIDIA GPU, so accessibility for CUDA. Maybe you have a AMD card, so there is ROCm here, also Vulkan. And the thing is, whatever you're running, you have support for all types of models on all types of hardware. Of course, also including CPU. So that's the beauty of it is that you can swap out different models, compress them, and use them in an optimized way. So, what does this look like in action? Well, as an engineer, as a developer, if you're just tinkering around, you can try out and use Llama C++ either through the terminal using the Llama CLI. So the Llama CLI allows you to call in a specific model—and so this will be model.gguf— and run that and chat with that using your own terminal or CLI. But for a lot of use cases, you're going to want an open AI-compatible local server. So in order to do this, we would run the command Llama server, point to the model, and we would type in the model here, but also we would do a port assignment. So port 8080. And on that port, we will be able to send Git and POST requests, be able to connect different extensions. And maybe you're using something like LangChain or LangGraph, where you have the same compatibility between remote servers, but also local model servers that you might be running as well. Now, there's also additional capabilities with Llama C++, specifically for capabilities like being able to work with images, be able to describe what's happening in there as well, or as I mentioned before, the connection between different services that your AI models might want to use using model context protocol. That allows you to bring in databases, your CRM, you name it. So, thanks to the open-source community, AI is becoming more accessible than ever, from models to compression to kernels and support for developers who want to run their own local AI models, knowing that their data stays on their device and there's no rate limits or API outages. Thanks so much for watching. If you learned something today, please be sure to drop a like and hack the algorithm. Also, stay subscribed for more content on AI and open-source technology. Thanks and have a great day.
