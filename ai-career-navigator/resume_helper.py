from openai import OpenAI

# ⚠️ Hardcoded API key (testing only)
client = OpenAI(api_key="sk-proj-12gTyU88mFRlsoxtrxrKsqIOos-I_oraN44wXr6r9YLYqpK3iokr3eZRCAwVx3QrrhnZLa3oM5T3BlbkFJ705AOhMFUF27vMK6jrD1kOHzSFmREKLuyCI67EhP5FmKn1GRmJ0AAoGJt88S81Sp0kG-8o8mIAA")

def improve_resume(resume_text: str, target_role: str = "Data Analyst") -> str:
    prompt = f"""
    You are an ATS resume expert.
    Improve the following resume for the role: {target_role}.
    1) Give an ATS optimization checklist.
    2) Rewrite the summary, skills, and 2 sample bullet points with strong verbs + metrics.
    3) Suggest keywords and a clean one-page layout.
    Resume text:
    ---
    {resume_text}
    ---
    Format output in markdown.
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"Be precise, practical, and recruiter-friendly."},
                  {"role":"user","content":prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content
