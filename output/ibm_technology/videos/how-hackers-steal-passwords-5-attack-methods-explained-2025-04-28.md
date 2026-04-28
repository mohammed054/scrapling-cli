![Thumbnail](https://i.ytimg.com/vi/vKPGZHoHX8k/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLB6rEXK6y_lHTBvUTZ0ogVsPgm_bA)

# How Hackers Steal Passwords: 5 Attack Methods Explained
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2025-04-28 |
| **Type** | Video |
| **Duration** | 13:07 |
| **Views** | 1,603,637 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,670,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=vKPGZHoHX8k) |
| **Category** | - |
| **Language** | - |
---

## Score

| Component | Raw | Normalized |
|-----------|-----|------------|
| Views | 1,603,637 | `1.0000` |
| Likes | 0 | `0.0000` |
| Comments | 0 | `0.0000` |
| Engagement rate | `0.000000` | `0.0000` |
| **Final score** | | **`0.183940`** |

> Ranked by: **weighted**
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Want to uncover the latest insights on ransomware, dark web threats, and AI risks? Read the 2024 Threat Intelligence Index → https://ibm.biz/BdnicA

Learn more about a Brute Force Attack here → https://ibm.biz/Bdnicu

🔐 How do hackers steal passwords? Jeff Crume breaks down five attack methods—guessing, harvesting, cracking, spraying, and stuffing—and shares tips to prevent credential theft. Discover strategies like multi-factor authentication, passkeys, and rate limiting to secure your systems today! 🛡️💡

Read the Cost of a Data Breach report  → https://ibm.biz/BdnicL

#cybersecurity #hackers #cyberthreats
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
| **Characters** | `12871` |
| **Error** | `none` |


Have you ever wondered how a bad guy hacks your password? It's a big problem. In fact, according to both IBM's Cost of a Data Breach Report and the X-Force Threat Intelligence Index, stolen, misused, or otherwise compromised credentials are the number one attack type. There are lots of ways this is done, but in this video, I'm gonna focus on five different approaches they use. Guessing, harvesting, cracking, spraying, and stuffing, and don't worry that I'm giving away any secrets because the bad guys already know this stuff. My purpose is to arm the good guys with this knowledge and provide some tips at the end on what you can do to prevent this from happening to you. Let's start first with password guessing. So here we have a bad guy who's gonna try to hack into this system and he's gonna posit some particular guess into the system. Well, what is he gonna base that guess on? Well, it might just be out of his imagination. It might be just a knowledge about the individual who this system. It could be because he walked by where their laptop was and saw a yellow sticky on the system. We refer to these things as the PC sunflower because people collect a lot of those around their systems and just reads a password off of that. So a lot different ways they could base this. And one other possibility is they use a password database. That is when systems have been cracked in the past, sometimes we get to find out what all those passwords were in the password database in the clear. And those are made available publicly on the Internet, and attackers can use that. So anything the attacker can do to make a more intelligent guess, those would be the different items that they would consider. Well, if it's a guessing attack, they're then going to try to log in. And if they're wrong, okay, then they try again. And if there wrong again, in most systems, you get three strikes and you're out. So, that's the problem and that's reason, by the way. That those three strikes policies are in place. So someone can't just keep guessing over and over and again. So usually he's gonna get three guesses and then the account will be locked out. So unless this is a really good guess, that's probably not a very effective way to do things. Now, another approach would be harvesting. This is where the attacker is going to actually know what the password is and it's not a guess. In a harvesting attack, and there's numbers of different ways this could occur, but one is they install some sort of malware on this system. That malware we call a keylogger. And everything that's typed on this system then is sent to this guy. It's either stored locally and then later he retrieves it or it's sent in real time. But that keyloger or an information stealer, info stealer or whatever you want to call it is something that's recording everything they type including passwords. So that could be fed directly into this guy and he knows exactly what to enter. So obviously we need to keep this system clean. So that it doesn't have that kind of a malware on it. Another thing that could happen is through a phishing attack where this user is convinced to log in to some particular website and then the website is a fake, they think it's a real one and they type in their credentials there and then those flow here. In either of these cases, the bad guy has just harvested the information and can now log in directly. Okay, now let's take a look at another technique We call it cracking. In password cracking, what the attacker is going to do is start with a database of stored passwords. Maybe he logs into the system, hacks into a system, and pulls out that database where all the passwords are stored, and he extracts those. But here's the thing. Assuming they did a decent job of security, these passwords are hashed. That is, using a special one-way encryption technique that cannot be reversed. So they're not readable. In any normal sense, and there are going to be a number of these hashed passwords that now the attacker has available to them, but in and of themselves in the hashed form they're no use. So what can he do in order to reverse what is an irreversible encryption? Well, you can't, but you can back your way into discovering what the original password was. And the way that gets done is you start with, again, a different type of guess. What you would do maybe is take one of these databases of publicly known available common passwords, or you could use a password dictionary. Those are also available on the internet. So you can find a lot of different ways, use it in worst case, you start doing a brute force where you try every single possible password combination, but you use some source to pull out a clear text password that you can read and you hash it in the same way these passwords are hashed. Then you just do a comparison and say is this equal? Well if it's not then I move on. Is it equal? And then if it is, then I didn't have to know what the original password was. I didn' have to break the encryption. What I did was I figured out what my guess was and I knew that it matched so therefore I know I have found the right password. That's a way of cracking a password. Our fourth type of technique... Is called password spraying. And in password spraying, again, we need to start off with an attempt, a guess. Now again, we could get this, maybe from this publicly available information, it could be a lot of other sources, but we're gonna start off with a guess and what we're going to do is across a particular system, there will be multiple accounts. So we have account one, account two, and so forth. So all the way down to account N. So lots of accounts on this system. And what we're gonna do is we're going to take that password that we have as a guess, and we're to try it here and see if it works. And if it does, of course we're in. If it doesn't, try it down here. Then try it done here. Try it for all of these. That's why it's called spraying, because we're spraying it across all of the different accounts within a particular system. And the attacker, think about from their perspective, they don't necessarily need to get into account two or account one. Their goal is just to get into anything. So they'll take any password and try it across all of these and until they finally get a hit. And why does this work? Well, because people tend to use the same passwords again and again. So something that is in this publicly available database that was based on a previous breach, probably someone, if it's a common password, someone has used that password on this system as well. So it's good place to start with guessing. And, in that guessing, again ... The advantage to spring is it avoids the three strikes penalty. We're only doing one attempt. If it doesn't work, we move on to the next account. Then we move onto the next count and the next to count and so forth. So that way, if unless someone is really looking hard, they're not gonna even know that they're under attack because it flies slow and low below the radar. A similar type of attack is credential stuffing, which is the same kind of idea. It's just a variation on a theme. In this case, we're gonna take our password guess and we're going to try it across not multiple accounts, but multiple systems. So I'll try it a across a particular, if this is system one, and then system two, system N, I'm gonna try this on this particular system. And if it works, again, I mean, if it doesn't, I move on, and I move on. That's what the attacker is going to do in this case. Now again, very similar to spraying, but notice the difference is, these are across different systems. This is across a single system. So same concept. This one is even harder to detect because probably the person that is responsible for security on this system may not be the same one that's responsible on this system. So they may not able to monitor and look across all of these. So here again, we're leveraging these well-known bad passwords. And guessing across these systems. Okay, now we've taken a look at five different types. There are other ways as well, but at least we've taking a look these. Now, what can you do to prevent this from happening? How can you keep from being a victim? Well, there are three things that we do in cybersecurity. We do prevention, detection and response. So let's first take a look at some things you can do for prevention. So one of the prevention things we can do is test password strength. So when someone types a password into your system, you ought to be able to test and see if it's got the right level of complexity to it. Don't make it too complex because then people just have to go write it down. But some level of complexity and length, and by the way, length is strength when it comes to passwords. So longer is probably even better than complexity. Also check it against a database like we've talked about before, of these known passwords, known vulnerable passwords, and make sure it doesn't match any of those. If you can, test and see that someone is using a different password across multiple systems. So there are a lot of things you can do there. And to that last point, something you can to encourage people to use multiple passwords and complex long passwords is to use a password manager or a password vault. Some sort of secrets management system, if you're looking at this on an enterprise level or a Password Manager, if you are talking about it on a personal level. Here, the system can generate strong passwords for you and keep track of all of those for you. Also make sure it will encourage you that you're less likely to use the same password across multiple systems, therefore reducing your attack surface. Another thing is to use multi-factor authentication. Don't rely just on a password. Look for other things, not just something you know, something you are, something you have. So maybe a message to your phone or a biometric like a face ID or something along those lines. What's the best way to not get your password stolen though? Don't have one. Don't have a password. Get rid of passwords and go with passkeys. Sounds like the same sort of word, but it's a lot different. The solution is a lot stronger. It's based on cryptographic techniques. I won't get into the details of it, but if you have an option to choose pass keys, do it. And then the last one I'll mention in terms of prevention is rate limiting. We want to make sure that someone isn't able to just flood our system with tons and tons of password logins. You want to baseline. And understand what is a normal level of traffic for people trying to log in, and don't accept if all of a sudden you have just a burst of login attempts that don't make any sense. Okay, then moving to detection, what can we do there? Well, I'd like to look for a couple of different situations based upon spraying and credential stuffing. One is multiple failures over time. I wanna see if I'm seeing an increase in the number of failures over a given interval of time. Now if an attacker is really smart they'll spread this out over a really long time, but if they're not then you might just suddenly see a whole bunch of attack attempts and you would want to flag that and then take some action, which we'll talk about in a second, also another thing you could be looking for is multiple failures over the account space. So on a particular system you will be looking four did i have a failure on one account then another account then another account, another account. That would be a sure fire sign that we're looking at a password spraying attack, by the way patent pending on that one. so stay tuned, Now let's move on the response side. what could you do on this once you've discovered that you're under attack what should you be doing? Well one of the things you want to do is block suspicious IPs, ip addresses, because you know if you're seeing tons of logins from one place all at one time that's probably a bad actor. So let's just block that IP. Disable compromised accounts is another. Once we know that an attack has occurred, we should go back and look and see if maybe that one password that was attempted across lots of different ones and then suddenly worked on one. Okay, that was a spraying attack and the one that got logged into is probably suspicious at this point. So maybe we want to block that until we can do an investigation, and then ultimately, if we know an account has been compromised, we lock it out, we force a password change. So that way the attacker can't use the information that they already have to get into the system. So there you have it, lots of ways for attackers to get in and lots of way for you to keep them from doing it. Do these things and you'll make life a lot harder for the bad guys and that's how we want it to be
