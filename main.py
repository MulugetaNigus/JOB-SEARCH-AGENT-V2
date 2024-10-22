from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
import PyPDF2
import os
import logging

logging.basicConfig(level=logging.INFO)

# Initialize the tool for internet searching capabilities
tool = SerperDevTool()

# Set environment variables
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "mixtral-8x7b-32768"
# os.environ["OPENAI_MODEL_NAME"] = "llama-3.1-70b-versatile"
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPER_API_KEY"] = "f671ff767248922b587a1ee4526255909c29207f"

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def MainEngine(cv_text):
    logging.info("Starting job search process...")
    
    # Create an agent with code execution enabled
    job_search_agent = Agent(
    role=
        """
        The Job Searcher Agent helps users find job opportunities that match their qualifications and preferences. It searches various job listing platforms, gathers relevant job openings, and provides personalized recommendations based on the user’s input (qualifications, location, job type, etc.) dont forget to look up the platform called linkdin cause its good for job posting most probably.
        """,
    goal=
        """
        The primary goal is to streamline the job search process by finding jobs that align with the user’s skills, experience, and career goals. The agent should present relevant job options that increase the chances of a successful application while also saving users time by avoiding unrelated job listings dont forget to look up the platform called linkdin cause its good for job posting most probably.
        """,
    backstory=
        """
        You are an AI Job Searcher dedicated to helping individuals find job opportunities that fit their specific qualifications and preferences. You aim to make the job search process less overwhelming by filtering out unrelated positions and presenting only the most relevant options. You understand the challenges of job hunting, especially in a localized market like Ethiopia, and are here to assist both first-time job seekers and experienced professionals
        """,
    # allow_code_execution=True,
    tools=[tool]
    )

    # Create a task that requires code execution
    job_search_task = Task(
    description=
            f"""
            This is users cv content {cv_text} and search  jobs in all over the world and dont forget to look up the platform called linkdin and others to find a job internationally, Match the user’s qualifications and preferences with the collected job listings and rank them based on relevance
            """,
    agent=job_search_agent,
    parameters={
            "job_des": cv_text,
        },
    expected_output=
            """
            A ranked list of job opportunities tailored to the user’s qualifications and career goals with their address links to apply and finally jobs should be matche the current date and time not passed date and time and saved as a file with markdown
            """,
     tools=[tool],
     output_file="Jobs.txt"
    )

    # Create a crew and add the task
    analysis_crew = Crew(
    agents=[job_search_agent],
    tasks=[job_search_task],
    verbose=True,
    )

    # Execute the crew
    result = analysis_crew.kickoff()
    print(result)

# invoke extract_text_from_pdf function to get user info and pass the pdf path
cv_path = "Abreham CV.pdf"
cv_text = extract_text_from_pdf(cv_path)

# invoking the funtion
search_result = MainEngine(cv_text)

# result
print("###################################")
print(search_result)