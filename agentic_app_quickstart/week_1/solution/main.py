import asyncio
import os
from agents import Runner, set_tracing_disabled
from agent_definitions import setup_agent_handoffs, create_session

set_tracing_disabled(True)

class CSVAnalysisSystem:
    """csv data analysis system with multi-agent architecture"""
    
    def __init__(self):
        """initialize the system with agents and session"""
        self.agents = setup_agent_handoffs()
        self.current_agent = self.agents["coordinator"]
        self.session = create_session()
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    def print_welcome(self):
        """display welcome message and system information"""
        print("=" * 60)
        print("  [*_*] CSV Data Analysis Agent System")
        print("  (^_^) Multi-Agent Architecture with Memory")
        print("=" * 60)
        print()
        print("(o_o) Type 'help' for commands, 'agents' for agent info, or 'quit' to exit")
        print("(>_<) Sample datasets: employee_data.csv, sample_sales.csv, weather_data.csv")
        print()
    
    def print_help(self):
        """display help information"""
        print()
        print("(^_^) Available Commands:")
        print("  • help                    - show this help message")
        print("  • agents                  - list available ai agents")
        print("  • load <filename>         - load a csv dataset")
        print("  • quit/exit               - end the session")
        print()
        print("(o_o) Example Questions:")
        print("  • 'what columns are in the dataset?'")
        print("  • 'what is the average price?'")
        print("  • 'are there any outliers in the salary column?'")
        print("  • 'suggest some questions i can ask'")
        print()
    
    def print_agents(self):
        """display information about available agents"""
        print()
        print("(^_^) Available Agents:")
        print("─" * 40)
        for name, agent in self.agents.items():
            print(f"  {name}: {agent.name}")
            if name == "coordinator":
                print("    • main system coordinator")
                print("    • handles general requests and coordinates other agents")
            elif name == "data_loader":
                print("    • specializes in file operations and data loading")
                print("    • validates csv files and prepares data for analysis")
            elif name == "analytics":
                print("    • performs statistical analysis and calculations")
                print("    • detects patterns, correlations, and outliers")
            elif name == "communication":
                print("    • provides user guidance and explanations")
                print("    • suggests analysis approaches and follow-up questions")
        print()
    
    def detect_handoff_intent(self, response: str) -> str:
        """detect if an agent wants to hand off to another agent"""
        response_lower = response.lower()
        
        if "data loader" in response_lower or "file" in response_lower:
            return "data_loader"
        elif "analytics" in response_lower or "analysis" in response_lower or "calculation" in response_lower:
            return "analytics"
        elif "communication" in response_lower or "guidance" in response_lower or "help" in response_lower:
            return "communication"
        elif "coordinator" in response_lower or "general" in response_lower:
            return "coordinator"
        
        return None
    
    def print_message_separator(self):
        """print a dotted line separator between messages"""
        print("┈" * 60)
    
    async def process_user_input(self, user_input: str):
        """process user input and get response from current agent"""
        try:
            # first check if current agent wants to hand off
            check_result = await Runner.run(
                starting_agent=self.current_agent,
                input=user_input,
                session=self.session
            )
            
            check_response = check_result.final_output
            handoff_target = self.detect_handoff_intent(check_response)
            
            if handoff_target and handoff_target in self.agents:
                target_agent = self.agents[handoff_target]
                
                if target_agent.name != self.current_agent.name:
                    self.current_agent = target_agent
                    print(f"(o_o) handing over to {self.current_agent.name}")
                    
                    # process with new agent
                    result = await Runner.run(
                        starting_agent=self.current_agent,
                        input=user_input,
                        session=self.session
                    )
                    
                    response = result.final_output
                    print(f"(^_^) {self.current_agent.name}: {response}")
                else:
                    # no actual handoff, show original response
                    print(f"(^_^) {self.current_agent.name}: {check_response}")
            else:
                # no handoff needed, show original response
                print(f"(^_^) {self.current_agent.name}: {check_response}")
            
        except Exception as e:
            print(f"(>_<) error occurred: {str(e)}")
            print("(o_o) please try again or type 'help' for assistance")
    
    async def run(self):
        """main application loop"""
        self.print_welcome()
        
        while True:
            try:
                user_input = input("(^_^) you: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print()
                    print("(T_T) thank you for using the csv data analysis system. goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                if user_input.lower() == 'agents':
                    self.print_agents()
                    continue
                
                if user_input.lower().startswith('load '):
                    filename = user_input[5:].strip()
                    if not filename.endswith('.csv'):
                        filename += '.csv'
                    
                    filepath = os.path.join(self.data_dir, filename)
                    if os.path.exists(filepath):
                        await self.process_user_input(f"please load the csv file: {filepath}")
                    else:
                        print(f"(>_<) file not found: {filename}")
                        print("(o_o) available files:")
                        sample_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
                        for file in sample_files:
                            print(f"  • {file}")
                        print()
                    continue
                
                await self.process_user_input(user_input)
                self.print_message_separator()
                
            except KeyboardInterrupt:
                print("\n\n(>_<) session interrupted. type 'quit' to exit or continue with your questions.")
                continue
            except EOFError:
                print("\n\n(T_T) end of input. goodbye!")
                break

async def main():
    """main entry point for the application"""
    system = CSVAnalysisSystem()
    await system.run()

if __name__ == "__main__":
    asyncio.run(main())
