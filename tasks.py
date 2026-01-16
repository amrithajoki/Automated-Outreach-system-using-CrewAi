from crewai import Task

class AutomatedOutreachTasks:
    def find_leads_task(self, agent, tech_topic, search_depth):
        return Task(
            description=(
                f"Search for technical leads related to '{tech_topic}'. "
                f"You should look for recent GitHub issues, discussions, or LinkedIn posts where "
                f"people are struggling with specific problems related to {tech_topic}. "
                f"If you can't find a direct struggle, look for repositories using {tech_topic} "
                f"and infer potential scaling pains from their README or package.json. "
                f"Search depth factor: {search_depth} (adjusts how deep you dig - conceptually). "
                "Output a list of leads with: "
                "1. Name/Handle "
                "2. Source URL "
                "3. 'Hook' (The specific problem or observation) "
                "4. Confidence Score (Green/Yellow/Red) -> "
                "   Green=Explicit problem found. "
                "   Yellow=Inferred from tech stack. "
                "   Red=Generic hiring signal."
            ),
            expected_output=(
                "A structured list of 3-5 leads with Name, URL, Hook, and Confidence Level. "
                "Format as a JSON-like string or extremely clear bullet points."
            ),
            agent=agent,
            async_execution=False
        )

    def draft_email_task(self, agent, leads_context):
        return Task(
            description=(
                f"Take the leads found by the Scout: {leads_context}. "
                "For EACH lead, draft a short, 150-word text-based email. "
                "Do NOT include subject lines or placeholders like '[Your Name]'. "
                "Just the body text. "
                "Constraint: "
                "- If Confidence is Green: Be direct about the problem found. "
                "- If Confidence is Yellow/Red: Use an 'observation' pivot ('I noticed you use...'). "
                "Tone: Professional, Technical, Helpful. No salesy fluff."
            ),
            expected_output=(
                "A series of email drafts corresponding to each lead. "
                "Clearly separate them with '---' or Lead Name headers."
            ),
            agent=agent,
            async_execution=False
        )

    def explain_solution_task(self, agent, tech_topic, problem_context):
        return Task(
            description=(
                f"topic: {tech_topic}\n"
                f"User Problem Context: {problem_context}\n"
                "Analyze the user's specific problem in the context of the valid tech topic. "
                "Provide 3 concrete, actionable technical solutions or strategies to solve this problem. "
                "Constraints: "
                "- Length: 150-200 words total. "
                "- Format: Bullet points with specific technical recommendations. "
                "- Tone: Advisory, Expert, Solution-Oriented. "
                "- If no specific problem is provided, default to explaining best practices for the topic."
            ),
            expected_output=(
                "A structured list of 3 recommended solutions/strategies. "
                "Markdown format is required."
            ),
            agent=agent,
            async_execution=False
        )
