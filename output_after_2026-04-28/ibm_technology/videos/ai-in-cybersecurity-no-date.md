![Thumbnail](https://i.ytimg.com/vi/4QzBdeUQ0Dc/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAPXTf1I70dsVLVRZLUah-jlSUmHQ)

# AI in Cybersecurity
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 3y ago |
| **Type** | Video |
| **Duration** | 6:18 |
| **Views** | 182,671 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=4QzBdeUQ0Dc) |
| **Category** | - |
| **Language** | - |
---

## Tags

`qradar` `xdr` `edr` `ai` `artificial intelligence` `cyber security` `cybersecurity` `it security`
---

## Description

IBM Security QRadar EDR: https://ibm.biz/QRadar_page
Threat Intelligence report '23: https://ibm.biz/BdPCWC
Check out the AI and Cybersecurity eBook → https://ibm.biz/BdSkcA

Cybersecurity professionals are in short supply. How can companies boost the efficiency of their existing cybersecurity staff? In this video, Jeff "the security guy" explains how AI can act as a force multiplier that help you address security threats more effectively.

Get started for free on IBM Cloud → https://ibm.biz/ibm-cloud-sign-up
Subscribe to see more videos like this in the future → http://ibm.biz/subscribe-now

#AI #Software #ITModernization #Qradar #JeffCrume
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
| **Characters** | `5645` |
| **Error** | `none` |


Right now there are hundreds of thousands of jobs open in the cybersecurity space. And we can't fill those positions fast enough and we can't make experts fast enough to fill them either. So what are we going to do? With the people we have, we're going to have to use force multipliers in order to be more effective and meet the need. And two of the things that we can do for force multipliers is we can use automation. That allows us to work more efficiently, or we can use artificial intelligence--that allows us to work more intelligently. I'm going to specifically focus on this one in the video today--to talk about how we can use AI to investigate a problem, to identify an issue, to report on a particular problem, and ultimately to research and find out more about a particular problem. So let's start with this first one: investigate. How could we use AI to investigate a particular issue, if we become aware that there might be an issue? Well, we can use a construct called a knowledge graph, which is a way of representing information about the physical or logical world, but representing it as a data structure. And the way this works is--to give you an example. Let's say we have a domain. And this would be like the name of a web domain. And that domain then resolves to a particular IP address. Also we--so this is what we normally have with a website. Now, what else do we have? Well, we might also have a URL. That's the actual link that you're going to type into your browser. And that is going to link to a particular file on the file system. Now, let's take, for instance, if that file on the file system ends up pointing-- because we know through an AV signature, an antivirus signature --what if this points to malware? Then this is some information that we can now connect together. Then, if we say that this URL is in fact contained by that domain, and then I add a user out here unsuspecting--who connects then to this IP address. Then, all of a sudden I have a path that goes all the way through from this user to this malware. And now I have this data structure that has represented, in fact, the connection that occurred. I now know this user has been infected by this malware, and here's the path it took to get there. And in fact, if this knowledge graph is good enough, I'll be able to look and see what other users might also be affected and what other malware and what other sites. So this is a way of representing information and then we can do some reasoning over that in order to do inference. Now, this is how an AI system might do this internally. Now, so that's one way we could do investigation. How about to identify in more detail a particular problem? So systems will typically write out lots of log records. Once an event occurs on a system, then we cut a log record. We put out information about--here's the time, the date, here's who did it. Here's what they did, here's the system they did it to. Here's where they did it from. Those kinds of bits of information would be contained in these log records. And we have loads and loads of these. So it's very difficult to sort through all of that and find where are the anomalous activities. Where are the outliers? Well, in particular, what we'll find is, in this case, let's go with an example and say here is a record where a privileged user logged into the system and created a new account. Then, almost immediately afterward, in almost no time, they copied all the contents of a database. And then, almost directly immediately, they deleted the account. Now, each one of these activities independently wouldn't represent necessarily a problem, but if you do all of these within a very short period of time, then we could use a time decay function and something like machine learning, which is essentially pattern matching on steroids, to look at all of these things and look at multiple factors across multiple records and realize we have an outlier, we have an anomaly. We have what may be an attack scenario where an insider has taken advantage of the system. So that's another use of AI and machine learning, in particular, in order to diagnose a problem. What else could we do? Well, we could report. There's a requirement in security circles that you report against: Are you complying with regulatory requirements or not? And some of the things that we might do in those cases is gather the log records and process those. We might also use information that we've gained here to enrich our reporting data. So that's another example where enriching the report with the information we have from the AI system, and that's also allowing us to report, we're spending less time. And then finally, to do research. Imagine I'm investigating, I'm identifying, I'm doing all these kinds of things. And what I'd like to be able to do is find out, what is this bit of malware? And I'd like to know more about it. I want to know more about any of these systems. So it would be nice if I had a natural language processing system--a chatbot that I could go and talk to and ask it questions and it has a knowledge base that it draws on. So, in fact, we're going to see more and more of this kind of capability going forward where a chatbot becomes essentially another member of the staff to answer questions as we're trying to do investigations. So you can see now, AI can help us a lot in the cybersecurity space. And that's in fact why IBM, 100% of our security software products include AI. Thanks for watching. If you found this video interesting and would like to learn more about cybersecurity, please remember to hit like and subscribe to this channel.
