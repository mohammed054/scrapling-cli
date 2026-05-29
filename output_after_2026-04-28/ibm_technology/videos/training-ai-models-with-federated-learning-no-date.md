![Thumbnail](https://i.ytimg.com/vi/zqv1eELa7fs/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCITQYu-3jv7fGp_PAxkl2OrXkgpQ)

# Training AI Models with Federated Learning
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2y ago |
| **Type** | Video |
| **Duration** | 6:27 |
| **Views** | 50,611 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=zqv1eELa7fs) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Explore  watsonx.ai → https://ibm.biz/Bdy4qU

Federated learning is a way to train AI models without anyone seeing or touching your data, offering a way to unlock information to feed new AI applications. In this video, Martin Keen discusses the forms, benefits and challenges of federated learning. 

Get started for free on IBM Cloud → https://ibm.biz/sign-up-now
Subscribe to see more videos like this in the future → http://ibm.biz/subscribe-now

#ai #watsonx #llm
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
| **Language** | `en-US` |
| **Characters** | `5567` |
| **Error** | `none` |


Let's unpack the concept of federated learning, a method for training AI models that is all about keeping your sensitive data right where it should be, with you. Now, AI applications like chatbots, recommendation systems and spam filters, they're all very data hungry and they have been fed tons of examples, mountains of information which they use to learn their specific tasks to build an AI model. Now, normally in machine learning, we gather all of this data from different sources and bring it to one place. All of this will reside in a central server and that's where the actual training of the model takes place. Federated Learning turns this process on its head. Instead of bringing the data to the model, we take the model to the data. So here's how it works. Think every device, like a smartphone or a laptop or a server, it has its own local version of a model. O each of these are reporting into their own model. And this model learns from the data right there on the device itself. Now, after the model has learned from the local data, it sends only the model updates back to the central server, not the actual raw data. So this all goes here to the central server. And then that server aggregates all of these updates from all the devices to create what is called the global model. Now, why bother with this level of decentralization? Well, this concept was first introduced by Google in 2016 at a time when global attention was focused on the use and misuse of personal data. Concerns about data privacy and security prompted the search for alternatives to traditional centralized AI training methods giving birth to federated learning. So let's imagine a scenario involving a group of companies that want to collaborate on building a model to predict market trends. But each company has sensitive sales data they want to keep private, so each company has access to an initial baseline predictive global model. Here's our global model up here. And this resides in a central server. Now in their individual environments, each company trains the instances of the model using their own sensitive sales data. So we have the global model here and then these individual models with each company, and here is their sensitive sales data along the bottom. And they're tweaking and refining their model based on their unique data. So the companies do not share their sensitive sales data. Instead, they only share the updates they made to the model. Now, these updates, they don't contain any raw sales data, but they do reflect the insights gained from the data. The model updates are then sent back to the central server. And here they integrated into the global model. Now, this iterative process continues with each company refining the model based on their private data and sharing only the model updates. Over time, this model becomes increasingly accurate at predicting market trends, even though no company had to share this sensitive data. Each company benefits from the collective intelligence of the group while maintaining their data privacy. That is the essence of federated learning, allowing for collaborative learning from shared model updates while keeping the actual data distributed and private. Now we can think of federated Learning as coming in three flavors. So there's "horizontal". And horizontal federated learning describes the forecasting model example we've just discussed where the data sets were all similar. In this case, the similarity was this was all sales data. Now another one is called "vertical" federated learning. So instead of using similar datasets, we're dealing with complementary data using movie and book reviews, for example, to predict someone's music preferences. And then the third kind is called "federated transfer learning". Here we start with a model that's already been trained to do one task and then adapt it to do something slightly different. Like how a pre-trained foundation model designed to perform a task like detecting cars is trained on another dataset to do something else entirely, like identify cats. Now the use cases for federated learning are far reaching and impactful. Just consider the health care industry where federated learning allows medical institutions to collaboratively train their models on their sensitive data without sharing the actual medical records. Or how financial institutions can improve their fraud detection mechanisms and credit scoring systems without compromising on customer privacy. However, federated learning is not without its challenges. There is the risk of inference attacks where adversaries may try to extract information about the data from the shared model updates when we put them up there. Now, to counter this, researchers are looking into strategies like secure multi-party computation to ensure privacy by encrypting model updates or by adding a degree of noise to the data to mislead potential attackers. Other challenges include computational efficiency because we do have all of this work going on locally here and maintaining transparency in model training and creating incentives for truthful participation. But in the end, Federated Learning offers a promising path towards a new generation of AI applications by addressing privacy concerns and leveraging the power of distributed computing. Federated Learning holds the potential to revolutionize how AI models are trained. If you have any questions, please drop us a line below. And if you want to see more videos like this in the future, please like and subscribe. Thanks for watching.
