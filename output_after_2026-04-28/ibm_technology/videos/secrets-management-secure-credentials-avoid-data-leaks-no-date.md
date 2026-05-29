![Thumbnail](https://i.ytimg.com/vi/BqekRTA6VCs/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCYWIV2o63mCBzGi-ZfRWQzv7Ls-A)

# Secrets Management: Secure Credentials & Avoid Data Leaks
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 9:40 |
| **Views** | 12,241 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=BqekRTA6VCs) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified Deployment Professional? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdnRTf

Learn more about Secrets Management here → https://ibm.biz/BdnRTP

12,000 API keys leaked in training data—are your secrets at risk? 🔒 Jeff Crume reveals how centralized secrets management combats sprawl, plaintext storage, and unauthorized access. Learn to encrypt credentials, rotate secrets, and protect sensitive data in modern IT systems.

Read the Cost of a Data Breach report → https://ibm.biz/BdnRTv

#cybersecurity #apikey #dataencryption
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
| **Characters** | `9251` |
| **Error** | `none` |


I've got a secret. In fact, I've gotten hundreds of them, and I'll bet you do too. Don't worry, I won't ask you to tell me any of them, but let me ask you this, what's the best way to keep a secret? The simple answer is don't tell anyone, but if that secret is a credential that needs to be shared so that other users or applications can function, then how do you give them access without leaking it to the whole world? That's what secrets management is all about, and it's what we're gonna unpack in this video. We'll take a look at... What are secrets from an IT perspective? What are the issues involved? And how can you keep secrets secret? Okay, let's start with what are IT secrets? Everybody's got tons of these, as I said. For instance, you've got passwords. Those are things that let you get into a system, and hopefully you're the only one that knows what those passwords are. If you've programs, applications, then they're probably using a different form of authentication, maybe using something like an API key. So these things will be sitting out there and you may have tons of these things. Cryptography, if you're gonna keep your information secret, then you need to be able to encrypt it, and that means you've got keys, sometimes private keys, public keys, symmetric keys, all kinds of keys, but you've get keys and those need to be also kept secret. Related to that, if your doing anything with PKI, public key infrastructure, Then you will probably need to know about certificates, digital certificates. And these things, while technically not secret, they do need to be stored in one place. The certificate generally just has public information in it, but you still need to have one trusted source where you have those things so that you can go look them up, and therefore it would be a good thing to manage all these together. And finally, we could have all sorts of other, I'll just call them tokens, as a general catch-all term. That would be for other things. You may have dynamic tokens and other things of that sort. So look at all of these things and I'm going to suggest that you've got tens of these. If you're an organization of any size you probably got hundreds. You might even have thousands of these thing. So that's what it is. A lot of secrets and you've gotta manage them all. You can't remember them all so how are you going to manage them? Now let's take a look at what some of the issues are with storing those secrets. Well, one of the first ones is this issue of sprawl. That is, you're gonna end up with these secrets spread hither and yon all over the place. You might see them in source code. If somebody were to actually see the source code, they might be hard coded in there. It could be in config files, which are generally visible to people that might have access to them. It could in a version control system of some sort, where, again... this information might be stored in the clear, which leads me to my next point, that this stuff is stored in clear is an issue. Another example of places where these secrets might be kept might result in them being logged, written out to a log of some sort, and then if anyone has access to the log, they're gonna see the secrets, and that's not a good thing to do. Another thing, in fact, that's a theoretical risk that I'm referring to. There was one recent report that came out where there were 12,000 live API keys and secrets of that sort that were found in a training data set that's used to train large language models, some of the really popular ones that you know of. So that means if that's going into the training of those systems, those systems might spit those things out at some point in the future. Again, a big problem. This stuff needs to remain private. That's why we call it a secret in the first place. I also need to manage access. So I need some sort of access control capability so that we can keep it secret, but it needs to be revealed to the right person, the person who is authorized to see this stuff. I need to be able to monitor how all of this stuff works, who is accessing it and when and why, and then ultimately, secrets can't stay that way forever. We need to able to rotate secrets. That is, if it was a secret now, if someone has enough time, they might be able brute force, guess what that secret is or discover it through some other means over time. So we change them over time and that way this rotation of secrets becomes a way that we add additional security into the system. If I'm not rotating, then I'm basically a sitting duck and we wanna be a moving target. So those are the issues. Now, how are we going to address those? Well, the first one I talked about was sprawl, and in that case, you can see if I've got multiple sections of source code or multiple systems, they've got secrets embedded in them. That's a problem because the more different places they are, the larger the attack surface is, and the harder it is to secure all of those different things. So what would I want to do? Well, ideally, what I want do is centralize. So I want be able to take all of this stuff and come up with a centralized secrets management system and have these systems go query it whenever they need the secrets. Therefore, we keep the secrets here and not there, that addresses the sprawl problem. The next thing, how about this information in the clear, the secrets that are in the clearer, obviously are not secrets, those are public secrets. So the clear simple answer is encrypt those things. So if I do that, then if someone does happen to look into one of these systems, then they're only gonna see encrypted information, they're not gonna see the actual thing. How about access control? Well, have access control lists. have an authentication system, then make sure that you are authorized to access this information in the first place and add that into the secrets management system. Other things that we might do is monitor, okay, I need to be able to audit this system. I need see who accessed it and why. And then ultimately, rotation of secrets so that they change over time. Well, what I wanna be able to have there is this notion of dynamic secrets. with dynamic secrets. Now I have a system that can do ephemeral secrets. In other words, it's a temporary thing. It's time-based and unique secrets. That is, it is unique to every single system. There's no shared secrets across or duplicated secrets. Every single one is unique. Every single has a short lifespan. So it makes it really hard for a bad guy to discover these things and use them before they've expired. Okay, what would a system that does these kinds of things actually look like? Let's take a look at the architecture. So who do we have trying to access this? Well, as I said, we've got users that are gonna try to get into the system. We've got a bunch of different apps that are going to try to getting in. We may have cloud instances that are trying to get in. So I've got all of these things trying to access the secrets. And then somewhere over here, I'm gonna have some data store. that is gonna have the actual secrets in it, and this is going to be encrypted for sure, so that if someone gets a hold of that, they still can't see what's in there. So users trying to access secrets. Now, how are we gonna handle this? Well, what I need is a system in the middle that does this secrets management. And one of the major things that it needs to be able to do are the four A's. If you've seen any of my videos on identity and access management, I talk about these four A's. So, what are they? Well, it's authentication. That's answering the question, who are you? There's authorization. That's entering the question are you allowed to do this or not? And then we have administration. That's how I control these previous two A's. And then ultimately, I mentioned a monitoring and audit system. That's the fourth A. I wanna be able to audit the information and see if I did the previous three A's correctly. So now I can authenticate that it's the proper user, the proper app, the proper cloud instance that is accessing these things through these kinds of forays and monitor all of that. The other things I need to be able to do, I'm gonna call this CRUD. This is create, read, update, and delete. So I'm going to create a secret, I need be able read the secret, I need able to update it at some point, and then ultimately delete it and retire that secret, and the update part... I mentioned previously, is this business of rotation. So I need to be able to change those over time. So here we have a secrets management system that sits in the middle between the systems and users that need to access the secrets and the secrets themselves and manages all of that access and keeps it all very simple. So these things don't have to know this directly. They just need to know what they want and how to get to it. Now that you know what needs to be done, You could build all this from scratch, although I wouldn't recommend it because this stuff is really complex as you can see. Better would be to leverage an enterprise class secrets management tool that does all the heavy lifting for you. That way your secrets will truly be just that, secret.
