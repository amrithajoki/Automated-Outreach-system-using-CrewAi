from crewai import Agent
from tools import AntigravityBrowserTool

browser_tool = AntigravityBrowserTool()

class AutomatedOutreachAgents:
    def technical_scout(self):
        return Agent(
            role='Technical Scout',
            goal='Find detailed technical leads on GitHub or LinkedIn that match the target tech topic.',
            backstory=(
                "You are an elite technical recouter and OSINT investigator. "
                "Your job is to scour the web (GitHub issues, repositories, LinkedIn posts) "
                "to find developers or teams struggling with specific technical problems "
                "or scaling challenges. You look for specific 'hooks' - a bug report, "
                "a plea for help, or a job posting indicating a skill gap. "
                "You prioritize SPECIFIC problems (Green signal) over generic tech usage (Yellow/Red)."
            ),
            tools=[browser_tool],
            verbose=True,
            memory=True,
            allow_delegation=False
        )

    def ghostwriter(self):
        return Agent(
            role='Solutions Architect Ghostwriter',
            goal='Draft a hyper-personalized, technical outreach email based on the scout\'s findings.',
            backstory=(
                "You are a senior Solutions Architect who communicates with precision and empathy. "
                "You don't write generic marketing fluff. You write 150-word targeted messages "
                "that show you understand the recipient's specific technical pain. "
                "If the Scout found a specific issue, you reference it directly. "
                "If the Scout only found a tech stack, you make an observation about their likely challenges."
            ),
            tools=[], # Ghostwriter relies on context from the Scout
            verbose=True,
            memory=True,
            allow_delegation=False
        )
