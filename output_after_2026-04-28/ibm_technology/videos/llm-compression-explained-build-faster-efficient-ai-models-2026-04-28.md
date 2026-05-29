![Thumbnail](https://i.ytimg.com/vi/wIXr22QTEHg/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBhPnFVpN43TOWPthcB11AeO1X76w)

# LLM Compression Explained: Build Faster, Efficient AI Models
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-04-28 |
| **Type** | Video |
| **Duration** | 11:23 |
| **Views** | 26,255 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=wIXr22QTEHg) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx AI Assistant Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/Bdpsig

Learn more about Small Language Models here → https://ibm.biz/Bdpsih

Shrink massive AI models with ease! ⚡ Cedric Clyburn explains LLM compression and quantization techniques to optimize performance. Learn how to deploy scalable AI with cutting-edge methods for real-world applications!

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdpsiV

#llm #aioptimization #scalableai
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
| **Characters** | `10614` |
| **Error** | `none` |


You typically hear a lot about how AI models are trained. So maybe it's the amount of data that we need in order to get training data. So the data aspect here, which might be trillions of tokens from the internet and other places. Or maybe you've heard about the immense hardware resources that you need in order do a training run. So this could be GPUs or TPUs, other types of accelerators. But what if I told you that the majority of the cost around AI isn't during training but it's actually during the deployment and through a process that's known as inference. So this is actually where all the money is going to once a training job has finished and we have that model, in a process called inference. So, inference is when you have a model, you have it running on an inference engine like vLLM or something like that, and you're using it for all types of tasks. So you're use it for chatbots, right, uh, customer service assistants, other types of uh, communication forms with AI. Or maybe you have PDFs or other documents and you're doing something known as RAG or retrieval augmented generation with your documents. Or maybe you're doing, say for example, vibe coding and you're using other types of agents, right? All of this under the hood, these different types of AI applications, are powered by inference. And that's why it's really important to understand how LLMs are actually deployed in production environments after they've gone through training and how to run them efficiently using optimization and compression techniques. And that's what you're going to learn about today. So, these techniques uh, do a variety of different effects. But the main three are firstly, reducing the latency in our AI models and applications. So that means from the time that you're giving a prompt to the time that you're getting that request back, uh, or maybe the time to first token, which is really important when you're building applications that you want to respond really quickly with, can be reduced through compression optimization of AI models. At the same time, the throughput can be increased. So, let's say you have one or hundreds of different users. Well, they all need to be getting their request back in a timely manner. And so by increasing the number of uh, tokens per second, or TPS, say, for example, 300 or something higher like that, can greatly increase the satisfaction of our users, right? And the last part, the most important part about AI compression optimization and why we do it, is because of the cost. So, as we know, running AI models during the training and the deployment is very expensive. And if we can reduce the number of GPUs or accelerators that we're using in order to run models for our applications, we can save a lot in hardware and allocate that in other areas. So, that's a little bit about AI compression optimization. Now let's learn how it actually works. See, as AI models grow more and more capable, while they're also becoming increasingly expensive and difficult to deploy and run, we're now seeing model parameter sizes go from the billions, so X billion parameters, to trillions sizes, right? So, this comes at a challenge, right? So, models are more capable and can do more than ever, but let's do some napkin math here really quickly, because let's say we take a popular model, say for example, the Llama 4 series, uh, which uh, let's say the biggest one or one of the biggest is the Maverick, and the Maverick comes in at a 400 billion parameter size. Well, if we're going to run or try to run that model at original weights, well, we go from 400 billion parameters, right, and if we are going off what the uh, original weight was released at, well, that's going to be uh, two bytes uh, per parameter. So, this is a floating point uh, 16 release right here. And so you times two bytes per each individual parameter, and the result that you end up getting for this model to run at its original weight, my friends, is 800 uh, gigabytes that we need across different GPU accelerators. And so, for that specific situation here, we'd have to have not one, not two, three, four or five, we'd have to have five uh, different uh, 80 gigabyte cards uh, for GPUs, so something like a A100 that we would be running. Uh, and we'd have to run this across a multi-node setup, and that, my friends, is very expensive. So, you start to see with these really big models uh, why we need to optimize these models to run them in production environments, both quickly but also cost-efficiently and at scale. So, quantizing a model, on the other side uh, is what the action that we need to do in order to kind of shrink this down from, say for example, that floating point 16, so uh, floating point 16 precision here. This is our LLM, and we're actually getting this down to a lower precision. So, one of these might be, say for example, uh, integer 8, and I'll explain how this works here in a second. So here's our LLM, and what we're doing is we're cutting this down to 8-bit or 4-bit integers and greatly reducing the GPU requirements that we need in order to run this model, but also increasing the model throughput and the speed of the model. So what we do is we apply various machine learning methods that apply a sort of smart scaling to the billions of numerical values that make up the model's training, so the weights and the parameters of the model. And this preserves the original LLM's behavior and how it acts uh, while greatly reducing the amount of storage that it needs and space that it needs in order to take up on various accelerators. So this, for example, could be integer 8. So we're keeping those patterns but we're applying different machine learning algorithms like SparseGPT or GPTQ in order to shrink this model and allow it to still do what it typically does as a model but at a much smaller hardware footprint. For this example, we're going to be taking the Llama 4 model. So, specifically, this will be the uh, Scout. And the Scout is approximately 109 billion parameters. So we're gonna be using that for our example today. And by quantizing it or reducing the amount of numerical precision that's required to store and run that model, we're going to go from the original uh, BFLOAT16 precision that it was released at. Which if we have those 109 billion parameters and each parameter is taking up two bytes uh, of storage per parameter, that ends up getting us at 220 gigabytes of weight space of storage that we need in order to uh, run this on GPUs. So that ends being three uh, 80 gigabyte cards, right? So these could be A100s, that could be 10,000 dollars each, more or less, right. And so by compressing and quantizing this model, we go from that original weight that took those three 80 gigabyte cards to something like INT8. And with INT8, we're still doing that same 109 billion parameters, right? But instead of two bytes per uh, parameter, it's only one. So we're at 109 gigabytes of space. And this would only take, uh, in this example, well, it's going to take two 80 gigabit cards, right? So right off the bat, we're already saving a lot. And if we go even one more level deeper, well, let's go to INT4 which is commonly used, 109 times 0.5 uh, bytes per parameter. Then we get about 55 gigabytes of space that we're using. And so this only needs one 80-gigabyte GPU and you still have space for KV cache and other requirements in order to run a model. And so, just by doing this quantization, well, we were able to essentially reduce our hardware requirements from three GPUs to one GPU. And when we run this model, because it's a much smaller memory footprint, we can have up to a five times improvement on throughput. And a lot of tokens per second that our users are gonna be able to receive, which then compliments our satisfaction and, and, you know, the user happiness of the application we're trying to build. And the best part is that Red Hat, after doing half a million evaluations on quantized models here, uh, so doing evals, some that you might be familiar with, such as the AIME or another one such as the GPQA on reasoning, uh, found that wh ... there's actually less than a 1% degradation in accuracy on these benchmarks from the original model right here to the compressed model right here. So, this regularization effect that quantization does can actually even improve performance of the model. So, it's quite an awesome technology. But there's two big questions I want you to think about if you're looking to dive into model compression. Firstly is the AI use cases. So let's think about the two main AI use cases, right? If you're looking to build online uh, applications like chatbots or RAG or agents where a user makes a request and in real time that LLM actually provides a response, well, minimizing latency is key. So we're gonna be looking at weight only activation schemes such as W8, uh, and activation 16 quantization uh, that will provide a better output just because the GPU isn't always fully utilized. But there's a lot of other use cases uh, for AI and LLM inference, right? On the other hand, we've got offline inference. So let's say we have uh, thousands of customer transcripts that we need to analyze for sentiment, right? And the GPU is always going to be at full capacity. It's always going be busy. So formats like floating 0.8 or maybe integer 8, as we were just talking about here, are optimal because you can accelerate that rate of computation. And luckily, through Hugging Face, it makes it really easy to access different AI models that have been pre-optimized using these compression techniques from the leading labs like Llama or uh, various other uh, types of model families. And you can even use the open-source LLM compressor. So this is a open-source uh, project that is part of the vLLM umbrella, which allows you to import a model from Hugging Face to apply a quantization algorithm, one of these or various others, and save them so that you can go and use them on an inference engine, such as uh, vLLM, to get an API endpoint for your developers to use and share across your organization. So quantization, all in all, and model compression is a great way to save on cost related to AI from inference, but also to speed up uh, your throughput so that you can deliver AI applications faster and at scale. Plus, it's not just LLMs, it's also vision models and much more. I want to thank you so much for watching. If you learned something today, please be sure to hit that like button to hack the algorithm. And stay subscribed to the channel for more on AI and open source.
