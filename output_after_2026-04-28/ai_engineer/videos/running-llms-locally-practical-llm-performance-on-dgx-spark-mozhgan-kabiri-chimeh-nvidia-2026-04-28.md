![Thumbnail](https://i.ytimg.com/vi/c5-kx2bwoCk/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAPm99td60yrTTdojeS_a-_Z0tRuQ)

# Running LLMs locally: Practical LLM Performance on DGX Spark — Mozhgan Kabiri chimeh, NVIDIA
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-04-28 |
| **Type** | Video |
| **Duration** | 10:15 |
| **Views** | 4,003 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=c5-kx2bwoCk) |
| **Category** | - |
| **Language** | - |
---

## Tags

`ai` `ai engineer` `ai engineering` `software development` `tech` `startups` `software architecture` `machine learning`
---

## Description

Moving LLM workloads from the cloud to local infrastructure requires a shift in engineering strategy. In this talk, I share my journey of serving and benchmarking open-source models (1.5B to 14B) on an NVIDIA DGX Spark workstation. Using a reproducible methodology with vLLM, I analyze real-world trade-offs in throughput, latency, and the benefits of the 128GB Grace Blackwell unified memory architecture. You will leave with a clear framework for local model sizing, an understanding of quantization performance like NVFP4, and a guide for when local compute is the right choice for your AI stack.

Speaker info:
- LinkedIn https://www.linkedin.com/in/mozhgankch/
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
| **Characters** | `6994` |
| **Error** | `none` |


Hello everyone. I'm Moska Gabricima, developer relations manager at Nvidia, where I work closely with developers building and deploying AI systems. Today, we're looking at running LLMs locally, practical LLM performance on the Jetson Spark. This isn't a theoretical talk. It's a data-backed journey through the trade-offs of modern AI infrastructure. Findings are based on hands-on experiments with the goal of understanding what's actually practical on a single system. The evolution in AI puts greater demand on developer systems, creating two main challenges. You either run out of memory or you do not have access to the right software stack. Then you end up and pushing everything to the cloud or data center. As models move from experiments to production, concerns like cost predictability, data residency, and deterministic latency take center stage. And iteration speed often depends often depends on access to shared infrastructure. And since your work will be scheduled against other competing workloads, it causes delays in development work as well. So, the question becomes, can we bring some of that workflow closer to where development actually happens? To maximize developer productivity, local solutions to these challenges are required. The Jetson Spark is designed from the ground up to build and run AI and can be used as a standalone system. It's powered by the GB10 Grace Blackwell superchip, combining CPU and GPU with a unified memory architecture. With 128 GB of unified memory and NV4 support, it enables developers to work with models of up to around 200 billion parameters locally on a system that fits under the under a desk or on top of your desk. It runs the same Nvidia AI software stack used in production environments, meaning workflows can move from desktop to data center or cloud with minimal changes. The key idea here is not replacing the cloud, but bringing powerful AI development closer to the developer. This is my setup. Everything runs locally and is reproducible. To serve the models, I used vLLM with a set of quant models across different sizes and precision formats. I run this inside an Nvidia optimized container. This would ensure that our environment is identical to what you would deploy in a data center. And [snorts] instead of just showing raw results, I want to show you the how. I built an automated benchmarking harness. Every model run from 1.5 billion to 14 billion follows the same strict protocol. Environment isolation via Docker, three mandatory warm-up runs, and background GPU metrics logging at 1-second intervals. On the left, you're looking at the orchestrator script. For every execution, the script automatically generates a unique directory using a precise timestamp and a sanitized model ID. For every model run, it captures the full model's endpoint response and necessary metrics. On the right, you see the result, a clean, versioned artifact of the run. It contains everything to verify the findings, the metadata, and the text results from the benchmarks. On the lower right, you can see an example command for getting things started. Now, let's look at the actual measurement logic. In an AI application, end-to-end latency is important, but time to first token is the metric that defines the user's perceived performance. If the first token arrives instantly, the application feels responsive. And this script here shows how we timestamp the very first chunk of a streaming response. In this script, we're not just calling an API and waiting for a result. We're explicitly handling the streaming response from the vLLM server. If you look at the highlighted block in the stream_once function, you'll see the timestamping logic. To explore this in practice, I ran a series of experiments using vLLM on the Jetson Spark. I tested different models, from a smaller instruction model to larger optimized variants, all under the same setup. Everything was served locally. The goal here wasn't to push theoretical limits, but to understand realistic behavior in a developer workflow. Let's dive into the raw performance data I captured. >> [snorts] >> This bar chart represents the completion token per second across the test set. At the far left, you see the 1.5 billion instruct model delivering a massive 61.73 tokens per second. But the most interesting data point for us is the 14 billion NVFB4 model. Despite being nearly 10 times larger than the 1.5 billion model, it still achieves 20.19 tokens per second. I would say this is a critical engineering sweet spot. By leveraging Nvidia's NVFB4 4-bit floating-point quantization, we were we are able to maintain a sophisticated, high-intelligent model at a throughput that is still faster than the average human reading speed. What becomes very clear here is how aggressively throughput drops as model is scaled as models scale. And how much quantization helps. Have a look at the 14 billion base model. It drops to just 8.40 tokens per second. This proves that on Blackwell archi- on Blackwell hardware, the choice of quantization format is just as important as the hardware itself. It's what allows the Jetson Spark to bridge the gap between research work and production prototyping engine. The Spark allowed me to experiment with different precision formats locally and understand the trade-offs in the real time. While throughput is a measure of raw power, time to first token is the metric that defines user experience. It determines whether an application feels instant or broken. In other words, it reflects how quickly the model is starts responding. As we see in the results, the Jetson Spark delivers exceptional responsiveness. The increase for larger models is expected. More parameters mean more computation before the first token is generated. Out of all from this chart, the interesting ones are the comparison between the 14 billion parameter models, the base model and the NVFB4 model. As we can see, as we can see, the 14 billion NVFB4 is 3.4 times faster to first token than the unoptimized 14 base model. A key takeaway here from this data is that memory capacity is not the same as the memory bandwidth. While the Jetson Spark's 128 GB of unified memory allows us to fit massive models up to 200 billion parameters, our throughput is still governed by how efficiently we can move data. This is why NVFB4 is the hero here. It effectively increases our intelligence per byte, allowing a 14 billion model to feel as responsive as much smaller one. After running all of these, two things stood out to me. On when to use the Jetson Spark. For steady-state workloads, privacy-sensitive data, and rapid prototyping. It allows you to build and fine-tune locally with the exact same software stack used in Jetson cloud. Visit build.nvidia.com/spark to access the playbooks and software stack I used for these benchmarks. And in one run locally, iterate quickly, and when ready, scale to data center or cloud. That's the workflow that J uses Spark enables.
