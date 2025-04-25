from collections import Counter
import re

# [2025-02-20 14:34:02] INFO - Agent Response: ""I'm sorry, I didn't understand that.""


# Top 3 AI Responses:
# 1. "Hello! How can I help you today?" (12 times)
# 2. "I'm sorry, I didn't understand that." (7 times)
# 3. "Please provide more details." (5 times)

# Most Commo
# Most Common Errors:
# 1. Model Timeout after 5000ms (3 times)
# 2. API Connection Failure (2 times)

class LogSummaryAnaliser:
    def __init__(self):
        self.pattern = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] (\+\w+) - (.+)"
        # self.pattern = r'\[.*?\]\s*(INFO|ERROR|WARNING)\s*-\s*(.*)'
        self.log_level_types = Counter()
        self.message_types = Counter()
        self.errors = Counter()
        self.agent_responses = Counter()
        self.log_types = set()

    def get_logs(self, agent_log_path:str):
        print("calling")
        with open(agent_log_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                timestamp, log_level, message = re.match(self.pattern, line).group()
                self.message_types[message] = +1
                if "Agent Response" in message:
                    self.agent_responses[message] += 1

                if log_level == "ERROR":
                    self.errors[message]=+1
                
                self.log_level_types[log_level]+=1
                self.log_types.add(log_level)
    

    def printer_summary_log(self, agent_log_path:str):
        self.get_logs(agent_log_path)
        print("Log Summary:")
        for level_type in list(self.log_types):
            print(f"{level_type} messages: {self.log_level_types[level_type]}")

        
        print("Top 3 AI Responses:")

        most_common_ai = self.agent_responses.most_common(3)
        for idx, ai_response in enumerate(most_common_ai):
            print(f"{idx+1}. {ai_response[0]} ({ai_response[1]} times)")

        
        print("Most Common Errors")
        common_errors = self.errors.most_common(2)
        for idx, error in enumerate(common_errors):
            print(f"{idx+1}. {error[0]} ({error[1]} times)")
        


    
def test_regex_pattern():
    pattern = r"(\[\d[{2}-d{2}-d{2} \d{2}:\d{2}:\d{2}\])"

    text = "[2025-02-20 14:34:02] INFO - Agent Response: ""I\'m sorry, I didn't understand that."""
    print(re.match(pattern,text))


# test_regex_pattern()

if __name__ == "__main__":
    log_summarizer = LogSummaryAnaliser()
    log_summarizer.printer_summary_log("agent_log.log")