![Thumbnail](https://i.ytimg.com/vi/BvCOZrqGyNU/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLB5gw5ThCiuKUmPVZdfbEefqyIJnA)

# DIY AI Infrastructure: Build Your Own Privacy-Preserving AI at Home
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 9:54 |
| **Views** | 154,108 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=BvCOZrqGyNU) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx AI Assistant Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdGWuL

Learn more about AI Infrastructure here → https://ibm.biz/BdGWuT

What if you could run advanced AI models from home? 🏠 Martin Keen and Robert Murray explore how Robert built his own local AI infrastructure using open source tools like Docker and WSL2. 🤖 Jeff Crume then explains how to secure your data with VPNs, private data stores, and multi-factor authentication. 🔒

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdGWuw

#aiinfrastructure #llm #opensource
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
| **Characters** | `9544` |
| **Error** | `none` |


Martin, it seems like AI is everywhere these days. Finally, we have a computer that actually understands my language instead of me having to learn its language. A system that understands me. For instance, what if I'm looking to buy a new car and I need to do some research on the alternatives? Yeah, you could tell the chatbot to act as a car expert and then you can ask it, what would be the difference in cost to operate a gas powered car versus a hybrid car versus an EV car and then get guidance on the decision. And if it helped me find a rebate from the power company, it could pay for itself in just one instance, and if I enjoyed tinkering and DIY projects, wouldn't it be cool to learn how the technology works and host my very own instance of all of this? Yeah, very cool. And in fact, we have a colleague, Robert Murray, who has done just that with equipment in his own home office. Wait, you mean without a server farm of GPUs that dim the lights every time you ask it to do something? Absolutely. So let's bring him in to tell us how he did it. Today, requests to Generative AI typically connect to an AI model hosted somewhere on a cloud, but Robert here has built an infrastructure to host AI models like Llama 3 and IBM's Granite on his own personal infrastructure. So Robert, I want to understand how you did this. Absolutely. o let's start with this box, which represents your computer at home. So tell me sort of the stack that you built here. Sure. So I started with Windows 11. All right, so it's just a straight up. Because I have it. Yeah, ok. That was the reason, just because it's there. It's there. OK, so you've got Wins 11, and then what's on top of that? Well, I unleashed WSL2. Now you're gonna have to tell me what WSL2 does. It's basically Linux on Windows. I'm going to think that there's probably a virtualization layer coming. Yes, there definitely is and that is Docker. Ok, Docker is running on top of all of this. Now, we need some AI models. So where did you get your AI models from? I pulled them down from Ollama.com. OK, so if we take a look at the AI models, what are some of the models that you actually took? Oh, so I started with Granite. Right, IBM's granite model, yeah. Llama, and there's so many other models that you can pull down. Yeah. They're there, Open source. A whole bunch of open source models. Okay, so we've got a Docker machine here with Windows 11, WSL2. You've downloaded these models from Ollama. Is this now the solution? Well, I actually can use this. I can run all this right from the command line. Wow. Okay. So you can open a terminal window and then start chatting with Llama or Granite. Yes. Very, very fast. But most of the AM models that are cloud hosted, you do that on a chat interface, a UI. So how are you able to add a UI to all of this? Docker containers. Ah, okay, all right. So let's put some Docker containers in. What did you have for the UI? I used Open WebUI. It's one of the many solutions that a person could use, but I found this to be extraordinarily helpful. Ok. It's easy to use. Yeah! So with Open WebUI, you can just open up a browser and then chat with the model, pick the model you want, and send requests to it. And there I was, and that's what I was working with for a long time right out of my home. But what if you're on the go? Well, that's where another container comes in. Okay, what have you got here? So it's a VPN container configured with my own domain. All right, so what can access this guy? This. Ah, ok, your phone. So now I am able to access my system from my phone or basically any internet connection. It's awesome. How very cool. All right, well, let's say that I wanted to actually replicate what you've done here and build it. I'm gonna ask you about this server itself. What are the system requirements? So let's start with RAM. How much RAM do I need for this? I would recommend at least 8 gigabytes. 8 gigabytes. That's not much. How much do you actually use? Well, I'm using 96 OK, slightly above the minimum requirement. Absolutely. All right, so let's RAM. What about storage? Storage, I would recommend having at least one terabyte. OK, because some of these models can get pretty big. Yes, they can. Now, these models come in different sizes. So what's parameter count sizes we're using with Granite and Llama? I'm using anywhere between 7 and 14 billion parameters. 7 to 14 billion, okay. I have run up to 70. 70? How did that work out? Slow. I can imagine. OK. So the other thing that people often talk about in terms of system requirements are GPUs. So should I be using GPUs for this? Well. My initial configuration. I had no GPUs, but more GPUs the better The more, the better, right. So, we've got this self-contained solution now, and it's got me thinking that when I talk to a large language model, I often want to provide it documentation in order to chat with that document. Absolutely. Now, if I'm using a cloud-based model, I need to take my document and upload it to somebody else's server so that the AI model can see it. I take it that you have a better solution to that. I do. I use my own NAS system. Okay, so you have a NAS server setup. And from that NAS system, I pull in my documents, pull them into the open web UI, and chat away. And I'm doing it every single day. So Robert, the other thing I like about this architecture is at least to my mind, this looks like a really secure solution. Hold the phone there just a second, nice job AI guy, but let's really look at the security on this Robert. First of all, I think it is a good job here and I think you've put in some features that will help preserve security and privacy, but let's take a look at what some of those are because what you don't want is your data is our data, we want your data is your data, not your data is our business model. So how do we make sure that we're not falling into the same trap that a lot of those other chatbots that are free apps on the app store that you can download aren't falling into. Well, first off, I put it on my own hardware. Yeah, exactly. So I see that very clearly. It's on your hardware, so you control the infrastructure. You can decide when to turn the thing on and off. It's your data on your system. So that's the first point. Absolutely. Yeah, and then also it looks like that you included a private data store. So now it's not your information is training somebody else's model, and you're pulling information that might be poisoned or anything like that. You have some control over that as well. Yes, and interesting enough, that's what's actually got me started on this whole path. By having a NAS, I wanted my data to be my data. And data is the real core of an AI system anyway, so that makes a lot of sense. Also, I noticed some open source components. So you've got one right here, you've got open source models here as well. And that's a good idea, because instead of proprietary stuff, in these cases, at least we have an idea that the worldwide open source community has had a chance to look at this and vet it. Now granted, there's a lot of information to be vetted, so it's not trivial, no guarantees. Maybe it's a little more secure because more people have had a chance to look at what's actually happening under the covers. Agreed. And then also I notice you want to be able to access this from anywhere, which is one of the really cool aspects and we want to make sure that that access is also secured. So I see you put a VPN over here so that you can connect your phone in and do that securely. And how are you making sure everybody else in the world can't connect their phone in here as well? multi-factor. multi-factor authentication, and now we know it's really you, and we know the information is exchanged in a secure way. So a lot of features that you put in here, I think it's a nice job. Thank you. Yeah. And one other thing to think about, because these components, we really don't know what all of them would do, it is still possible that one of these things could be phoning home and sending data to the mothership, even without your knowledge. So one of the things that might be useful is put a network tap on your home network, and then that way you could see if there are any outbound connections from this, because there shouldn't be based upon the way you've built that. Well, that's a really great idea, Jeff. I'm going to have to look into that. Okay, there you go with the improvements for version two. Hey, Jeff. Oh, hey, Martin. Nice to have you back. Yeah, it seems like Robert's really done some nice work with this, don't you think? For sure. It just goes to show that you can now run sophisticated AI models on a home computer to build a personal chatbot. Yeah. Something like that would have been science fiction just a few short years ago, but now it's available to anyone who really wants to spend the time to assemble it all. Right. and you'd like. So much more about a technology by really digging into it and getting your hands dirty with it. Yeah, and by the looks of your hands, you've been doing a lot of digging because those things are filthy, and the added bonus is that you end up with a better assurance that your data is your data because you have more control and you can ensure that privacy is protected in the process. Spoken like a true security guy that you are, Jeff. All right, so you've seen Robert's approach. So how would you, dear viewer, do anything differently to make the system even better? Let us know in the comments.
