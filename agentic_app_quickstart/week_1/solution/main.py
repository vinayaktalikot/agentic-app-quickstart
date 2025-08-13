import asyncio
import sys
import uuid
from typing import Optional

from agent import create_csv_analysis_system


class CSVCLI:
    """Hybrid professional command-line interface for CSV data analysis."""
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize the hybrid professional CLI.
        
        Args:
            session_id: Optional session ID for conversation continuity
        """
        # Generate session ID if not provided
        self.session_id = session_id or f"session_{uuid.uuid4().hex[:8]}"
        self.analysis_system = create_csv_analysis_system(self.session_id)
        self.session_active = True
        self.conversation_count = 0
    
    def display_welcome(self):
        """Display professional welcome message."""
        print("=" * 80)
        print("📊 CSV Data Analysis Agent")
        print("=" * 80)
        print()
        print("Welcome! I'm your intelligent data analyst with persistent memory.")
        print()
        print(f"Session ID: {self.session_id}")
        print("Database: csv_conversations.db")
        print("Framework: SQLiteSession + OpenAI API")
        print("Memory: Persistent SQLite database")
        print()
        print("Available datasets:")
        print("  • sample_sales.csv - E-commerce sales data")
        print("  • employee_data.csv - HR and salary information")
        print("  • weather_data.csv - Weather measurements")
        print()
        print("What would you like to know about your data?")
        print()
        print("Commands:")
        print("  • Type your question naturally (e.g., 'What's the average price?')")
        print("  • 'status' - Show system status")
        print("  • 'help' - Show available commands")
        print("  • 'session' - Show session information")
        print("  • 'quit', 'exit', or 'q' - End the session")
        print()
        print("-" * 80)
    
    def display_help(self):
        """Display comprehensive help information."""
        print("\n📖 Help & Examples")
        print("-" * 40)
        print()
        print("Commands:")
        print("  • help - Show this help message")
        print("  • status - Show system status")
        print("  • session - Show session information")
        print("  • quit/exit/q - Exit the application")
        print()
        print("Example Questions:")
        print()
        print("Basic Analysis:")
        print("  • What's the average price in the sales data?")
        print("  • How many employees are in the Engineering department?")
        print("  • What are the column names in weather_data.csv?")
        print()
        print("Dataset Information:")
        print("  • What datasets are available?")
        print("  • Show me info about sample_sales.csv")
        print("  • What columns are in employee_data.csv?")
        print()
        print("Advanced Analysis:")
        print("  • Find correlations between temperature and humidity")
        print("  • Detect outliers in salary data")
        print("  • Group sales by customer state and sum amounts")
        print()
        print("Tips:")
        print("  • Be specific about which dataset you want to analyze")
        print("  • Ask follow-up questions to dive deeper")
        print("  • Use natural language - I understand context!")
        print("  • I remember our entire conversation!")
        print()
    
    async def display_system_status(self):
        """Display comprehensive system status."""
        try:
            session_info = self.analysis_system.get_session_info()
            
            print("\n📊 System Status")
            print("-" * 40)
            print("System: CSV Data Analysis Agent")
            print("Status: Operational")
            print("Architecture: SQLiteSession + OpenAI API")
            print("Memory: Persistent (SQLite database)")
            print(f"Session ID: {session_info['session_id']}")
            print(f"Database: {session_info['database_path']}")
            print(f"Framework: {session_info['framework']}")
            print("Available Tools: Dataset loading, statistics, analysis, correlations")
            print("Conversation Count:", self.conversation_count)
            print()
            
        except Exception as e:
            print(f"❌ Error retrieving system status: {str(e)}")
    
    def display_session_info(self):
        """Display session information."""
        try:
            session_info = self.analysis_system.get_session_info()
            
            print("\n🔐 Session Information")
            print("-" * 40)
            print(f"Session ID: {session_info['session_id']}")
            print(f"Database Path: {session_info['database_path']}")
            print(f"Framework: {session_info['framework']}")
            print(f"Memory Enabled: {session_info['memory_enabled']}")
            print(f"Session Type: {session_info['session_type']}")
            print()
            print("💡 This session will be saved and can be resumed later!")
            print("🔧 Using SQLiteSession + OpenAI API")
            print()
            
        except Exception as e:
            print(f"❌ Error retrieving session info: {str(e)}")
    
    async def process_user_input(self, user_input: str) -> str:
        """
        Process user input using the hybrid analysis system.
        
        Args:
            user_input: The user's question or request
            
        Returns:
            str: The agent's response
        """
        try:
            self.conversation_count += 1
            response = await self.analysis_system.analyze_request(user_input)
            return response
            
        except Exception as e:
            return f"""❌ System Error

I encountered an unexpected error: {str(e)}

This might be due to:
- Network connectivity issues
- API rate limiting
- Data processing errors
- Session database issues

Please try again or ask for help."""
    
    async def run_interactive_session(self):
        """Run the interactive CLI session with professional features."""
        self.display_welcome()
        
        while self.session_active:
            try:
                user_input = input("\n🤔 Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"\n👋 Thank you for using the CSV Data Analysis Agent!")
                    print(f"Session {self.session_id} has been saved. You can resume later!")
                    self.session_active = False
                    break
                
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                elif user_input.lower() == 'status':
                    await self.display_system_status()
                    continue
                
                elif user_input.lower() == 'session':
                    self.display_session_info()
                    continue
                
                elif not user_input:
                    print("Please enter a question or command.")
                    continue
                
                print(f"\n🔍 Processing: {user_input}")
                response = await self.process_user_input(user_input)
                print(f"\n📝 Response:\n{response}")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Session interrupted. Session {self.session_id} has been saved!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
    
    async def run_single_query(self, query: str):
        """
        Run a single query and return the response.
        
        Args:
            query: The user's question
            
        Returns:
            str: The agent's response
        """
        try:
            print(f"🔍 Processing: {query}")
            response = await self.process_user_input(query)
            print(f"\n📝 Response:\n{response}")
            return response
        except Exception as e:
            error_msg = f"❌ Error processing query: {str(e)}"
            print(error_msg)
            return error_msg


async def main():
    """Main function to run the hybrid professional CLI."""
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        cli = CSVCLI()
        await cli.run_single_query(query)
    else:
        # Interactive mode
        cli = CSVCLI()
        await cli.run_interactive_session()


if __name__ == "__main__":
    asyncio.run(main()) 