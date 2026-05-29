![Thumbnail](https://i.ytimg.com/vi/KJN5P9xMYIE/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLB6dLU528MGh4GjEZFzyoYu6cGMjQ)

# How To Defend Your Website Against Bad Bots - Experience Report
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2y ago |
| **Type** | Video |
| **Duration** | 8:11 |
| **Views** | 9,445 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=KJN5P9xMYIE&pp=0gcJCQ0LAYcqIYzv) |
| **Category** | - |
| **Language** | - |
---

## Tags

`web dev` `web development` `bots` `three tier architecture` `three-tier-architecture` `CDN` `Content delivery network`
---

## Description

Learn more about intrusion prevention system→ https://ibm.biz/Bdyaqa
What is three-tier architecture? → https://ibm.biz/BdyaqK 

Bots are common place on the internet, but how do you ensure you're not overrun by resource consuming requests from "bad bots." IBM Developer Advocate, Dan Kehn, explains the components and strategy you can add to your classic three-tier architecture to help protect your resources and provide the best experience for your users. So when bad bots come for you, you'll know what to do.

Get started for free on IBM Cloud → https://ibm.biz/sign-up-today
Subscribe to see more videos like this in the future → http://ibm.biz/subscribe-now

Chapters
00:00 What is a "bad bot"?
01:17 Three parts of the solution
01:37 Original three-tier web topology
02:00 New components of the solution
03:30 Web Application Firewall (WAF)
04:20 What is bad behavior?
05:42 Challenging bad behavior
06:51 Caveats

#bot #malware #DDoS #webdevelopment #performance
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
| **Characters** | `7649` |
| **Error** | `none` |


So I was working on a project where we had a performance problem with a website. And we looked at it, and it was really kind of strange because we would see these strange unexplained spikes in traffic, and yet the number of sessions was approximately the same. So we looked at the logs and we realized there wasn't just more users, it was some users were consuming an insane amount of resources. We traced it down to what we were calling "bad bots." And so for this presentation, I want to explain how we fixed this problem and how you could potentially address this same problem. So first, what do I mean by a bad bot? Let's look at the extremes. First we have the "good" bots. Those are the the Googles, the Bings, the DuckDuckGo, etc. Those are ones that don't strain your resources too much. And they also respect the rules of the road, as it were [ed: like valid user agent in HTTP request]. And then we have at the other extreme, which I'm not going to cover in this particular presentation, those that represent a security problem--what I call "evil" bots. And those are bots that are really trying to compromise the admin login or something like that. Those are ones that I'm not going to refer to in this specific one. I'm more interested in the ones that are really badly behaved. In other words, they're demanding more resources and how can you address them. I'm going to cover this in three different parts. The first part is kind of a general protection strategy that you can use for your website. The second, which is directly to this point, is how can you detect bad behavior and what to do about it. And then the third is kind of what you should be aware of with this--some of the caveats for this solution. So first, I understand this diagrams a little bit busy, so work with me on this one. This is a three-tier architecture where you have your web [server] being accessed by different users and bots, which is-- and skipping over just for a moment --accessing your web servers. That goes to an application server and then to your back-end database. That is the original topology. We're going to introduce some new components in this and I'm going to explain them one-by-one, starting from the left and heading over. So from the users, we head over to a proxy, which is a reverse proxy. So what is that? A reverse proxy is your forward-facing sort of interface to the Internet. Normally your web server would be outward facing and that way the users and bots, etc. know the IP addresses of those particular servers. What you do is you put a reverse proxy in front of those and that becomes the public face of it. So why do you do that? Well, there's a couple of different reasons. One is it allows you to filter traffic; so that way, if there's malicious traffic, you can pull that off, or you can also introduce other components very easily, like a CDN, which is a content delivery network. A content delivery network basically is a set of servers located throughout the world which capture the static sort of resources from your web servers, cache them, and then deliver them to users. That takes off some of the load from these back-end servers. While you're there, another handy component is a load balancer. And that allows you to be able to distribute the load to your back-end servers across multiple servers. And so, for example, if it's Black Friday and you've got a lot of traffic you anticipate, you can add additional servers to handle that additional load, and then when the event's over, you can go ahead and decommission them. Okay, so that was the big picture for the beginning of the general protection, where in the proxy we can add filtering to be able to handle some of these potential evil or bad bots. But what I want to really lead to is, is this star of the show, that is a web application firewall (WAF). That is different from a firewall that you might traditionally think of in the Linux sense of having a firewall where you're blocking by IP address or service to your server. A web application firewall is programable, and it has a number of rules. In fact, typically it comes with thousands of predefined rules that can detect this sort of invalid access you want to prevent. But here's the interesting part: You can also program it dynamically and that I could use to detect this bad behavior. So what do I mean by bad behavior? Let's go through several examples to explain what I mean. So if you are looking through your logs and you're seeing accesses, let's say for a user, you might see something where they access the page within a given interval of four pages and then they're going to pause,-- to be able to read that. They might access another page during the next interval and so on. The point being is, is that normal user behavior is: read some pages, take a pause, read some more pages, etc., right? A good bot. What it does is kind of similar to this pattern where it might ask for a page, ask for a page, and then if your server returns an HTTP return code of 429 [Too Many Requests], it pauses. So, for example, you could say 429 [Too Many Requests] HTTP code, you know, let's wait 30 seconds. And it will respect that and thus it will stop requesting pages and then resume. The bad bots, on the other hand, they will request page after page after page, and they will not respect the fact that you've entered a 429. And evil [bot], which I haven't covered in this case, they will request 100 pages, 100 pages--as much as your server can literally withstand to be able to consume that sort of [content] from your pages, and it won't respect that. So if we could detect this particular case, what we do is we install a monitor here. And this monitor will capture the logs from your different web servers looking for this particular pattern. And if it detects what we are calling this "bad bot", one that is not respecting a 429 [Too Many Requests], it can then create a dynamic rule. For example, to block IP traffic for, say, another 30 minutes. That way, typically your bad bots, if they get too many dropped requests, they'll simply move on and you won't have a problem from there. This will smooth out those top spikes and be able to give you much less resource consumption. In fact, in our tests we found that typical bad bot activity reduction was 15 to 45% of your resources. So not only do you save on the amount of resources you're consuming, but your users ultimately get faster performance. Okay, some caveats before I wrap up. First and foremost is this is just **a** solution. There are other ways you can approach the same problem, so I recommend that you iterate on this solution. This is a good starting point. Also, keep in mind that if you're using a reverse proxy, there is some overhead. You can see that I'm jumping from one server to the next. Those additional hops can introduce additional latency that can cause you time that you might not have if you were connecting directly. But it isn't that much-- for a typical [case], on the order of, say, 20 milliseconds. And probably, finally, the most important point is, is keep in mind that if your reverse proxy is being provided by a third party, you really need to be able to trust them. Because that proxy is going to see the IP addresses and HTTP request headers that go all back to your servers. So that means you need to trust that they are going to be responsible about that privacy and also that they are taking security steps to make sure that the data they are capturing is not going to be compromised in some sort of way. Thanks for watching. Before you leave, hey, don't forget to hit like and subscribe!
