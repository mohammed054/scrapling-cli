![Thumbnail](https://i.ytimg.com/vi/uxE8FFiu_UQ/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBgQX8YmxLCpfEAUH9n_csh3J0Tjw)

# Run AI Models Locally with Ollama: Fast & Simple Deployment
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 5:59 |
| **Views** | 57,384 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=uxE8FFiu_UQ) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Curious about running AI models locally with Ollama? Check out the code here → https://ibm.biz/BdndQU

Ready to become a certified watsonx AI Assistant Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdndQ8

Learn more about Large Language Models here → https://ibm.biz/BdndQg

See how to build AI-powered tools that run locally with Ollama. 🚀 Cedric Clyburn demonstrates how to maintain data privacy, integrate Langchain, and simplify development using local AI deployment. 💡 Discover how to prototype smarter and optimize tools for enterprise tasks with ease. ✨"

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdndQh

#ollama #llm #aiintegration
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
| **Characters** | `6062` |
| **Error** | `none` |


Hey, quick question. Did you know that you can run the latest large language models locally on your laptop? This means you don't have any dependencies on cloud services and you get full data privacy while using optimized models to chat, uses code assistance and integrate AI into your applications with RAG or even agentic behavior. So today we're taking a look at Ollama. It's a developer tool that has been quickly growing in popularity and we're gonna show you how you can start using it on your machine right now, but real quick, before we start installing things, what value does this open source project provide to you? Well, as a developer, traditionally I'd need to request computing resources or hardware to run something as intensive as a large language model. And to use cloud services involves sending my data to somebody else, which might not always be feasible. So by running models from my local machine, I can maintain full control over my AI and use a model through an API, just like I would with another service, like a database on my own system. Let's see this in action by switching over to my laptop and heading to ollama.com, and this is where you can install the command line tool for Mac, Windows, and of course, Linux, but also browse the repository of models. For example, foundation models from the leading AI labs, but also more fine tuned or task specific models such as code assistants. Which one should you use? Well, we'll take a look at that soon, but for now, I'll open up my terminal where Ollama has been installed, and the first step is downloading and chatting with a model locally. So now I have Ollama set up on my local machine. And what we're going to do first is use the Ollama run command, which is almost two commands in one. What's going to happen is it's going to pull the model from Olamma's model store, if we don't already have it, and also start up an inference server for us to make requests to the LLM that's running on our own machine. So let's go ahead and do that now. We're going to run Ollama run granite 3.1 dense, and so while we have a chat interface here where we could ask questions, behind the scenes, what we've done is downloaded a quantized or compressed version of a model that's capable of running on limited hardware, and we're also using a back end like llama C++ to run the model. So every time that we ask and chat with the model, for example, asking vim or emacs, What's happening is we're getting our response, but we're also making a post request to the API that's running on localhost. Pretty cool, right? So for our example, I ran the granite 3.1 model and as a developer, it has a lot of features that are quite interesting to me. So it supports 11 different languages so it could translate between Spanish and English and back and forth, and it's also optimized for enterprise specific tasks. This includes high benchmarks on RAG capabilities, which RAG allows us to use our unique data with the LLM by providing it in the context window of our queries, but also capabilities for agentic behavior and much more, but as always, it's good to keep your options open. The Ollama model catalog is quite impressive with models for embedding, vision, tools, and many more, but you could also import your own fine-tuned models, for example, or use them from Hugging Face by using what's known as the Ollama model file. So we've installed Olamma, we've chatted with the model running locally, and we've explored the model ecosystem, but there's a big question left, what about integrating an LLM like this into our existing application? So let me hop out of the chat window and let's make sure that the model is running locally on our system. So Ollama PS can show us the running models, and now that we have a model running on localhost, our application needs a way to communicate with this model in a standardized format. That's where we're going to be using what's known as Langchain and specifically Langchain for Java in our application, which is a framework that's grown in popularity and allows us to use a standardized API to make calls to the model from our application that's written in Java. Now, we're going to be using Quarkus, which is a Kubernetes optimized Java flavor that supports this Langchain for J extension in order to call our model from the application. Let's get started. So let's take a look at the application that we're currently working on. So I'll open it up here in the browser. Now, what's happening is that this fictitious organization Parasol is being overwhelmed by new insurance claims and could use the help of an AI, like a large language model, to help process this overwhelming amount of information and make better and quicker decisions, but how do we do that behind the scenes? So here in our project, we've added Lang chain for J as a dependency, and we're going to specify the URL as localhost on port 11434 in our application.properties, pointing to where our model is running on our machine. Now we're also gonna be using a web socket in order to make a post request to the model, and now our agents have AI capabilities, specifically a helpful assistant that can work with them to complete their job tasks. So let's ask the model to summarize the claim details. And there we go. In the form of tokens, we've made that request to the model. running with Ollama on our local machine and we're able to quickly prototype from our laptop. It's just as simple as that. So running AI locally can be really handy when it comes to prototyping, proof of concepts and much more, and another common use case is code assistance, connecting a locally running model to your IDE instead of using paid services. When it comes to production, however, you might need more advanced capabilities, but for getting started today, Ollama is a great pick for developers. So what are you working on or interested in? Let us know in the comments below, but thanks as always for watching and don't forget to like the video if you learned something today. Have a good one.
