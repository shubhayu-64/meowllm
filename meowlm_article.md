# Building MeowLM: A Tiny Language Model From Scratch

Language models like GPT-4 are massive, requiring thousands of GPUs to train. But the core principles behind them—transformers, tokenization, autoregressive training—are simple enough to build on your laptop.

In this article, we will build **MeowLM**, a tiny generative AI model trained entirely from scratch. But instead of predicting Wikipedia or Reddit text, MeowLM is trained on synthetic data representing the thoughts and demands of a house cat. It gets zoomies, demands food, stares at ghosts, and refuses to leave your keyboard.

We will cover the entire pipeline:
1. **Dataset Creation**: Building the synthetic cat brain.
2. **Tokenization**: Teaching the model how to read text.
3. **Model Architecture**: Writing a Transformer from scratch in PyTorch.
4. **Training**: The training loop and learning rate schedules.
5. **Inference**: Chatting with our virtual feline.

---

## Step 1: Building the Dataset (`generate_data.py`)

A language model is only as good as its training data. Because we want MeowLM to act like a cat, we generate a synthetic dataset using randomized templates. 

Instead of writing 60,000 unique sentences by hand, we define **vocabulary pools** and **topic templates**.

```python
FOODS = ["tuna", "chicken wet food", "the crunchy bits", "salmon pate"]
GHOSTS = ["greebles", "a dust mote", "a shadow", "the invisible bug"]

def gen_zoomies():
    user_inputs = ["why are you running around", "it's 3am, go to sleep"]
    cat_outputs = ["must go fast.", "i saw a ghost.", "zoomies.", "*drifts around the corner*"]
    return {
        "input": random.choice(user_inputs), 
        "output": random.choice(cat_outputs)
    }
```

We generate 60,000 conversational pairs across various topics: getting the 3 AM zoomies, refusing to take a bath, demanding food (but then not eating it), and sitting on keyboards.

Each sample is formatted using special tokens so the model learns the boundary between human and cat:
```text
<|im_start|>user
why are you running around<|im_end|>
<|im_start|>assistant
must go fast.<|im_end|>
```

---

## Step 2: Tokenization (`prepare_data.py`)

Neural networks process numbers, not text. We use a **Tokenizer** to convert strings into integer IDs. 

We train a **Byte-Pair Encoding (BPE)** tokenizer on our generated text using the Hugging Face `tokenizers` library. 
- BPE starts with individual characters (bytes) and iteratively merges the most frequent pairs.
- This creates a vocabulary of 4,096 tokens tailored to our dataset. So words like "zoomies" or "greebles" might become single tokens, while rare words get split into sub-word tokens.

We define three critical special tokens:
- `<pad>` (ID 0): Used to pad short sequences so we can train in batches.
- `<|im_start|>` (ID 1): Marks the beginning of a message.
- `<|im_end|>` (ID 2): Marks the end of a message.

---

## Step 3: The Transformer Model (`model.py`)

MeowLM uses a decoder-only Transformer architecture (like GPT). It’s deliberately small so it can train quickly:
- **d_model**: 256 (the size of our embeddings)
- **Layers**: 4
- **Attention Heads**: 4
- **Total Parameters**: ~3 Million

### The Attention Mechanism
Attention is how the model learns context. At each step, a token looks at previous tokens to figure out what comes next.

```python
qkv = self.qkv(x) # Generates Query, Key, and Value vectors
attn = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
```
We apply a **causal mask** (a lower-triangular matrix of ones and negative infinities) to the attention scores. This is crucial: it prevents the model from looking into the "future" when predicting the next word.

### The Feed-Forward Network & Residuals
After attention mixes context across tokens, each token passes through a feed-forward network (FFN). We use `LayerNorm` and residual connections (`x = x + layer(x)`) to stabilize training and allow gradients to flow easily.

Finally, a linear layer (`lm_head`) projects the 256-dimensional embeddings back into our 4,096-token vocabulary to predict the next word.

---

## Step 4: The Training Loop (`train.py`)

Our dataset loads text as tensors. We structure the data so the model predicts the *next* token:
- `x` (Input): All tokens except the last.
- `y` (Target): All tokens except the first.

We use **Cross-Entropy Loss** to measure how surprised the model is by the correct next token.

### Training Optimizations
To make training efficient, we use several techniques:
1. **AdamW Optimizer**: Includes weight decay to prevent overfitting.
2. **Cosine Learning Rate Schedule**: We start with a "warmup" (gradually increasing the learning rate) and then decay it following a cosine curve. This prevents the model from making huge, unstable updates early on and helps it fine-tune at the end.
3. **Gradient Clipping**: Prevents "exploding gradients" by capping their maximum value.
4. **Mixed Precision (AMP)**: Uses 16-bit floats on GPUs to speed up training and save VRAM without sacrificing accuracy.

Every few hundred steps, we evaluate the model on our held-out test set to ensure it isn't just memorizing the training data.

---

## Step 5: Inference (`inference.py`)

Once the model is trained, how do we talk to it?

We pass a prompt to the model (e.g., `<|im_start|>user\nare you hungry?<|im_end|>\n<|im_start|>assistant\n`). 
The model predicts the next token. But instead of always picking the absolute highest probability token (which is boring and repetitive), we use **sampling**:

1. **Temperature**: Scales the logits before softmax. Higher temperature (>1.0) makes the cat more random and chaotic. Lower temperature (<1.0) makes it more predictable.
2. **Top-K**: We restrict the sampling pool to the top 40 most likely tokens, cutting off the "long tail" of gibberish.

The model generates one token, we append it to the context, and pass it back in. This loops autoregressively until the model outputs the `<|im_end|>` token.

---

## Evaluating the Cat (`eval_cases.py`)

To systematically test the model, we write evaluation cases. We don't just want grammatically correct text; we want the *personality* to shine through.

Example test case:
```python
{
    "id": "bath_time",
    "prompt": "time for a bath",
    "expect_keywords": ["no", "water", "hide", "scratch", "betrayal"],
    "expect_style": "horrified, defensive"
}
```
If we prompt MeowLM with "time for a bath", and it replies "i am already clean. i lick myself. hiss.", the test passes.

### Conclusion

And there you have it! From raw text generation to a working neural network, MeowLM proves that the architecture powering massive AI models is accessible, hackable, and can even be used to simulate a grumpy house cat.
