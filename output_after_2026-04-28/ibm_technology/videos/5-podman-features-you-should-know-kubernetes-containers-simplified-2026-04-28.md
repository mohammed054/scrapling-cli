![Thumbnail](https://i.ytimg.com/vi/dEy3pQKhE8k/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLBw4ObpktgSwcv6wbpX64spJkXy3Q)

# 5 Podman Features You Should Know: Kubernetes & Containers Simplified
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2026-04-28 |
| **Type** | Video |
| **Duration** | 9:23 |
| **Views** | 6,815 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 0 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=dEy3pQKhE8k) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified Developer - App Connect Enterprise? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdpiZs

Learn more about Containers here → https://ibm.biz/BdpiZi

Podman runs rootless containers! 🚀 Cedric Clyburn shares 5 game-changing Podman features, from simplifying Kubernetes workflows to deploying bootable containers. Learn how Podman transforms container management for developers and DevOps teams with these powerful tools!

Sign up for a monthly newsletter for Cloud updates from IBM → https://ibm.biz/BdpiZj

#podman #containers #kubernetes
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
| **Characters** | `9017` |
| **Error** | `none` |


I can almost guarantee that you've heard about containers. Containers are really cool and unique technology that allow us to take our application, including the source code, whether it's written in Python or Java or whatever you use, along with its dependencies, its configuration, everything that I need for it to run, and package it up into one unit, being a container image, and then give that to you to share to my team and deploy across the hybrid cloud. So, containers are really cool, but the thing is, a lot of people associate containers with Docker. And the thing, is there's an open-source alternative that's called Podman, and Podman is really cool. Firstly, when we run Podman and we spawn in new containers, well, there's no background daemon system that's running in the background. Also, at the same time when we spawn these containers and start them on our machine, we're rootless by default, which is really cool. And then finally, Podman's been trusted by enterprises and organizations for over 10 years. So, Podman is quite cool. And I want to talk about five new features that have been coming out with the Podman team and community that are quite interesting if you're an application developer, if you work in DevOps, or if you're just someone who likes working with technology. So, let's get started with five new features about Podman, beginning with Podman Desktop. So. Let's think about the life of a developer or an engineer, right? You're probably frequently running and working with containers, having to SSH and debug things, or maybe you're building custom unique container images for your applications or your workloads, and maybe you are taking those and deploying them to some type of orchestrator. For example, Kubernetes is one of the most popular. Now, there's a lot of tools that you need in order to do this. So, for example, you need that container engine, so that would be, in our case, Podman, to set that up. You would need something like kubectl to set up a local Kubernetes environment to test things in your inner loop of development. And also, for example, use additional things like minikube in order to set up that environment. So, we're working with a lot of tools, a lot of dependencies in order to start working with containers and move those applications to Kubernetes. Now, what's really incredible is that the team working on Podman has released Podman Desktop, which is an open-source and cross-platform application and interface, in order to manage all of these components in one place. So for example, I can open Podman Desktop to view the logs and SSH into my application, start debugging there. Or I can also get the manifest in a file to understand, hey, what's happening with this application, and build those images and also deploy them to a registry or spin up a local Kubernetes environment with Kind or minikube and deploy those applications there too. And so this is really cool because we have a customizable interface that makes things really easy. Plus, if you're forgetful like me, you don't need to memorize the command line in order to set up things like port mappings and persistent volumes, that type of thing. Now, Kubernetes is just one way to manage containers on a system. And perhaps one of the most powerful pop-in features is being able to run containers as system services using SystemD. Now this is really cool because if you do the command Podman generate, and then SystemD for whatever pod or container that we're currently running, you're automatically generated a declarative file that allows you to have restart policies, health monitoring and more, which is perfect for a production or home lab setup where you have a container that needs to run for a long time. You get the same ephemeral benefits as containers, but it's now tightly integrated into the system itself. So, let's talk about what these look like. Well, we're gonna have our unit files, which is going to describe a little bit about what's happening, or say, for example, when the machine boots, we can have a dependency, for example. Or after something happens, then we can have that action in the SystemD file as well. Maybe wait for access to a network or something like that or set a timer. And then the container file of the section allows us to describe which image that we want to run. And so we could have our, you know, container image here, any restart policies that we wanna have. And then now this entire SystemD unit file will be managed by the host and by system controls so that we can start and stop this file, which is managing the containers for us on boot. So that's another really cool feature of Podman itself. Let's say, though, that you are deploying to Kubernetes, as it's one of the de facto ways in order to deploy your containers across the hybrid cloud. So, Kubernetes is an open-source project that's been around for quite some time, along with Podman and Docker, as an orchestrator. And if you run the command Podman Kube, or Kubernetes, generate, well, it's going to output you various types of files, depending on what you need, all with Kubernetes YAML. So, perhaps it's a deployment of your application. So you can just then use kubectl apply, or even Podman Desktop to apply this container in a deployment spec already for you. Or maybe it's just a pod. Or, say for example, it's a volume. All of this can be generated by Podman, even services as well, so that you can go essentially from your container, develop that locally, export that Kubernetes manifest in a file just like this, and then either deploy this using your command line, upload it to wherever you're hosting your applications, to use that Kubernetes YAML directly from your local machine but now be able to deploy that onto your environment in the cluster that you're using as well. But let's talk about that inner loop of development, right, where, as a developer, we're building out new features, right, implementing code and then, hopefully, we're doing proper testing on that before we go to deploy that, perhaps, on a Kubernetes cluster, as I just mentioned. Now, a lot of developers are being told, hey, you should implement this AI feature, whether it's RAG or agentic AI. The thing is, how do you start implementing that AI capability? Well, whether it's a Python or Java application, you can use the Podman AI Lab. So this is an extension with Podman Desktop that allows you to run models as an AI API. So, you have essentially an inference server, so you have Llama C++ that's running an Apache 2.0 license model. And this AI API allows us, as I finish this up, to make requests from our application using just typical REST request or maybe LangChain integration in our application, then get those responses back so that we can build out those AI features without having to have any third-party dependencies or make a request to a third-party model because even the AI model is running in a container alongside all of our existing applications. So that, my friends, is the Podman AI Lab. Perhaps the last and coolest feature of Podman is the support for bootable containers. Now, let me introduce this to you. So, imagine your container file here, right? This is how we define how we want our application and its dependencies to be packaged. But what if we could take the same container file and deploy an entire operating system with it? So, let's say we go ahead and build this container file. Well, we work from a specific base image that includes the entire Linux kernel and other you know, drivers, dependencies that we need in order to build an image that can then be deployed to a variety of different environments. So this is the deployment of a bootable container which could go to a number of different locations. So, maybe it's a cloud, so it's .ami or maybe it is a virtual machine that we want to deploy our operating system and its applications onto, right? Or maybe it something like IoT devices. But whether it's QCOW2 or an AMI or .raw, we have the operat ..., the ability, sorry, to deploy this image as a full operating system. And then when we need to make changes, check this out, we then just update to the registry. So the registry being over here as the storage for our images. And so we just download the specific layers of the container that we need to update the entire OS. So, it's a really cool concept known as bootable containers. I highly recommend that you check it out if you have a second, another open-source project that is really cool too. So, Podman does a lot more than just containers, and I think it's the easiest tool to get them running on your system. Plus, with deployment options for Kubernetes and creation of disk images like this, you can have more predictability and peace of mind going from local development to production environments. Now, if you learned something today, be sure to like the video and to hack the algorithm. And make sure you subscribe for more content around open source and AI.
