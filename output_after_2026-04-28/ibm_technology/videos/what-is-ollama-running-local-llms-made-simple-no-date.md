![Thumbnail](https://i.ytimg.com/vi/5RIOQuHOihY/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAGn3RFZ2r8PznS1USHcBzovhClYA)

# What is Ollama? Running Local LLMs Made Simple
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 7:13 |
| **Views** | 270,449 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=5RIOQuHOihY&pp=0gcJCQ0LAYcqIYzv) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx AI Assistant Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/Bdnd3d

Learn more about Large Language Models (LLMs) here → https://ibm.biz/Bdnd3x

What if you could run large language models locally with just one command? 🚀 Cedric Clyburn shows how Ollama, an open-source tool, simplifies deploying LLMs on your machine. 💡 Protect your data, save costs, and explore powerful AI solutions—all from your own system. ✨

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/Bdnd3D

#ollama #opensourceai #llm
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
| **Characters** | `6826` |
| **Error** | `none` |


By now, you've probably tried out some really helpful AI models to summarize your data, to act as a pair programmer, and much more. But traditionally, this meant using cloud services. Perhaps you were using an LLM through some type of chatbot, or for me, an API that was hosted on a cloud service. But at the end of the day, I was using someone else's cloud computing resources. Now, what if I told you, though, that there's open source way. to run AI models and LLMs locally from your own machine. And that allows you to save on cost for your AI bills, to keep your data private and as a developer to build out applications and features that use AI from your on machine. Now that's right, today we're gonna be taking a look at Ollama to run large language models or LLMs from your old machine. Now, this is really, really cool because you're able to take a model which might be quantized or compressed and run it from your own system resources and integrate with a huge ecosystem of models from Llama to Mistral and beyond. And for organizations that are looking to use AI in their applications, it can be very helpful because we're able take and deploy a small or large language model locally and ensure that customer data doesn't leave the secure environment at all. And this is all using a simple command that we're going to take a look at here in a second. But how does it work and what should you know about using Ollama? Well let's begin with the Ollamas CLI. Now whether you're on Windows, Mac or Linux, you can head over to ollama.com in order to download the CLI or command line interface for your machine. Now this allows you to download models, to run them, and to interact with them all from your own terminal. While in the past you had to go over to repositories such as Hugging Face in order to download model weights, and you had work with complicated setup in order to get the model ready to be inferenced and chatted with, this is all simplified with Ollama through a single command, Ollamarrun. After that, we'll pass in the argument or parameter of the model name. It could be granite, could be llama, could be deep seek, and that'll kick off the process. to download one of the Ollamas own models, their compressed and optimized models to your machine, and start up an inference server, similar to how you would start up a web server and serve your web pages. This will drop you into a GPT looking chat window, and you can almost think of the ollama run command as a package manager for AI, allowing you to run and manage models with a single command. Now, that's awesome, but speaking of models, Thanks for watching! Ollama has a catalog of standardized and customizable language, multi-model embedding and tool calling models. Now, I just said a lot of things, but let's break it down here. The first one that I wanted to mention is a type of model for language. So for example, that means working with your text and data, either in a conversational or base type of format or an instructional format for answering questions and answers. Now, the second type is multi-modal models. So for example. working with images and being able to analyze, hey, what's going on in this specific frame? Now, the next one is a type of model called embedding, which is essentially taking our data from PDFs and other types of data formats and preparing it to be used in a vector database to do question and answering on our own unique data. And then finally, the last type of model that you can use is tool calling. So, it's a fine-tuned version of a language model. that is familiar with calling different functions, APIs, and services in an agentic way. Now, these are some of the types of models, but how would you pick the right model for your use case? Well, it's a good question, and it depends on your project's requirements. But some of popular models that we see being used a lot in the community are, for example, llamas series of models. Different open and fine-tuned models for various use cases that provide support for different languages. as well as IBM's Granite model. So, the Granite Model is a enterprise ready LLM that can be used with RAG or agentic functionality. And we also see these types of reasoning models that are being more and more popular that essentially provide chain of thought or thinking capabilities to answer your questions. Now, beyond just using the Model Catalog, you can actually take advantage of what's known as the Ollama model file to essentially just how Docker has abstracted the complexities of containers. Well, we're using a model file to abstract the complexities models to be able to import from Hugging Face, for example, or to start from a model that you already have and customize it with system prompts and different parameters to be the best model for your use cases. But no matter what type of model that you want to use, your request at the end of the day will be passed through the Ollama server, which is running on localhost on port 11434. So for example, let's say you're making a request or prompt to the model from your CLI, from your terminal with Ollama. Well, this is actually being passed to the Ollama model server, and in a similar way for applications that might want to use models, for example with Langchain or another framework, you're make a post request to the model that's running on local host. on this specific port, which is a REST server. So it has endpoints, and we can make that request similar to how we would make a request to any other service that's running on our machine. And right here is the simplicity of Ollama for developers. It lifts the weight of having to run the model in your application, and it abstracts the model as an API. So you make that requests, and you get that response back all locally on your machine. Or let's say you want to run Ollama on another machine and you just SSH there, or you make that request remotely. No matter what you do though, Ollama is doing the heavy lifting of running the model. And you can even connect other interfaces, such as Open Web UI, in order to set up a simple RAG pipeline and use your PDFs or other documents to be passed with the context of that information to Ollama and get that response back. But that is the Ollama server. Now. Whether you want to save on cloud costs when you're using AI models, or have private sensitive data that can't leave your premise, or even limited internet access in an IoT device, you can use Ollama and the power of open source AI to use and manage LLMs from your local machine. Now, it isn't the only tool for doing this, but as a developer, it's made my life much easier, and I encourage you to check it out. As always, thank you so much for joining us today. Make sure to like the video if you learned something. and have a good one!
