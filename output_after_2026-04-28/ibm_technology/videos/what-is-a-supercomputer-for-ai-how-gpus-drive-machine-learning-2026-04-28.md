![Thumbnail](https://i.ytimg.com/vi/zocwmW5wZe8/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBUvroTXpHXcEORf-JvNIrlSFlwqw)

# What is a Supercomputer for AI? How GPUs Drive Machine Learning
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-04-28 |
| **Type** | Video |
| **Duration** | 9:13 |
| **Views** | 9,601 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=zocwmW5wZe8&pp=0gcJCQ0LAYcqIYzv) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx Data Scientist? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdpZcP

Learn more about Graphics Processing Unit (GPU) here → https://ibm.biz/BdpZcy

 🚀 Did you know GPUs, originally built for gaming, now fuel generative AI? Lauren McHugh Olende explains why GPUs outperform CPUs for AI tasks, enabling large-scale models like LLMs with faster memory and parallel processing. Discover how AI hardware drives innovation—and why it matters for your projects!

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdpZcM

#machinelearning #ai #gpu #cpu #supercomputer
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
| **Characters** | `6441` |
| **Error** | `none` |


How did graphical processing units, or GPUs, which were originally built as hardware for video gaming, become the most popular and ubiquitous infrastructure used in generative AI today? And why are traditional CPU-based data centers not repurposable for AI in all cases? And does everyone need expensive hardware to build and run AI systems? The breakthrough behind the rise of generative AI is often credited to software innovations, like new AI algorithms that came out with the transformer model architecture. But hardware breakthroughs were equally important, such as new kinds of chips and better computer chips, which have allowed researchers to train models at a massive scale to make them as knowledgeable as we know them to be today. For example, have you ever opened a Excel file in your laptop with thousands of rows of data and your laptop crashed? Then you know the pain of hardware limitations. And an AI, and in particular in building LLMs, hardware limitations happen just the same, except at a vastly larger scale. Think of datasets and calculations that are big enough to crash tens of thousands of laptops worth of compute. And that's where GPUs come in. So let's break down why these types of chips are so important in making generative AI possible. To understand why GPUs process AI tasks faster, let's start with how these computer chips fundamentally work. So chips like GPUs or CPUs have tens of billions of tiny electrical switches called transistors. Different groups of these switches have different functions. Some of them handle math computations. We'll call those compute. Some of them store the working data and the instructions for those computations. We'll call that cache, which you can think of as the short-term memory. Some decode instructions and plan and coordinate which steps happen in which orders for, which order for these calculations. We'll call these control, which really control the logic. And then some store input data for the calculations. We'll call that the memory and you can think of that as longer-term memory. So, CPUs are designed to solve a wide variety of tasks quickly. Why? That's because CPUs are what we use in our personal computers and data centers where they need to be general purpose to switch between different things like web services or databases or analytics. So when it comes to compute, relatively speaking, we'll put that low. They do few, they have fewer, less emphasis on mathematical operations. The cache we'll put at moderate or medium because they do need short-term memory to perform the calculations that they do, but the control is where we'll put them at high. And that's because they have to do more instruction following, more handling of branch logic that varies across task, more scheduling of which operations get done first. The memory we'll put at relatively lower, because CPUs normally just borrow the memory from the rest of the computer. They don't have, they normally don't have dedicated memory. GPUs, on the other hand, are meant to process a high number of similar computations at once or in parallel. For compute, this means a high number of mathematical operations running at once. For cache, it's similar. They need some short-term memory to get those calculations done. For control, though, it is fewer because most of the calculations it does is the same calculation performed at a vast scale, but not as much variety as a CPU. For the memory, we'll put it at high, because at least in the case of AI, a GPU needs to store model weights. And if you remember, model weights have grown exponentially in recent years. When one of the first open LLMs came out in 2018, called BERT, it had about a 110 million parameters. Now we have LLMs with over a trillion parameters, so that requires a lot of memory. And not just more memory, but also faster access to that memory, which is also referred to as the memory bandwidth. This, ultimately, is why GPUs work for AI and LLMS. GPUs are great for performing a high volume of mathematical operations that are highly parallel as well, meaning it's the similar operation performed at a large scale, all while holding huge model weights in memory or VRAM. And there's a really interesting reason why GPUs were originally built with so much memory. And that's because they were created to render graphics faster, mostly for use in video games. So in graphics, large memory was used for holding data on the values of textures or lighting or shading or physics. And now, we repurpose that same large memory for holding huge model parameters. So without video games, we might not have LLMs as we know it. Now the next question is, do you always need GPUs or a whole AI data center to build AI systems? It really depends on what you're doing and the size of the models that you're using. If you're training an LLM, typically requires a GPU, no matter the size of the model, because training workloads are more intensive than simple inference workloads. If you're tuning a model, large models typically require a GPU. For small models, they also typically require a GPU but there may be exceptions where you can use a CPU, if it's an especially small model, you're using a parameter-efficient tuning technique on a compressed model. Finally, if you're running a model, take into consideration whether you're running it for a personal use application, something where you don't see a high volume of use, in which case, if you're using a single model with a single inference call or very few inference calls, CPU might certainly suffice. If you're using even a just a personal application but a larger model, say something above 10 billion parameters, you'll likely want a GPU for the kind of speed that you're hoping for. If it's a customer-facing app meant to support more users and larger tasks, GPU is typically required if you're using a larger model. And even if you are using a smaller model, GPU is typically required because otherwise you'll experience high latency. It's important to remember it's AI hardware, not just the algorithms that have enabled generative AI. However, building AI applications doesn't automatically mean you need to use a whole data center full of GPUs or even any GPU at all in certain cases. So despite these chips being a critical technology for generative AI, you don't need to let that deter you from starting small, with the hardware that you have access to today.
