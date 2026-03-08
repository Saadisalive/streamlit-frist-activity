from qroq import generate_response

import re
import streamlit as st

def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return True
    
    t = text.strip()

    if t.endswith(("**"),("*"),("-"),("_"),(':'),(","),("("),("["),("{")):
        return True
    if re.search(r"\d+\.\s*\*$", t):
        return True
    if not re.search(r"[.!?]\s*$", t): #no sentence ending punctuation
        return True
    return False


def complete_response(question: str, max_rounds: int = 2) -> str:
    #Ask for clean structured answer (helps avoid unfinished bullets)
    base_prompt = (
        "Answer clearly in nubered points"
        "Do not cut sentences. Finish each point fully.\n\n"
        "Question: {question}")
    
    ans = generate_response(base_prompt,temperature=0.3, max_tokens=1024)

    #2) If it looks cut, continue from last line without repeating
    rounds = 0
    while rounds < max_rounds and looks_incomplete(ans):
        cont_prompt = (
            "Continue EXACTLY from where you stoped."
            "Do not repeat earlier text. "
            "Finish the incomplete point and complete the answer.\n\n"
            f"question: {question}\n\n"
            f"Answer so far: {ans}\n\nContinue:")
        more = generate_response(cont_prompt,temperature=0.3, max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans = (ans.strip() + "\n" + more.strip()).strip()
        rounds += 1

    return ans

def main():
    st.title("AI Assistant(beta)")
    st.write("Welcome! You can ask me anything about various subjects, and I'll provide an answer.")

    user_input = st.text_input("Enter your question here:")

    if user_input:
        st.write(f"**Your question:** {user_input}")
        response = complete_response(user_input)
        st.write("**AI's answer:**")
        st.markdown(response)
    else:
        st.info("Please enter a question to ask.")

if __name__ == "__main__":
    main()
    