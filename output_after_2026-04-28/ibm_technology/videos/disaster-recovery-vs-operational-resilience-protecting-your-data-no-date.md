![Thumbnail](https://i.ytimg.com/vi/kr6fc869Ugs/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLC4UF0lgmx9jiSab_rDYJyfgs1jtQ)

# Disaster Recovery vs Operational Resilience: Protecting Your Data
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 7:24 |
| **Views** | 6,502 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=kr6fc869Ugs) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified Administrator - Cloud Pak for Security? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdGNQD

Learn more about Disaster Recovery here → https://ibm.biz/BdGNQR

Tornadoes hit your data center, but what if ransomware infects your backups? 🌪️💻 Grant Harris explains disaster recovery vs operational resilience, showing how to protect against natural disasters and cyberattacks. Learn strategies like ransomware-proof backups and rapid recovery. 🚀

Read the Cost of a Data Breach report  → https://ibm.biz/BdGNQF

#disasterrecovery #datasecurity #cyberresilience
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
| **Characters** | `6387` |
| **Error** | `none` |


Today, we are talking about tornadoes, earthquakes, floods, and black hat hackers. Now, why are we talking about these things? Well, we have disaster recovery and operational resilience as two kind of pillars of frameworks that people have when they're thinking about protecting their data. Now, the traditional column is disaster recovery. And like I was saying, this is your tornadoes, this is your floods, this is, you know, all the things that are natural disasters that can wreak havoc on a data center, or have a power outage, things like that, that are, you know, the bread and butter of what most people have had their DR plans focused around since data centers became a thing. Now on the other side is operational resilience. So this is taking disaster recovery and adding in the ever-growing and extremely present threat. of our favorite people, these black hat actors. Now, these folks are different from tornadoes, different from hurricanes, even though they are considered damage creators, they have a brain. And as opposed to these natural disasters who just roll in, destroy what they're gonna destroy, and then they're out, this person can be living in your system for weeks, months, maybe years, trying to entangle themselves in your systems so much so that when you get hit with a ransomware email saying that you've been attacked, you have no way of recovering your data effectively unless you have operational resilience as the goal that you're trying to achieve. So, the scope of these two, well tornadoes affect just one place at a time and they come and go. So we'll call this local. Now, on the other side of things, we'll call this global because these folks can live anywhere. I mean, a lot of times ransomware attacks will hit the United States from Russia, China, all over the world. Now these also can be broken down into state actors and just kind of ransomware groups, and the state actors kind of play a different game than the ransomware organizations in that they are in it for just widespread destruction of your data. The ransomware folks, they want money. Sometimes people pay the ransom and they get their data back. Not the best idea because there's caveats to that, obviously, but if you're dealing with a nation state attacking you, it's not gonna end up good. Your data's gonna be destroyed, so you need to be extra prepared for that. Now, the other part of it is backups. Everybody says, okay, I got hit. Well, I'll just recover from my backups. Well, in a disaster recovery paradigm where a flood hits you, that's completely fine. Now, yeah, backups affected, no, let's say no to that. This is a big yes on this side, because you can imagine if you were a smart hacker, you would have in your mind the thought of, okay, I wanna do as much damage as I can do before and kind of make myself sticky in their system before I announce myself. And that often is the way that people know that they've been affected. So they will come into your backups, affect your backups with infections and they will then hit your production, and once they hit production, a lot of people will just trigger their backup to recover in, and then they're in for an even worse nightmare than they already were in. So, local, global. Backups affected, no. Backups affected, very much so, and it's almost the cornerstone of their strategy. Now, the recovery objectives also are important with this. Once again, much more simple on this side, you have an RPO and an RTO. basically the SLAs for how you want your organization to be able to recover from these natural disasters. Now, this also applies over here. So RPO, RTO are perfectly appropriate to apply to this side, but you need the combination of these things plus immutable snapshots, because since this is a thinking actor, they can get into your backups and they want to get into your backups, and you need to make sure that not only can they not change anything, they shouldn't be able to see your backups. This should be a, instead of a worm, this should be more of like a warn. Read once, write once, read never, unless you're the right person. So RPO and RTO is all good, but if you don't have a known good copy to recover from, it's kind of a moot point because you just keep on reinfecting yourself and you're back to square one. So duration is another thing. This is, you know, the floods will recede and you'll kind of be left with the damage, and this is basically maybe hours to days. On the other side of this, this is very dependent on how prepared you are for the event. Now the industry average on recovering, once you know that you've been infected, is 23 days. That's getting close to a month, so let's call this months slash months. This is so important to understand because you have a real ability to control this with how well you have prepared for this contingency of a threat actor getting into your system. If you have your infrastructure set up in a way that is able to detect quickly and also recover quickly that known good copy, you can shrink this month down to a day, a shift, however you like to call it. It all is in how prepared you are. Now the last piece for these two columns to distinguish them is likelihood. Now, everybody has a DR plan. It's important to note that not everybody tests their DR plan, which is important, but everybody has a DR plan. Now, the likelihood that a tornado's gonna hit your data center, even though tornadoes happen every year, it's still very low. So, low odds that this is gonna be happening to your organization specifically, but everyone's prepared for it. On the other side, This is a very high likelihood because threat actors are constantly trying to penetrate as many systems as they can to either wreak havoc, so political discord, or make some money most likely. Now this is the one everyone's prepared for. This is the one that people don't really realize that being ready for this side does not make you immediately ready for this side. So big impact more likely to happen bad guys thinking about the worst ways they can affect you versus very predictable things that you can plan on. So while you wanna have disaster recovery as the foundation of your planning, you really wanna extend that over to be truly operationally resilient, which allows you to handle all the tornadoes, but also handle all these bad guys in the black hats.
