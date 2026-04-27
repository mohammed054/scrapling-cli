![Thumbnail](https://i.ytimg.com/vi/81FbpXpfxTc/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCN7SA8geIFGn4uiuOsPYcr4TxLow)

# AI Models as a Service: Powering Agentic AI, Privacy, & RAG
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-03-29 |
| **Type** | Video |
| **Duration** | 10:31 |
| **Views** | 30,631 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,670,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=81FbpXpfxTc) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx AI Assistant Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/Bdpiku

Learn more about AI As A Service here → https://ibm.biz/BdpikL

What if you could control AI like your own private cloud? 🤯 Cedric Clyburn explains how AI Models-as-a-Service simplifies deployment, supports agentic AI, and enables RAG workflows, all while ensuring privacy and governance. Learn how to scale secure, effective AI in hybrid and private environments!

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdpikC

#aimodels #agenticai #retrievalaugmentedgeneration
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
| **Characters** | `9889` |
| **Error** | `none` |


As an engineer, I've been using different forms of generative AI for years now. I could think of first, it was a coding assistant in my IDE back in maybe 2022. And then, of course, that progressed to us getting those early versions of GPT back in 2023. And then, we were adding our data, right? We were doing techniques such as RAG or retrieval augmented generation to pull in our PDFs and other data sources. And that led us to, of course, other types of APIs and services with agents and MCP back in 2025 and who knows what's gonna happen in 2026 and the years after. The thing is, as I've been using all of these different AI models and AI services, all of this has been through public APIs, and I've both been sending my data but also sending my money to third-party APIs in order to use their models. And now as organizations are looking who deploy their own private and sovereign AI solutions to power all of these applications like RAG and agentic AI, well, how can they be sure that they're keeping, firstly, their costs down when they're deploying their own AI, but also ensuring that they have that data privacy and sovereignty while also having governance and being able to scale this up to not only just a couple engineers, but an entire team of developers and at the end of the day, end users? You probably know what's gonna be the answer. It's a technique that's known as models as a service. So just as we've had, you know, software as a surface back in the day to provide us Gmail and storage and a lot of other utilities that we use every day. Well, models as service is kind of this new pattern that's emerging that's allowing us to serve multiple models, whether it's vision or language models through one singular API, an API that's providing us transparency behind the billing and cost of our GPU utilization, the data privacy and sensitivity of our data and governance, but also observability all through this API gateway, right? But we're also able to then share this to a variety of different users and developers who will then be consuming the model. So the IT team here or platform engineers are serving these models. And then the end developers or users here are the final consumers of these artifacts. And this my friends is what we call models as a service. And I'm really excited to show you how this works behind the scenes and why models as service is becoming a de facto standard for how organizations can scale and deploy models where they work. In fact, I bet that you've already used models as a surface in your own work. So I want you to think about the AI giants, right? So they're not actually giving you access to these huge data centers that they have. They're giving you access to individual models, but they're doing so in a way that's actually quite similar to models as a service. So think about these different versions of models that you can access. You're not accessing them directly. You're going through some type of app or API, for example. Just as we have the API gateway that we just mentioned earlier. So that you can then ensure that you've got billing or authentication or something like that that you need as a prerequisite to then access, for example, the app or the API. So our devs here can now use that API of the model to build out really cool applications, maybe RAG or agentic AI apps. And then the users down here are happy little users that are consuming the AI application. And so this is exactly what models as a service is, and it's already being used today, but the only difference that we're talking about is that instead of renting third-party services and servers or paying for tokens, you're able to run your own models as a service to maintain control over cost, the access of the models and the maintenance of the model. And let me tell you, that maintenance part is super important because, for example, each time a new frontier model is released, let's say a version 7 or something of this model, the older versions are typically depreciated, and sometimes, it's with or without notice. So let's say, for example, we get rid of that V5, and this means, as a developer, if your application is already or currently using that model, you're now forced to upgrade to a newer version of the model. But what happens if the prompt template, for example for version 5, is different than that of the version 6 model? Well, as we know, the model behavior might change, and those bugs are then going to impact the developer down here, which then he has to spend time or they have to spend time fixing their application for the users to consume at the end of the day. So it kind of creates this downstream effect. And so with models as a service, you're able to have full control over the models that you're releasing and the maintenance on how they are released in the lifecycle. So if you want to go to Hugging Face and search for a new model, you can then add that here to your models as a service infrastructure with your IT team and be able to manage what's currently being used most by your teams and maybe depreciate of what you don't need anymore. Now I want you to think about environments that are sensitive. So, for example, when we typically think of data sensitive environments, it's something like healthcare or say financial services where you have a lot of personally identifying information or PII. And the data that is within these organizations need to be handled with a lot of scrutiny because one, it's customer data, but secondly, there's a lot of government regulations and practices around the handling of that data. So it's not easy to just go connect to some type of third-party LLM with that data, right? Because when we're going to a third- party LLM, what we're sending, maybe what might not be sensitive data, but there could be risk of a data break or leakage, and so, all of this information is typically kept on premise. And it's not just the database, right? It's also the applications that are being used. It might also be the, for example, hardware, so GPUs and CPUs. All of this can typically run on-prem or maybe in a mixed hybrid cloud environment where it's on-prem, but also in the cloud and other data sources. But the cool part about models as a service is you become your own private AI provider. So in addition to the applications and the databases, we can also run these local large language models alongside of our applications so that we have this fully air gapped and disconnected environment so that can deliver these secure LLMs but without having to depend on a public cloud provider but we still get the benefits of RAG or retrieval-augmented generation for private documentation with AI, or agentic AI that can call our different services, and it's all within this disconnected environment. So how does this look in action? Well, let's architect it out, starting with the base layer of infrastructure and orchestration, using a technology like OpenShift or Kubernetes. So these are the open-source technologies that allow us to bring together a variety of different environments, such as on-prem, for example, or cloud providers, or say, for example, Edge, if we're running our workloads and AI out there as well. So we can bring together, for example, GPUs, all in one place to be able to dynamically scale them when needed. Now let's also talk about our AI platform layer. So the AI platform is really important in this situation because vanilla Kubernetes by itself can use additional capabilities such as inference engines with VLLM or other projects such as KServe that allow us to orchestrate individual LLMs just like microservices. And this gives us a lot of flexibility when we're running AI workloads. And at this point, yes, technically we can run a model, but to expose the endpoints for our organization and teams to use in a standardized way, well, this involves some type of API gateway. So the API gateway here is the way for us to add these additional enterprise capabilities. So, for example, rate limiting, or maybe authentication for our users, or the ability to do usage tracking, and much, much more, and have observability throughout this entire process, right? Because it's not just the kind of infrastructure itself, but the observability for telemetry, for example, or logging or for example, with AI applications, we need to understand why did they make the decision they made. So this could be the traces of how the LLM is going to an MCP server to call a database and get the information back. So all of this additional information is really important to have, but because of the open-source projects like Prometheus and Grafana and Jaeger, and many more that we're pretty familiar with for traditional applications using open-source technologies as well, what we're able to apply this to AI applications and be able to get a more behind-the-scenes look when it comes to building AI apps. And with this centralized AI infrastructure, instead of having to work from a single model that we've maybe deployed from our IT team to a single team or user, and have to do that multiple times and spread that across, well, we're able to individually call LLMs that are all managed by this models-as-a-service infrastructure up here to be able to support various teams from our organization as they independently scale up their AI efforts, but also make sure that we have cost control in effect. We've got data privacy and full control over our AI adoptions that we can scale things up when we're using AI. So models as a service, it's just one of the many approaches that you can use, but it's quickly becoming the standard for in-house and sovereign AI infrastructure. Now, if you learned something today, please be sure to like the video and hack the algorithm. And stay subscribed for more content on AI and open-source technology. Well, see you.
