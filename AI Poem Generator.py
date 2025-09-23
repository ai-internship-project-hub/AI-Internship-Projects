import torch
from transformers import pipeline, set_seed

# --------------------------
# Load model
# --------------------------
MODEL_NAME = "gpt2"   # better than distilgpt2, you can try EleutherAI/gpt-neo-125M
text_gen = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=0 if torch.cuda.is_available() else -1
)

# --------------------------
# Generator
# --------------------------
def generate_text(prompt, max_new_tokens=150, temperature=0.8,
                  top_p=0.92, top_k=50, repetition_penalty=1.2,
                  no_repeat_ngram_size=3, seed=42):
    if seed is not None:
        set_seed(seed)
    out = text_gen(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        eos_token_id=text_gen.tokenizer.eos_token_id,
        pad_token_id=text_gen.tokenizer.eos_token_id,
        num_return_sequences=1
    )[0]["generated_text"]
    return out

# --------------------------
# Poem prompt
# --------------------------
def make_poem_prompt(theme, lines, style, rhyme, tone, language="English"):
    rhyme_line = f" Use a {rhyme} rhyme scheme." if rhyme.lower() != "none" else ""
    return (
        f"Write a {lines}-line poem in {language} about '{theme}'."
        f" Style: {style}. Tone: {tone}.{rhyme_line}"
        " Each line must be a separate poetic line with vivid imagery."
        " Do not include a title. Begin directly with the poem.\n\nPoem:\n"
    )

# --------------------------
# Generate poem
# --------------------------
def generate_poem(theme, lines=6, style="lyrical", rhyme="none", tone="peaceful"):
    prompt = make_poem_prompt(theme, lines, style, rhyme, tone)
    raw = generate_text(prompt, max_new_tokens=lines*25)

    # Keep only the "poem" part
    body = raw.split("Poem:\n", 1)[-1]

    # Clean into lines
    poem_lines = [ln.strip() for ln in body.splitlines() if ln.strip()]

    # Sometimes GPT rambles → truncate to required number of lines
    return "\n".join(poem_lines[:lines])

# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    print("=== AI Poem Generator ===\n")
    theme = input("Enter the theme of the poem (e.g., 'sunset by the sea'): ")
    lines = int(input("Enter number of lines: "))
    style = input("Enter style (e.g., 'lyrical', 'haiku', 'modern free verse'): ")
    tone = input("Enter tone (e.g., 'peaceful', 'romantic', 'sad'): ")
    rhyme = input("Enter rhyme scheme (None / AABB / ABAB): ")

    print("\n--- Generated Poem ---\n")
    print(generate_poem(theme, lines, style, rhyme, tone))
