import asyncio
import os
from agents import Runner, set_tracing_disabled
from agent_definitions import setup_agent_handoffs, create_session

set_tracing_disabled(True)


class CSVAnalysisSystem:
    def __init__(self):
        self.agents = setup_agent_handoffs()
        self.current_agent = self.agents["coordinator"]
        self.session = create_session()
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")

    def print_welcome(self):
        """display welcome message and system information"""
        print("welcome to the csv data analysis system")
        print("=" * 50)
        print("this system uses specialized ai agents to help you analyze your csv data")
        print("available agents:")
        print("- coordinator: main system coordinator")
        print("- data loader: handles file operations")
        print("- analytics: performs data analysis")
        print("- communication: provides guidance and explanations")
        print("=" * 50)
        print("available sample datasets:")
        sample_files = [f for f in os.listdir(self.data_dir) if f.endswith(".csv")]
        for i, file in enumerate(sample_files, 1):
            print(f"{i}. {file}")
        print("=" * 50)
        print("type 'quit' or 'exit' to end the session")
        print("type 'help' for assistance")
        print("type 'agents' to see available agents")
        print("type 'load <filename>' to load a dataset")
        print()

    def print_help(self):
        """display help information"""
        print("help - csv data analysis system")
        print("-" * 30)
        print("basic commands:")
        print("  help          - show this help message")
        print("  agents        - list available agents")
        print("  load <file>   - load a csv file (e.g., load sample_sales.csv)")
        print("  quit/exit     - end the session")
        print()
        print("example questions you can ask:")
        print("  what columns are in the dataset?")
        print("  what is the average price?")
        print("  how many customers are from california?")
        print("  are there any outliers in the salary column?")
        print("  what are the correlations between numeric columns?")
        print("  suggest some questions i can ask")
        print()

    def print_agents(self):
        """display information about available agents"""
        print("available agents:")
        print("-" * 20)
        for name, agent in self.agents.items():
            print(f"{name}: {agent.name}")
            if name == "coordinator":
                print("  - main system coordinator")
                print("  - handles general requests and coordinates other agents")
            elif name == "data_loader":
                print("  - specializes in file operations and data loading")
                print("  - validates csv files and prepares data for analysis")
            elif name == "analytics":
                print("  - performs statistical analysis and calculations")
                print("  - detects patterns, correlations, and outliers")
            elif name == "communication":
                print("  - provides user guidance and explanations")
                print("  - suggests analysis approaches and follow-up questions")
        print()

    def detect_handoff_intent(self, response: str) -> str:
        """detect if an agent wants to hand off to another agent"""
        response_lower = response.lower()

        if "data loader" in response_lower or "file" in response_lower:
            return "data_loader"
        elif (
            "analytics" in response_lower
            or "analysis" in response_lower
            or "calculation" in response_lower
        ):
            return "analytics"
        elif (
            "communication" in response_lower
            or "guidance" in response_lower
            or "help" in response_lower
        ):
            return "communication"
        elif "coordinator" in response_lower or "general" in response_lower:
            return "coordinator"

        return None

    async def process_user_input(self, user_input: str):
        """process user input and get response from current agent"""
        try:
            # first check if current agent wants to hand off
            check_result = await Runner.run(
                starting_agent=self.current_agent, input=user_input, session=self.session
            )

            check_response = check_result.final_output
            handoff_target = self.detect_handoff_intent(check_response)

            if handoff_target and handoff_target in self.agents:
                target_agent = self.agents[handoff_target]

                if target_agent.name != self.current_agent.name:
                    self.current_agent = target_agent
                    print(f"handing over to {target_agent.name}")

                    # process with new agent
                    result = await Runner.run(
                        starting_agent=self.current_agent, input=user_input, session=self.session
                    )

                    response = result.final_output
                    print(f"agent: {response}")
                else:
                    # no actual handoff, show original response
                    print(f"agent: {check_response}")
            else:
                # no handoff needed, show original response
                print(f"agent: {check_response}")

        except Exception as e:
            print(f"error occurred: {str(e)}")
            print("please try again or type 'help' for assistance")

    async def run(self):
        """main application loop"""
        self.print_welcome()

        while True:
            try:
                user_input = input("you: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("thank you for using the csv data analysis system. goodbye!")
                    break

                if user_input.lower() == "help":
                    self.print_help()
                    continue

                if user_input.lower() == "agents":
                    self.print_agents()
                    continue

                if user_input.lower().startswith("load "):
                    filename = user_input[5:].strip()
                    if not filename.endswith(".csv"):
                        filename += ".csv"

                    filepath = os.path.join(self.data_dir, filename)
                    if os.path.exists(filepath):
                        await self.process_user_input(f"please load the csv file: {filepath}")
                    else:
                        print(f"file not found: {filename}")
                        print("available files:")
                        sample_files = [f for f in os.listdir(self.data_dir) if f.endswith(".csv")]
                        for file in sample_files:
                            print(f"  {file}")
                        print()
                    continue

                await self.process_user_input(user_input)
                print()

            except KeyboardInterrupt:
                print(
                    "\n\nsession interrupted. type 'quit' to exit or continue with your questions."
                )
                continue
            except EOFError:
                print("\n\nend of input. goodbye!")
                break


async def main():
    """main entry point for the application"""
    system = CSVAnalysisSystem()
    await system.run()


if __name__ == "__main__":
    asyncio.run(main())
