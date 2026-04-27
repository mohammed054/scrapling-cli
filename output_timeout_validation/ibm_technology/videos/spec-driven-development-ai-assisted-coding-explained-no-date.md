![Thumbnail](https://i.ytimg.com/vi/mViFYTwWvcM/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLAuqYTTIHe20IXpMmy--g7tDm3JRQ)

# Spec-Driven Development: AI Assisted Coding Explained
---

## Info

| Field | Value |
|-------|-------|
| **Date** | Unknown |
| **Type** | Video |
| **Duration** | 9:00 |
| **Views** | 261,125 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 0 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=mViFYTwWvcM) |
| **Category** | - |
| **Language** | - |
---

## Tags

_No tags._
---

## Description

_No description provided._
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
| **Characters** | `8804` |
| **Error** | `none` |


Right now, the way apps are getting built is completely changing because before, writing and reviewing code was the hardest part. But now it's knowing how to effectively convey what you want to build with an LLM. And then, my friends, is what's known as spec-driven development. Thank you very much. Nah, I'm just kidding. Because the thing is, spectrum and development has become one of the most important skills to learn if you're looking to be an AI engineer or to use AI to help build your applications. But let me explain why it's different from a common technique that you might also know, which is vibe coding, right? And this is typically what people think of when they think of AI-assisted coding or coding agents. So I want to give you a quick example of what vibe coding typically looks like, and we'll kind of compare how this is different than spec coding here in a second. But as a user, as a developer, as a builder, what you're going to start from is typically your AI coding agent, whether it's in a browser or it's on your machine itself. You're going to start from that initial prompt. So you're going to write that initial prompt to the LLM and say, hey, I want a specific application that does this functionality in this specific language like Java or Python. And that prompt is then sent to the model, and that model is then going to start generating code based on what it thinks that you want from that project and that it's been trained on as well. So at this point, we've got some boilerplate code, and this is great for testing. That's why I love vibe coding for, and we're going to go from here. But the thing is we might not have the exact desired implementation that we want. So we're going to go ahead and edit that prompt. So we're going to say actually I wanted um, something different or to use a different type of library or something like that. So we'll go from the prompt editing over to the AI uh, still continuing to code, and we'll go back and forth until we reach that desired implementation after a few tries. Right? So we are at the desired state of implementation. So that's typically what we see when we're doing vibe coding. But the thing is like how did, for example, the AI model decide to make that specific decision that it did based on the prompt that we gave? Because we could do a hundred different tries of this implementation of the app we want to create. We might get a different result every time. And that frustrates a lot of people. And the thing is,uh, vibe coding kind of skips the traditional software delivery lifecycle, also known as the SDLC that we're used to in software engineering. So the software development lifecycle takes a little bit of a different approach, because we start our project by planning and designing using specific project requirements, or the PRD as it's typically called. And then we take what we need and require for our project and begin to implement those features. Once we have those features, we test to see if they work. We do a little bit of quality assurance, and then it goes into the deployment phase—from dev to staging to production and finally the maintenance of that project. And so while vibe coding is fantastic, and I know it feels like magic, spec coding takes a little bit of a different approach and adds in some of these software development lifecycle components to AI-generated software development. So let's take a look at what spec coding looks like in a hypothetical scenario. So spec coding or spec-driven development n-again is going to take into consideration some of those software development lifecycle aspects, right, but also use the LLM just like vibe coding in order to as a AI agent write code or run these tests. But it all starts, um, with the prompt, of course, at first. But the thing is, we're not prompting a specific implementation. We're prompting what we want our system to do, so the behavior, the constraints that we want. And that specific uh, specification is then used like a contract to create a requirements. And this requirements is going to be kind of the main hierarchy of how this project is going to work. So how we want the model and the agent to write code, to do tests, documentation, verification and much, much more is all going to be focused from around the requirements itself. And the thing is, if we're happy with those requirements, so if we're happy we can approve and we can say yes, I want to turn this requirements specification into a design document that will then have to-dos for each specific implementation. Or I can say, hey, I want to edit how I want this project to be implemented, because at this point nothing has been implemented and AI models are all about proper instructions. So having a spec like this is much better than having the LLM guess what solution is going to hopefully best fit the user's request. So we go from the design here, and if we're happy with that design and how we actually want it to be implemented in code, well, then we can have the model, if we're happy, go off and implement this. So we can go and use that AI agent, or we can continue to do more requests on the specific implementation features that we want to get back to. And that's how spec coding works. But really quickly, I want to explain how it's different than other development cycles. So in traditional development, so the way that,uh, you know, most folks kind of started by writing code, it was uh, first code, right? And then afterwards it was documentation, right? So we would kind of start with our intuition um, and we would kind of go from there. The thing is, we also started to work with test-driven development. So test-driven development, as you can probably assume in the name, is where we start from the test and what the functionality we want for this, you know, application's behavior to be, and then go into writing the code afterwards. So that was also another popular way to approach development. And the thing with uh, spec coding, so spec-driven development is it kind of turns it on its head. So we kind of go from specifications, these specs that we have here, to the design document requirements and actually implementing that. And then we go to code. And so it's kind of test-driven development and behavior devel ... driven development on steroids, which is really cool. So let me give you a quick example of how this works in practice. So, we'll start off with vibe coding. So with vibe coding, again, we're just talking to the model. We're doing quick edits on the fly. I think that's that's what it's best for, right? We're going to say hey we need um, let's see, what do we need. Uh, maybe, um, a slash login page for our users, um, to authenticate. So,okay, that's a great request to the model. But how does it, how do we know what it's going to do? It might have 30 different ways to implement this, and we might have to go back and forth with the model. And that can take sometimes longer than just writing the code ourselves. So, vibe coding is one way to approach that problem. The spec-driven development uh, approach is a little bit different, but of course still using the LLM to create this requirement that we have for this feature, right? So, in this case, with spec-driven development, we're going to have a new feature. And this feature is going to be user authentication, right? So, this is a new feature that we want to the LLM to build out. Of course, we haven't started implementing yet. This is just the kind of planning phase.Uh, and we're going to say hey, this is going to be an endpoint at slash login to do post requests to. Okay, awesome. And then what variables are we going to take for the username and password. Well, we can say hey we're going to accept two different variables, so they're going to be user and then pass. Awesome. So that is in there, and we know when the implementation starts why it got to this conclusion. Um, let's say for some reason if it doesn't work, we're going to have a fallback, a failure code. Um, if missing, I don't know, it's a username. Right? And then we can also generate test cases from here. So, let's go on to test. And we're going to say hey um, valid credentials. Um, we'll give a 200 code. And this is really cool because when we're doing AI-assisted coding, we now have less ambiguity for our coding agents. And we can use spectrum encoding to kind of flip the traditional development model, right, so that we have this spec and that becomes the primary artifact that drives all this downstream work like implementation and test and much more. If you learned something today, I'd love if you could hit the like button and hack the algorithm. And make sure you subscribe for more content around AI and application development. Have a good one!
