![Thumbnail](https://i.ytimg.com/vi/OejCJL2EC3k/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLABH4KhcwSTZYC-hXPD59XVI3NAHg)

# What is MLOps?
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 3y ago |
| **Type** | Video |
| **Duration** | 6:55 |
| **Views** | 151,244 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=OejCJL2EC3k) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud` `MLOps` `DevOps` `watsonx` `AI` `Artificial Intelligence` `ML` `MachineLearning` `Machine Learning`
---

## Description

Check out watsonx: https://ibm.biz/BdvDnH

It takes a lot of time, effort, and money to train a machine learning model. And yet a majority of models that are trained and developed never actually make it to production. What can be done to lower the cost and frustration of ML model development? Automation! Otherwise known as MLOps, it's modeled after the same practices as devOps that have led to faster code development at lower cost. In this video, David Adeyemi explains what got us here and where to go next.

#mlops #ai #watsonx #devops #machinelearning
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
| **Characters** | `6619` |
| **Error** | `none` |


Have you ever been training a model only to find that it never reaches production? Well, 68 to 80% of models that are trained and developed never actually make it to production. Well, I'd like to introduce something that will make training a whole lot easier for you and your team and make deployments much easier and will have much less stress. And to illustrate that, actually, I have a story to give some context. So my team was on a crunch time with a project with getting a model out. And so we finally got the department to approve a GPU server for us to be able to use some of these larger language models like Bert and Roberta and things like that. So we got on there, we started doing our work. We went as fast as we could to put our notebooks on there. We're getting some good results. We started getting some pretty good accuracy, and we continue developing until one day we try to SSH to the server and we can't. So only to find out that our department only paid for one month on the GPU server. So what happened to all the notebooks, all the data, all the features that we prepared on the server? Completely gone. And so maybe a moment of silence for all the notebooks that I lost in that. But that pretty much reflects what a lot of manual processes-- what a lot of manual training processes, I mean, look like right now. So, first of all, you're usually starting out with EDA, and EDA is just exploratory data analysis. Can we get the data that we need to make this model a success? So you're looking at, you know, getting it from SQL databases or from different teams that can give you an export, but somehow your gathering all this data. Once you get the data, you know that the data is not ready. The data has to be prepped. And so you're looking at some time with data prep and working in some of the gaps and seeing if anything needs to be cleaned. And from there you might move to feature engineering that might which might still be within the same process, at the same time, you're doing your data prep and you're creating, you're transforming some of these columns and you're turning them into new features that will help your model. Well, once you have the features, you're ready to train. And so training is usually the next step. Training is its own process, it's its own task because you have to look into different models. You have to look and see which one is going to give you the best accuracy, which one is most applicable to your problem. Is it NLP, is it a regression? That type of thing. And the training starts once you get some good models. You also have to do the a hybrid parameter optimization depending on the model. From there, you're ready for deployment. And deployment can be its own can of worms because it's either using some sort of API or try to integrate with a front end or back end. And if you're a small team like my own, you might be the people writing both the front end and the training - so you're doing all of that. And then finally be ready for monitoring and looking at how this is performing. It's up on deployment server however you decided to do your end point and you just want to look and see if this accuracy is good enough for the business. But what'll happen is, you know, entropy-- eventually your model is not gonna be as accurate as it needs to be. And so this process, this whole process starts again. Or your team is tasked with a new model. But all of that is manual and really adds a lot of headache. Only for, only 60 to 80%. Only 20% - 40 to 20% of them actually making it to production. That's a whole lot of work. And I'm here to show you a different and better way. So MLOps, as you can tell from the name, implements DevOps principles, DevOps tools and DevOps practices into the machine learning workflow. And so the beginning of DevOps in the beginning of really any development project is you're going to start out with the dev and the EDA work. All of that, at the end of the day, is code, right? You're writing a notebook, you're writing some sort of Python script or some R script or Julia or something like that. But all of that is code and you can put all of that code in a source code repository. And what that does, is it opens us up for the automation that's going to come next. So we can actually go in two directions from our Dev and EDA. We can, first of all, the deployment - if that's an API that you're writing or a front end or something like that... the deployment can have CI and CD tools applied to those commits that you're putting into your repository. On the on the other side - your training can also take benefit from CI and CD. And I'm repeating those terms, but what the what that means is continuous integration and continuous deployment, which just means that every time you make a commit on your repositories, automatically you can build and automatically you can you can deploy your deployments or automatically you can push a model to start being trained. Usually if you have the resources, you're going to want to separate your training infrastructure from your deployment infrastructure. And that's because they're doing different tasks. Training, usually going to want a GPU, some sort of highly parallel computation. And on deployment, you might be fine with spinning up Docker containers or something, little containers that might have a load balancer to just handle demand. But from there, both of these can benefit from monitoring. So in DevOps, there's naturally a monitoring tool just to make sure deployments are still live, just to make sure your rollouts are happening. And you can also see how A/B tests are doing and things like that. We can apply the same ideas to your model. How is your model accuracy? Are there things, or maybe trigger, let's say you reach 80% accuracy, which is which is too low, what you can do from that is automatically trigger a new training process and you'll take the code, it'll begin the new training on new data and using CI/CD and using automation, you can get a new model up on the production server without too much hassle. So just imagine how much stress is gone from doing this manually to going to this automated MLOps type of pipeline. I hope this helps and I hope that you'll be able to see better accuracies and much more speed whenever you're training your models. Thank you. Thanks so much. If you like this video and you want to see more like it, please like and subscribe. And my department said, if we reach 10,000 likes, they're going to pay for another month on the GPU server. If you have any questions, please drop them in the comments below.
