![Thumbnail](https://i.ytimg.com/vi/kNl4riqEt-E/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAxqh2wnWXHn7LzCw9zwwfmRRC5fA)

# Moving Data to the Cloud - Experience Report
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2y ago |
| **Type** | Video |
| **Duration** | 5:32 |
| **Views** | 12,565 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=kNl4riqEt-E) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud` `cloudmigration` `databases` `cloud migration`
---

## Description

Migrate to the IBM Cloud :   https://ibm.biz/Move_to_the_IBM_Cloud

Cloud database solutions:  https://ibm.biz/Cloud_Databases

It's tempting to move your data to a cloud-based platform, but where to start? In this experience report, Wes Pretsch explains how his team validated performance as part of their migration of a 1TB+ on-premise database to the cloud. And most importantly, Wes answers the most important question: Was it worth it? [spoiler: absolutely!] 

Get started for free on IBM Cloud → https://ibm.biz/ibm-cloud-sign-up
Subscribe to see more videos like this in the future → http://ibm.biz/subscribe-now

#cloud #cloudmigration #lightboard #ibmcloud
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
| **Characters** | `5135` |
| **Error** | `none` |


So we've all heard of the cloud and have at least heard of cloud migration. But what's really involved? I'm currently on a team that is response for responsible for transferring an on-premise database to the cloud. And this on-prem database is nearly a terabyte in total size. And so this video is an experience report on some of the problems and solutions I've faced. And then some general advice I'd give for teams in the future. And this experience I'm going to talk about is really a small timeline compared to the overall grand scheme of things with the entire project. But before we dive into that, let's first answer "Why?" Why the cloud? Well, one cloud is cool and IBM's going all-in on cloud technology. But more specifically, we really like cloud for its disaster recovery and for its scalability features. And so this brings us to today's presentation. For this experience, I was on a team responsible for performance testing each kind of database to make sure scientifically that switching to the cloud is actually better for our team and for our product. And so there's three major problems that we had to work through. First, how are we going to test the cloud? Next, what kind of metrics help us prove performance quality? And third, how do we get these metrics results and present them properly? So first, testing. How do we test the cloud? Well, my team set up a cloud environment and we created a test instance of the database by copying over a big chunk of the tables and filling those tables with auto-generated data. This way, we don't have to lift and shift the entire database to the cloud, realize it doesn't work when we are testing it, and then now we're all sad because of all that wasted effort. This way we have two instances of the database in both environments and we can send queries to both of them and then emulate the performance that we're going to get when we eventually do switch over the database to the cloud. So we have our testing set up. Now, metrics. What kind of metrics help us prove performance quality? Well, after a good amount of discussion, my team narrowed it down to five major things: CPU usage, memory usage, disk IO, latency and lock waits. This will give us a good overall foundation and enough information to make a rational decision about the move. Next, results. How do we get these metrics results and present them properly? Well, this problem out of the three was the most intensive and my work specifically dealt with creating the test suite that would be used to stress the databases. The test suite I created had thousands of queries and each of the four different CRUD operations, and then the rest of my team set up a monitoring system and a metrics query to run in parallel with the CRUD operations. So, while the CRUD operations are stressing the databases, we're getting all of the metrics that we need. Setting this test suite up gave us a lot of fun problems we had to deal with. Everything from those pesky SQL errors that give you no explanation on what's wrong or how to fix them to realizing that our log files were overwriting themselves mid-test. Luckily, my team is filled with a bunch of rock stars, so we powered through and figured it out. Once we finished our performance testing and gathered the metrics, we created a series of Python scripts to parse through the information, compile the outputs and generate visualizations. This way it was really easy for our management and execs to read. And lo and behold, the cloud was faster. And a lot faster. Especially with the CPU, memory, and disk IO, it blew on-prem out of the water. Now, I know cloud migration is a very lucrative process with a lot of moving parts, and so some general advice I'd give for the teams in the future are to communicate thoroughly. And to plan extra time. Starting off with communication. Now as a junior Dev, this is the first time I've done anything sort of cloud migration related, let alone something to this scale. So there's a lot of times I felt like I didn't really see the big picture and I kind of felt out of the loop. And so I had to meet with my leads and the rest of my team a lot just to talk about the work we've completed and the work we still need to do and where we're going. So for teams in the future, I highly recommend that you be consistent in making sure that everyone's on the same page, even if it may seem a little redundant. Next, always plan extra time. There's always going to be those fun problems that come up that you just can't plan for. And so especially if you're committing to a specific deadline, be sure to give yourself that extra wiggle room to give enough time to work through those problems. And I know that this advice is super generic and can be applied to literally any kind of project, but nonetheless, it applies here with cloud migration. So if you're going to take away anything from this video, know that, one: cloud is really that cool. And although this can be a really daunting process, it's worth the effort and you should check it out. Thanks for watching. If you like this video, be sure to hit like and subscribe.
