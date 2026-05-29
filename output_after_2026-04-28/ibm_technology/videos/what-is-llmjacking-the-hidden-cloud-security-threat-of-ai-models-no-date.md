![Thumbnail](https://i.ytimg.com/vi/dibZ1itSvM4/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCxm6uDeNdlrKE9v8IDq4roStubqA)

# What is LLMJacking? The Hidden Cloud Security Threat of AI Models
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 7:21 |
| **Views** | 32,287 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=dibZ1itSvM4) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified Administrator - Cloud Pak for Security? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdndTX

Learn more about Cloud Security here → https://ibm.biz/BdndTH

LLMJacking 🛡️ is a costly AI hijacking attack exploiting cloud vulnerabilities ☁️ and shadow AI 👥. Jeff Crume explains how attackers use large language models to drain your resources 💸. Learn how to spot vulnerabilities and secure your cloud systems 🔒 from this hidden threat!

Read the Cost of a Data Breach report  → https://ibm.biz/BdndT4

#llm #cloudsecurity #aithreats
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
| **Characters** | `6880` |
| **Error** | `none` |


Gen AI is an amazing technology that has changed the face of computing seemingly overnight. It can understand what you say using this thing called natural language processing, or it could create a brand new document for you just based upon a prompt that you feed to it. Another useful task is if you've got a ton of documents that are too long, didn't read, I could feed that in and it will give me a summary of just the important point, but running this advanced tech can be really costly, and someone has to pay the bills. The problem is that you may be unknowingly paying the bill for someone else who's riding on your dime. In fact, one report found that this could cost your organization $46,000 a day. That's a lot of money. The name given to this type of attack is called LLMjacking. LLM is in the large language model that's the underlying technology that powers these latest chatbots and jacking. because it's essentially hijacking your environment and leaving you with the bill. Let's take a look at how this whole attack works and what you can do to prevent it. Okay, so how does all this attack work? Well, it typically starts with a cloud instance that you own, but that you haven't really secured all that well. The attacker then figures out how to get into your cloud instance. How are they doing that? Well, they could be exploiting some known vulnerability or maybe it's unknown to you, and they are able to break in. It could be because of some sort of misconfiguration of the cloud environment that you didn't really lock everything down as well as you should have. It could also be from some stolen credentials. This could be passwords, API keys, things like that, and this is not theoretical. In fact, one recent report came out and said that they found 12,000 API keys and passwords that were available. through one of the very popular LLMs in its training data. So in fact, you could go to the LLM and ask it for some of these things and it would just spit that stuff right out for you. So here's how they end up breaking into your cloud environment, and once they've done that, then the attacker goes to a model repository, picks out a model that they like, this is just like shopping, downloads that into this cloud instance and now they have a large language model. a few tweaks more and they're off to the races. They now have their own LLM and it's running on your instance. You're the account holder and you're gonna get stuck with the bill, but that's not the end of it. In fact, if this guy wants to make a little profit, then what he can do is set up a reverse proxy, and the reverse proxy would allow lots of other people to log in, he gives them access, and then it exploits the vulnerabilities or the credentials that this guy used to break in in the first place or maybe he set up some others as a back door into this and he basically charges them access to this LLM. So not only is he having you pay the bill, but he then is getting a lot of this going directly to his pockets. So now we've taken a look at how this particular attack works. Now, let's take a look at what you need to do to protect against it. Well, let's look at the ways that this person was able to break into the environment in the first place. I told you one of them was this thing right here, credentials. So credentials, another word for that, are essentially secrets. And there are tools that do secrets management. In fact, the secrets that we're involved with here are things like API keys. It could be passwords. It could anything like that, that is supposed to be something that allows you to get into system that no one else knows. And what we need is a good place to store all of this kind of stuff, essentially a vault that can store those things and we can access them. And we make sure that we have access to them, not that all of the public LLMs and the bad guys have access them, so that's a good to start, is locking the front door and taking care of the keys once you've locked it. The next thing is, look what was happening in this cloud environment. There was an AI that was running, and it's running in your environment, and you didn't know about it. So this is what we refer to as shadow AI. In many cases, shadow AI can happen because an employee put it there. And they just wanted to experiment with it and see what it was gonna do. And it might be harmless, but you need to know about. So in fact, you can't secure what you can't see. You need to discover shadow AI in your enviroment. And in this case, you'd be discovering a truly illegitimate AI that's running on your system and using up your resources. The other thing you'd want to do if you discovered a shadow AI is to make sure that you secure it, that you have this thing locked down, that you don't have these kinds of problems with misconfigurations and the like. Now another area I said that the bad guy might get in would be through some sort of vulnerability that's found. Well, vulnerability management tools also exist, and we need those kind of capabilities. For instance, I need to be able to patch all the software in this system and that's not always an easy thing to do so use tools that allow you to do that, because every single level of down level old software you have has probably got a number of security vulnerabilities in it and those are the things this guy can take advantage of in order to get into your system. Some other things that we're going to look at is the configuration of this environment, the way the cloud is configured so we're gonna check on these kinds of things as well in that, and make sure that it discovers some of the common errors that people do, where they're exposing information that they wouldn't intend to do otherwise. There's also tools that help with this, cloud security posture management tools. So I recommend something like that in this space. And then ultimately, we need to be able to monitor all of this. Again, you can't secure what you can see. So I need to able to use the standard security information and event management tools and things like that, that look for security issues. that see whenever there are abnormal patterns and things like that. I also wanna look at usage records and see if there are people that are doing things in the system that they shouldn't be doing. Why is this particular cloud instance that's been pretty quiet for a long time, now all of a sudden it's peaked up? And well, maybe the reason that it is hitting a peak is because somebody is selling services on our system. And another thing is, look at the billing records here as well. Just look and see, if you're costing $46,000 a day suddenly for this environment, there might be a reason for that, and you'd want to know that. So do the things that I've talked about right here, and you should be in a better shape to avoid this LLMjacking.
