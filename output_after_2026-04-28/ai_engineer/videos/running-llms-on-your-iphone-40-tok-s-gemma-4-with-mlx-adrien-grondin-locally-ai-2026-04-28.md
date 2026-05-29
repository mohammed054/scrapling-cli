![Thumbnail](https://i.ytimg.com/vi/a2muGkT4WD4/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAMCN42JXfELCrJgi8XVsAMd7DnSQ)

# Running LLMs on your iPhone: 40 tok/s Gemma 4 with MLX — Adrien Grondin, Locally AI
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-04-28 |
| **Type** | Video |
| **Duration** | 10:50 |
| **Views** | 10,130 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [AI Engineer](https://www.youtube.com/@aiDotEngineer) |
| **Subscribers** | 491,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=a2muGkT4WD4) |
| **Category** | - |
| **Language** | - |
---

## Tags

`ai` `ai engineer` `ai engineering` `software development` `tech` `startups` `software architecture` `machine learning`
---

## Description

See more: https://x.com/adrgrondin/status/2040512861953270226

Speaker info:
- https://x.com/adrgrondin
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
| **Characters** | `9364` |
| **Error** | `none` |


[music] >> Okay, hello everybody. I'm going [clears throat] to show you today how to run Gemma 4 on iPhone with MLX. So, first let's introduce myself. I'm Adria. You can find my Twitter if you want to learn more about all on device things. I'm a developer of Locally AI, so maybe you have already seen the the app. So, Locally AI is a chatbot that allow you to run on device models on your iPhone with MLX. So, I will just go through what is MLX in a in a few few seconds. Basically, as I said, it's it's a chatbot. It's fully native. You can also chat with Apple Foundation with it. And and many models like that are compatible with MLX. And one of those models is Gemma 4. So, basically, [clears throat] Gemma 4 by Google in mind have a lot of model and some of them like can run on iPhone like the smaller ones and they are pretty great. Maybe you have seen on on Twitter one of the post I've made that I should I demo it running in the app on iPhone. It's really fast. It runs really well on MLX. And behind the app, so it's using [clears throat] MLX. MLX is a framework made by Apple that is optimized for Apple Silicon. So, mainly mainly the the chip [clears throat] in iPhone, but also the chips on the on the Mac. The the app Locally is available on iPad. It works also very well on this device and Mac OS. And everything is is built to be as optimized as possible on on this devices. So, if you want if you want to run on iPhone a language model, so Gemma works well, but you have a lot of model that you can run also. The Quen model and and the small LM model from Hugging Face. The place you you will want to go is GitHub and go to the repo MLX Swift LM. I won't go into detail how you implement the repo. It's I think I will let your agent in a implement that for you, but it's one repo that you need to install if you're developing an iOS or Mac OS or iPad OS app. And you can use you can use that to simply download the model and then run it. The API is very straightforward, very simple to to implement. In less than 10 minutes, you can have an iOS app with a model that is running on your on your device. That's very simple to do. As as mentioned, MLX So, this is MLX Swift LM, but if you're more into Python apps or Mac OS app, you can also run MLX VLM from from Prince. Maybe you have seen him that he's doing on device for audio with MLX audio and visual model with MLX VLM and also MLX video to to run to run image image generation model or image or video generation model. MLX it's the ecosystem is getting bigger it's getting bigger it's it's really great right now. You can do pretty much everything like omni models. As I say, text to speech speech speech to speech. There's a lot of thing that you can do with um with a model. And basically, let's say you integrate the you integrate this model. You can't just run any model on it. Like you need to you need to get some model and there's a good place to get the model is Hugging Face. I'm pretty sure everybody heard uh of Hugging Face. And on Hugging Face, you will want to look for MLX community. This is where like all of the the weight of the model, the quantized weight, the full size will be uploaded. So, you will just be able to go to this community look for the models. I think right now there's almost 4,000 or 5,000 model uploaded. So, the community is really active on it. When a model is is released by a by a lab you will directly have it almost 30 minutes after release quantized in 4-bit, 6-bit and everything that you can you can imagine. Here you have like an example for Gemma 4 8-bit, which is the one I I run on um on iPhone. There's like a lot of variant of it for from BF16 and make MXFP4 [clears throat] like 5-bit, 6-bit there's everything. So, so you download MLX Swift LM, install it with your agent or anything. Then you go to MLX community and you just choose the model you want to run and then with ID you can just pass it to the framework and it will directly it will be integrated with Hugging Face to download the model with MLX Swift LM directly. So, you just need to grab the ID and and pass it to to the framework. Usually, when you're running the the model on on iPhone, what you want to what you want to do is quantize select selecting some quantized quantized version of the model because the full size will be way too large. What I recommend is going is trying depending on the size between 3-bit and and 8-bit. Usually, between 4-bit and 8-bit. Usually, under like 4-bit it's getting it's starting to get a lot of impact on the output. And and the model are not that great usually. 4-bit is the lower I would go. And 8-bit is the higher I would go if you're using really small models. And in my app for example, I have like some bigger model like Gemma 4, but I also have some liquid model where that is 300 350 parameters and this it can run in shortcuts. So, you can do a lot of kind of automation because the model are really fast and really efficient at that at that size to do some text processing and things like this. And on the on the latest iPhone like if you take Gemma 4 8-bit quantized in 4-bit it's extremely fast. Like it can run easily at 40 token 40 token per second. I will just do an update in the slide because I remove I remove a slide where there's the video, but maybe I can add it back because I have a little bit more time. I just like this. So, just to show you in demo what's what the 40 token per second means. And that's running live offline. And as you can see, it's like really fast. Like 40 token per second is more than acceptable for a lot of use cases. This is of course streaming. You can also like not do streaming and do a UI that just will wait for for 4 seconds. And here the output is quite long. So, it's generating a lot of tokens. On device with MLX, it's working. It's here. Like it's really not easy and really not hard to to integrate. As I said, if you go to the to the repo MLX Swift LM very it's a breeze to to install. On top of that, as I said like again, latest iPhones really great, but it works also with older iPhone. Like you will not get 40 token per second, which is quite fast, but even if you get 20 tokens per second, that's already great and useful for a lot of for a lot of application a lot of use cases that you would want to do with with your with your with your app. You can go to and scan this QR code if you want to try it by yourself. If you want to have a if you have an iPhone, the app is on the App Store. It's free to use. Only thing is that you will have to download the model that's usually around 1 gigabytes or 3 gigabytes. Really depend on the on which model, but that's the biggest barrier right now. It's the size of the model, but this also is getting better. Model are getting smaller or getting smarter and they're also the iPhone is getting better. So, next and second the next next iPhone everything will just is reaching really great usability from what I can see. And also on top of that like maybe you have heard the news yesterday. Locally have been acquired by LM Studio. If you don't know LM LM Studio >> [clears throat] >> it's basically a kind of a AI studio for all your local models. So, you can download the the model with any model with LM Studio directly from Hugging Face. You can run them and you can open a server. You can run them with Llama CPP, but also MLX. So, you can really compare the different engine how they how they work. You can as I said, you can open a a server locally and connect your app to this to this hosted server with various various response response type. For example, open open API response type or >> [clears throat] >> or or Anthropic response type for streaming anything and you can just get any model running really easily with that. So, and I want to thank you. That was a very short introduction how you can do the same and run any model like in Gemma 4 if you want on your on your iPhone. If you have any question also. >> [applause] >> Does this support tool calling? Sorry? Does this Yes, like so yeah, I forgot about that. So, it support tool calling. Um not yet custom not yet structured generation. There are some package on top of MLX Swift LM that are trying to to make this make this working. Um I will let you Hugging Face is doing it, but you can easily find them online. But MLX Swift LM, yes, it support tool calling. So, that's really useful if you want to do tool calling and call over over system. And the model the model are getting also better at tool calling. They were not so great like a year ago. Now it's getting much better. I see you mentioned two things. First was the GitHub repo. Yes. And then the second thing was the app. Um So, you have the GitHub repo for for MLX Swift LM. That's the the package that will install in your app. And then you need to go to a game face and and getting to get the weight of the model. But for for a normal user, they can just download the app from the app Oh, and yes, if you want to try my app, you can if you want to try it like right now without having anything to install, you can do that. And you can choose any open source model inside that. Uh there is a selection that that they are not it's not any like I'm ensuring that all the model ones correctly on the on the iPhone because not all of them work work well. Thank you very much. >> [music]
