![Thumbnail](https://i.ytimg.com/vi/4gC3oueK9Gc/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBhQeOyn7sXQDZbcSsvkxMtAhpY-A)

# Building Trustworthy AI: Avoid Model Drift & Unsafe Outputs
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 5:24 |
| **Views** | 6,818 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=4gC3oueK9Gc) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified Associate Generative AI Engineer? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdGtm4

Learn more about Trustworthy AI here → https://ibm.biz/BdGtmr

What if your AI starts cursing like a sailor after deployment? 🤔 Learn 3 methods to ensure trustworthy AI, prevent model drift, and flag issues like bias or profanity. 🚀 Discover how to validate outputs, monitor for drift, and use filters to keep your AI reliable in production environments. 💻

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdGtms

#ai #machinelearning #aiproduction
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
| **Characters** | `4300` |
| **Error** | `none` |


So if you have AI and it's designed to talk like your basic 10th grader and it starts talking like a two year old, that's not good,. That's a problem. If you have AI and it starts cursing like a sailor after it's deployed and out in the world, that's not a good thing either. So how do you keep that from happening? So today in this video we're going to walk through three different ways that you can keep your AI doing what it's supposed to do. I think before we get into that, I think it's important though to understand what data scientists and AI engineers do. AI engineers and data scientists, we build models, and typically we build these models and what I'll call or what we call the development space, and you can think of our development space as kind of like a sandbox. It's our happy little world where we take inputs, build models, and these models create output. And while we're developing these models, we're very meticulous. We wanna make sure that this output is exactly what we want it to be, right? We don't want it to be, if we want the hey hi to speak like your average 10th grader and the output is speaking like a two-year-old, we're gonna go back and we're gonna fix that. If the model is designed to predict customer churn and it's not, we're gonna go back and fix that. But once we get to a point where we're happy with the model, we think it's wonderful, we put it into production, or we deploy it, we put it out into the world. Typically we'll call this our production space. like the deployment space in production. A model is going to have input and output. So how do we ensure that this model is doing what it's supposed to do? So we have really three different methods. The first is what we call comparing the model output to ground truth, right? So if we've built a model to predict churn, and those predictions are not accurate, like the people we've predicted to cancel their service don't cancel their service, we know there's a problem. So we can compare this output to some sort of ground truth. In the generative world, we can take, like if we have AI that's writing emails, based on some kind of prompt or some kind of stimulus, we can have a human write an email to the same stimulus, and the output coming from the AI in the human based on the same stimulus should be similar. If they're not, we've got an issue and we need to go back and look at our model. But again, in both situations, we're comparing the output of the model to some sort of ground truth. The other thing we can do, remember over here in the development space where the data scientists were very, very rigorous in terms of what their model was doing, we can compare the output in deployment to the output in development. So if we're predicting a model that should be predicting on average a churn rate of 4%, but in development, the average churn rate was like, let's say, .4%, that's an issue, right? What we're seeing in the deployment that is different than what we saw when we developed the model. Likewise, if we built a model to talk like your average 10th grader and all of a sudden it's talking like a two-year-old, that's an issue. And we could tell that by comparing it to the output that was created in the development. We can also compare the input data from production to development. Like if the average age of the data going into our model in development was 25 years and deployment or in production we're noticing that it's 50 years. Whoa, hold on, something could go wrong. We've had a lot, we're feeding a lot older group of people into this model. So comparing it to ground truth, comparing it to the model in development, comparing it to ground truth is sometimes called accuracy. Comparing it to ground truth is sometimes called model drift. The third thing we can do is we can create flags or filters around this output. For example, we can have a PII flag. So if somebody's social security number shows up in this output, this flag is gonna get flagged and we know, okay, we can't send this out into the world. Likewise, if it's hate, abuse, or profanity, HAP, we can identify in this output, flag it, get it out of there. So anyway, those are three ways that you can ensure that your AI is doing what it's supposed to do. I hope this was helpful. Thank you so much.
