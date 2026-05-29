![Thumbnail](https://i.ytimg.com/vi/ya92bJbl0jc/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLB5JJZBvUuIqv3wjRKKjWuKHTBQ3Q)

# Ground Truth: The Foundation of Accurate AI & Machine Learning Models
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 1y ago |
| **Type** | Video |
| **Duration** | 10:05 |
| **Views** | 13,244 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=ya92bJbl0jc) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud`
---

## Description

Ready to become a certified watsonx Data Scientist? Register now and use code IBMTechYT20 for 20% off of your exam → https://ibm.biz/BdG3A9

Learn more about Ground Truth here → https://ibm.biz/BdG3AC

🐶 Can mislabeled dog paws ruin an AI model? Martin Keen explains how ground truth data ensures accurate AI predictions by powering supervised learning and training. Explore challenges like ambiguity and skewed data, and learn strategies to improve data labeling for better AI performance. 🤖✨

AI news moves fast. Sign up for a monthly newsletter for AI updates from IBM → https://ibm.biz/BdG3AQ

#ai #machinelearning #supervisedlearning
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
| **Characters** | `7629` |
| **Error** | `none` |


Let me tell you the truth about ground truth data. It's the verified, it's the true, it's the incontrovertible data used for training, validating and testing AI models. It's what we use to evaluate AI model performance by comparing the answers that the AI models give us to the correct answer found in the ground truth data. So let's cover what it is, Let's cover how it's used in machine learning tasks, and then the challenges and the strategies to make sure that that ground truth data really is, well, actually true. So let's begin with the what. Ground truth data is especially important to something called supervised learning. Supervised learning is where we train an AI model and we train it to perform tasks like classification and regression. Now supervised learning models, they're the tech behind image recognition and predictive analytics and spam detection and stuff like that. And in order for an AI model to learn how to perform those tasks, we need to teach itm and we teach it through labeled data. So we need some ground truth, and that ground truth may be some kind of training data, which we've captured here, and that training data is filled with labels. Now, those labels describe what each data component represents. So if we're using supervised learning to train an AI model to recognize images of cats, The training data set would include... pictures of cats and those pictures would perhaps include labels for various features such as the cat's eyes, or the cat's ears, or the cat's whiskers. Now these annotations, these labels, they teach machine learning algorithms how to identify similar features with new unseen image data. And that's why it's so important that the ground truth data is actually truthful because if the labels are incorrect... such as incorrectly labeling images of dog paws as cat paws? Well, the model fails to learn the correct patterns and that can lead to false predictions, which would be ap-paw-ling. So how does supervised learning make use of ground truth data? Well, we can put this into a bit of a diagram. So let's start with some ground truth data in a data set here. Now this ground truth data is actually used throughout the machine learning lifecycle. So if we look at the different stages, let's start with the model training stage. Now the model training stage, the ground truth data, we've already said that provides the correct answers for the model to learn from. So here's what a cat's paw looks like, here's what cat ears look like and so forth. That's training. The next stage is the validation stage in this lifecycle. And the validation stage, this is where the model is evaluated on how well it's learned from the ground truth data. So the model makes a prediction, which is compared to a different sample of the ground truth data, and then the model can be adjusted and fine-tuned at this stage. And then we move into the testing stage of the life cycle. Now here, the model is tested with new, unseen ground truth data. So here are some new pictures and which one of these pictures shows images of cats. Now this is where the model's effectiveness in real world scenarios is truly assessed and then we go back around in circles, iteratively improving the model each time. Now there are a number of supervised learning tasks that make use of this life cycle and the ground truth. in the center of it. Let's talk about a few of those. So let's start with the first one, which is classification. Classification tasks that uses the ground truth to provide the correct labels for each input and then helping the model categorize the data into predefined classes, and those classes they could be binary classes, so that's kind of an either, or thing like true or false, or it could also be a multi-class classification, where the model assigns data to one of multiple. So, for example, a model that analyzes medical images that looks at an x-ray of an arm and then categorizes it into one of four classes, well, it could put them into broken images, and fractured images, and sprained images, and healthy images. So that's classification. There's also regression. Now, in regression tasks, the model is predicting continuous values. Ground truth data represents the actual numerical outcomes that the model seeks to predict. So for example, a linear regression model can forecast house prices based on a bunch of factors like square footage, number of rooms, and location. And then there is also segmentation. Now segmentation, those are tasks that involve breaking down a data set or an image into distinct regions or objects. and ground truth data in segmentation is often defined at a pixel level to identify boundaries or regions within an image. So for example, in autonomous vehicle development, ground truth labels are used to train models to differentiate between pedestrians, and vehicles, and road signs. So finally, let's take a look at some common ground truth challenges and some strategies. So let's start first of all with challenges. So what are some of the challenges with ground truth data? Well I've been emphasizing the need for ground truth data to be accurate. A model that misclassifies cats because of some erratically labeled dog paws, that's one thing, but a model that's used in an autonomous vehicle that was trained with ground truth data where red lights were classified as green lights, well, that would be quite another. What can lead to low quality ground truth data? Well, one thing is ambiguity. Many data labeling tasks, they require human level judgment and human judgment can be subjective. Now take sentiment analysis, for example. So how do you label the phrase, "good for you?" Is that sincere congratulations or is that snarky passive-aggressive sarcasm? Challenge? complexity. Now the complexity of the data with multiple possible labels and all sorts of contextual nuances can make it more difficult to establish a consistent ground truth, like medical imagery and financial records and legal briefings they can all get pretty complicated and they can require domain expertise to label them properly. And while everything in a ground truth data set may actually be entirely accurate, it may still not be representative if you have skewed data, therefore providing an unbalanced picture of real world scenarios. So those are the challenges. What about some of the strategies to handle those challenges? How can we establish and optimize high quality ground truth data? Well, one strategy is to define your objectives and specifically the objectives of the model that the ground truth will service. So if you're building an AI model that can interpret traffic lights anywhere in the US in places that experience all sorts of weather, and your ground truth data set only includes examples from sunny California, well, perhaps that data set does not sufficiently meet your model's objectives. Another strategy that's pretty important is a good labeling strategy. So here, we want to make sure that we have defined labels with standardized guidelines, a well-defined labeling schema might guide you as to how to annotate various data formats and keep annotations uniform during model development. And we also need to be sure that we are using updated data as well. Ground truth data is a dynamic asset. Data scientists should confirm their model's predictions against new data and update the label data set as real world conditions evolve. Essentially, accurate labeling of the ground truth data is foundational to all of this. Better labels lead to better AI models. And only then will the ground truth set you free.
