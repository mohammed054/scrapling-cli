![Thumbnail](https://i.ytimg.com/vi/S5AGN9XfPK4/hqdefault.jpg?sqp=-oaymwEnCNACELwBSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLA0Tkt7CrIHbDHz5Yilc5sJI6qf8Q)

# What is Back Propagation
---

## Info

| Field | Value |
|-------|-------|
| **Date** | 2y ago |
| **Type** | Video |
| **Duration** | 7:59 |
| **Views** | 187,037 |
| **Likes** | 0 |
| **Comments** | 0 |
| **Like ratio** | 0.0000% |
| **Comment ratio** | 0.0000% |
| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |
| **Subscribers** | 1,700,000 |
| **URL** | [Watch on YouTube](https://www.youtube.com/watch?v=S5AGN9XfPK4) |
| **Category** | - |
| **Language** | - |
---

## Tags

`IBM` `IBM Cloud` `back propagation` `backpropagation` `back-propagation` `ml` `dl` `machine learning` `deep learning` `ai` `artificial intelligence` `error mitigation` `neural networks.`
---

## Description

Learn about watsonx→ https://ibm.biz/BdyEjK

Neural networks are great for predictive modeling — everything from stock trends to language translations. But what if the answer is wrong, how do they “learn” to do better? Martin Keen explains that during a process called backward propagation, the generated output is compared to the expected output, and then the error contributed by each neuron (or “node”) is examined. By adjusting the node’s weights and biases, error is reduced and thus the overall accuracy improved.

Get started for free on IBM Cloud → https://ibm.biz/sign-up-now

Subscribe to see more videos like this in the future → http://ibm.biz/subscribe-now
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
| **Characters** | `6250` |
| **Error** | `none` |


We're going to take a look at back propagation. It's central to the functioning of neural networks, helping them to learn and adapt. And we're going to cover it in simple but instructive terms. So even if your only knowledge of neural networks is "Isn't that something to do with chatGPT?" Well, we've got you covered. Now, a neural network fundamentally comprises multiple layers of neurons interconnected by weights. So I'm going to draw some neurons here, and I'm organizing them in layers. And these neurons are also known as nodes. Now, the layers here are categorized. So that's let's do that, the categorization. We have a layer here called the input layer. These two layers in the middle here are the hidden layer and the layer on the end here, that is the output layer. And these neurons are all interconnected with each other across the layers. So each neuron is connected to each other neuron in the next layer. So you can see that here. Okay, so now we have our basic neural network. And during a process called forward propagation, the input data traverses through these layers where the weights, biases and activation functions transform the data until an output is produced. So, let's define those terms. Weights, what is that when we're talking about a neural network? Well, the weights define the strength of the connections between each of the neurons. Then we have the activation function, and the activation function is applied to the weighted sum of the inputs at each neuron to introduce non-linearity into the network, and that allows it to make complex relationships. And that's really where we can use activation functions. Commonly, you'll see activation functions used such as sigmoid, for example. And then finally, biases. So biases really are the additional parameter that shift the activation function to the left or the right, and that aids the network's flexibility. So, consider a single training instance with its associated input data. Now, this data propagates forward through the network, causing every neutron to calculate a weighted sum of the inputs, which is then passed through its activation function. And the final result is the network's output. Great! So where does back propagation come in? Well, the initial output might not be accurate. The network needs to learn from its mistakes and adjust its weights to improve. And back propagation is essentially an algorithm used to train neural networks, applying the principle of error correction. So, after forward propagation, the output error, which is the difference between the network's output and the actual output, is computed. Now that's something called a loss function. And the error is distributed back through the network, providing each neuron in the network a measure of its contribution to total error. Using these measures, back propagation adjusts the weights and the biases of the network to minimize that error. And the objective here is to improve the accuracy of the network's output during subsequent forward propagation. It's a process of optimization, often employing a technique known as gradient descent. Now, gradient descent, that's the topic of a whole video of its own, but essentially, gradient descent is an algorithm used to find the optimal weights and biases that minimize the lost function. It iteratively adjusts the weights and biases in the direction that reduces the error most rapidly. And that means the steepest descent. Now, back propagation is widely used in many neural networks. So let's consider a speech recognition system. We provide as input a spoken word, and it outputs a written transcript of that word. Now, if during training our spoken inputs, it turns out that it doesn't match the written outputs, then back propagation may be able to help. Look, I speak with a British accent, but I've lived in the US for years. But when locals here ask for my name-- Martin --they often hear it as something different entirely, like Marvin or Morton or Mark. If this neural network had made the same mistake, we'd calculate the error by using the loss function to quantify the difference between the predicted output "Marvin" and the actual output "Martin". We'd compute the gradient of the loss function with respect to the weight and biases in the network and update the weighting biases in the network accordingly. Then we'd undergo multiple iterations of forward propagation and back propagation, tinkering with those weights and biases until we reach convergence-- a time where the network could reliably translate Martin into M-A-R-T-I-N. This is can't be applied to people, can it? Well, but anyway, let's just talk about one more thing with back propagation, and that's the distinction between static and recurrent back propagation networks. Let's start with static. So static back propagation is employed in a feed-forward neural networks where the data moves in a single direction from input layer to output layer. Some example use cases of this, well, we can think of OCR, or optical character recognition, where the goal is to identify and classify the letters and numbers in a given image. Another common example is with spam detection, and here we are looking to use a neural network to learn from features such as the emails, content and the sender's email address to classify an email as spam or not spam. Now back propagation can also be applied to recurrent neural networks as well, or RNNs. Now these networks have loops, and this type of back propagation is slightly more complex given the recursive nature of these networks. Now, some use cases? If we think about sentiment analysis, that's a common use case for this. And that's a good example of where RNNs are used to analyze the sentiment of a piece of text, like a customer product review. Another good example is time series prediction. So predicting things like stock prices or weather patterns. Ultimately, back propagation is the backbone of the learning in neural networks. It tests for errors, working its way back from the output layer to the input layer, adjusting the weights as it goes with the goal to minimize future errors. Errors like how to pronounce Martin in a passible American accent. MART-EN... MAR-EN... MART-ENNE.
