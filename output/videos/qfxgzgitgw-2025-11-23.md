# _QfxGZGITGw
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2025-11-23 |
| **Type** | Video |
| **Duration** | 8:33 |
| **Views** | 29,362 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/channel/UCKWaEZ-_VweaEx1j62do_vQ) |
| **Subscribers** | 1,740,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=_QfxGZGITGw) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified z/OS v3.x Administrator? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/Bdba2X

Learn more about Open Source AI here → https://ibm.biz/Bdba2H

Open Source AI and Closed AI each offer unique advantages 🔍. Lauren McHugh Olende explores how models, data, orchestration, and applications form the AI stack. Discover how LLMs and AI agents are driving innovation across open and commercial systems.

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/Bdba2r

#opensourceai #llm #aiagents #aistack
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
| **Characters** | `6331` |
| **Error** | `none` |


Whether you're creating a simple AI chatbot or a complex AI agent, it's possible to architect a solution from end-to-end fully with open-source components. Understanding these pieces, how they work, the benefits, the frictions will help you evaluate where you want to consider open versus closed solutions in what you're building. Researchers from Harvard Business School estimate the value of all open-source software—which means software whose source code is publicly available and distributed freely—to be worth 8.8 trillion dollars. Within AI specifically, many of the most exciting new features from commercial AI tools are rapidly recreated as open-source implementations, which are made by—and distributed freely among—the AI community. Here, we'll cover the main components of open-source AI—models, data, orchestration and the application layer—and talk about the tradeoffs for each. Because open source focuses on software, we'll exclude the infrastructure and hardware layer, but that's a really important consideration too. Deciding whether to use open or closed AI in your stack is one of the most important choices a developer will make. The central point of the AI stack is the model. Different types of open-source models are available. They can range from LLMs—large language models—that are base tuned, as well as fine-tuned versions that are created by the community and made available for others to use. These could be fine-tuned on specific tasks, like question and answer, or on specific domains, like the legal domain. There's also other specialized models that are available in the open source. An example of this would be a model to do anomaly detection in biomedical images. If you're using an open-source model, you will also have to uh, implement your own inference engine to actually run these models. Options to run these models include open-source libraries that allow you to run these models on your laptop—one of the most famous ones being Ollama—or open-source inference engines to run on a server. Popular examples of this include vLLM or TensorRT LLM. On the other hand, if you're using a closed model, these are usually available via an API. You have to worry about making a call to the API, but this often means that the other layers of the stack are fully managed for you. You don't have to worry about the inference engine to run the model—including the optimizations to make it efficient—or worry about the infrastructure it runs on. The next layer of the stack is data. Now, this is one layer where actually the elements for both open and closed are the same. So, first you have to consider what are your data sources that you want to bring in to supplement or augment your AI model. There's your data connectors or integration to pull in data in a more automated way from tools or other sources. data conversion. If there is data you want to use in your AI system, but it exists in an unstructured way in a PDF, you first have to convert that to a more structured format. And then there is RAG pipelines and vector DBs, which is where you store your data once it's been vectorized into embeddings so that your model can pull it into context. Now these elements are the same between open and closed, but what varies is, of course, one is uh, open-source code that is freely available, one is not. Uh, so, one benefit of open source is that it's available for free, Closer, closed source is usually part of a commercial tool. So, one consideration is: Is it freely available? Next is, with open source, because the source code is available, you can actually make customizations or adaptations that you need to. Whereas with closed source, some of those might actually already be built out of the box. But if they aren't, you don't have the ability to customize. And then third is control over where it's deployed. So, because the open-source code is source code that's freely available to you, you can set this up on any server that you choose. You can keep it on premise, or you can deploy it to a public cloud. With closed offerings, these are mostly available via an API in a fully managed hosted solution, so you don't have as much control over where your private data might be going to or coming from. The next layer is orchestrate. Orchestrate defines how you break down your AI system into smaller tasks. This could be things like reasoning and planning how your AI system will tackle a problem. It could also include executing, so actually making tool calls or function calls. It could include loops to review what your agent has k-come up with and improve the quality of the response. How you actually implement these things is determined by which open-source agent framework you choose. On the other hand, in a fully closed source stack, there are some commercial platforms that allow you to do agentic tasks and control the orchestration through an API. So what you have to worry about is making an API call that matches up with those specs. It is, on the one hand, simpler, but in some cases might be oversimplified because you don't have as much control around the exact structure of your agent and ability to customize it uh, as if you're dealing with an open-source agent framework. Finally, is the application layer. This defines the interface that your user will use to interact with your AI solution. On the open side, the solutions to do this emphasize customizability. So you could use things like open web UI or anything LLM to give you full control over the user experience. There's also options to optimize for quick setup. Things like Gradio or Streamlit, which let you very quick-quickly create web-based interfaces with minimal setup for interacting with an LLM or AI-based solution. On the closed side, the primary route would be to build from scratch. So this would mean embedding your AI solution directly in the application, whether it's a web application or the mobile application that this fits into. Understanding each of these layers—models, data, orchestration and application—gives you insight to make informed choices. There may be cases where you want the convenience of prebuilt closed-source solutions, but it's also valuable to remember open-source AI options, which offer transparent and adaptable solutions that benefit from community innovations.
