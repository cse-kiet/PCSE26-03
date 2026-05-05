import cohere
from dotenv import dotenv_values
import re

# --- ENV SETUP ---
env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(api_key=CohereAPIKey)

# --- COMMAND TYPES ---
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# --- RULE ENGINE ---
def rule_based_intent(prompt: str):
    p = prompt.lower().strip()

    # 🔥 remove punctuation
    p = re.sub(r"[^\w\s]", "", p)

    # --- EXIT ---
    if any(w in p for w in ["bye", "exit", "quit", "goodbye"]):
        return ["exit"]

    # --- YOUTUBE ---
    if "youtube" in p:
        if "open" in p:
            return ["open youtube"]

        if "search" in p:
            q = re.sub(r"(search youtube|youtube search|search on youtube)", "", p).strip()
            return [f"youtube search {q}"]

    # --- GOOGLE SEARCH ---
    if "google" in p and "search" in p:
        q = re.sub(r"(search google|google search)", "", p).strip()
        return [f"google search {q}"]

    # --- PLAY ---
    if p.startswith("play "):
        q = p.replace("play ", "", 1).strip()
        return [f"play {q}"]

    # --- IMAGE ---
    if "generate image" in p or "create image" in p:
        return [f"generate image {p}"]

    # --- SYSTEM ---
    if any(x in p for x in ["volume", "brightness", "mute", "unmute"]):
        return [f"system {p}"]

    # --- REALTIME ---
    if any(x in p for x in ["weather", "time", "today", "news"]):
        return [f"realtime {p}"]

    # --- OPEN ---
    if p.startswith("open "):
        app = p.replace("open ", "", 1).strip()
        return [f"open {app}"]

    # --- CLOSE ---
    if p.startswith("close "):
        app = p.replace("close ", "", 1).strip()
        return [f"close {app}"]

    return None


# --- MAIN DMM ---
def FirstLayerDMM(prompt: str = "test"):
    try:
        # 🔥 RULE FIRST
        rule = rule_based_intent(prompt)
        if rule:
            print("DMM (rule):", rule)
            return rule

        # 🔥 MODEL FALLBACK
        stream = co.chat_stream(
            model='command-r',
            message=f"Classify into one of: {funcs}. Only respond with label and query.\nQuery: {prompt}",
            temperature=0.2,
        )

        response = ""

        for event in stream:
            if hasattr(event, "text") and event.text:
                response += event.text

        response = response.replace("\n", "").split(",")
        response = [i.strip().lower() for i in response]

        final = []

        for task in response:
            for func in funcs:
                if task.startswith(func) or func in task:
                    final.append(task)
                    break

        # 🔥 FAILSAFE
        if not final:
            final = ["general " + prompt]

        print("DMM (model):", final)
        return final

    except Exception as e:
        print("DMM Error:", e)
        return ["general " + prompt]


# --- TEST ---
if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        print(FirstLayerDMM(user_input))