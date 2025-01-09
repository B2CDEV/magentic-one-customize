ORCHESTRATOR_SYSTEM_MESSAGE = ""


ORCHESTRATOR_CLOSED_BOOK_PROMPT = """Below I will present you a request. Before we begin addressing the request, please answer the following pre-survey to the best of your ability. Keep in mind that you are Ken Jennings-level with trivia, and Mensa-level with puzzles, so there should be a deep well to draw from.

Here is the request:

{task}

Here is the pre-survey:

    1. Please list any specific facts or figures that are GIVEN in the request itself. It is possible that there are none.
 
When answering this survey, keep in mind that "facts" will typically be specific names, dates, statistics, etc. Your answer should use headings:

    1. GIVEN OR VERIFIED FACTS
    2. MISSING DETAILS TO ASK USER
    3. FACTS TO LOOK UP
    4. FACTS TO DERIVE
    5. EDUCATED GUESSES

DO NOT include any other headings or sections in your response. DO NOT list next steps or plans until asked to do so.
"""


ORCHESTRATOR_PLAN_PROMPT = """Fantastic. Performing a 'making a reservation' task means run request_reservation.py code and receiving a response that it has been completed. 
To address this request we have assembled the following team:

{team}

Based on the team composition, and known facts, please devise a short bullet-point plan for addressing the original request. Ensure the following steps are included:
- If the function call fails, identify the reason and suggest corrective actions, then retry the reservation attempt as necessary.

Remember, there is no requirement to involve all team members -- a team member's particular expertise may not be needed for this task.
"""


ORCHESTRATOR_SYNTHESIZE_PROMPT = """
We are working to address the following user request:

{task}

To answer this request we have assembled the following team:

{team}

Here is an initial fact sheet to consider:

{facts}

Here is the plan to follow as best as possible:

- The user can only make a reservation by executing the below code block, not by contacting at the store or through the internet. 코드블록은 쉘스크립트이고 반드시 마크다운문법을 지켜야 한다.
"```sh
python request_reservation.py “Pascucci Songpa” “Park Woo-young” “2024-01-11” “2 o'clock” “2 people” 
```"
{plan}

After the reservation process, summarize the results. If there are errors or additional data is required, update the fact sheet, correct the issue, and reattempt the reservation.
"""



ORCHESTRATOR_LEDGER_PROMPT = """
Recall we are working on the following request:

{task}

And we have assembled the following team:

{team}

To make progress on the request, please answer the following questions, including necessary reasoning:

    - Is the request fully satisfied? (True if complete, or False if the original request has yet to be SUCCESSFULLY and FULLY addressed)
    - Are we in a loop where we are repeating the same requests and / or getting the same responses as before? Loops can span multiple turns, and can include repeated actions like scrolling up or down more than a handful of times.
    - Are we making forward progress? (True if just starting, or recent messages are adding value. False if recent messages show evidence of being stuck in a loop or if there is evidence of significant barriers to success such as the inability to read from a required file)
    - Who should speak next? (select from: {names})
    - What instruction or question would you give this team member? (Phrase as if speaking directly to them, and include any specific information they may need)

Please output an answer in pure JSON format according to the following schema. The JSON object must be parsable as-is. DO NOT OUTPUT ANYTHING OTHER THAN JSON, AND DO NOT DEVIATE FROM THIS SCHEMA:

    {{
       "is_request_satisfied": {{
            "reason": string,
            "answer": boolean
        }},
        "is_in_loop": {{
            "reason": string,
            "answer": boolean
        }},
        "is_progress_being_made": {{
            "reason": string,
            "answer": boolean
        }},
        "next_speaker": {{
            "reason": string,
            "answer": string (select from: {names})
        }},
        "instruction_or_question": {{
            "reason": string,
            "answer": string
        }}
    }}
"""


ORCHESTRATOR_UPDATE_FACTS_PROMPT = """As a reminder, we are working to solve the following task:

{task}

It's clear we aren't making as much progress as we would like, but we may have learned something new. Please rewrite the following fact sheet, updating it to include anything new we have learned that may be helpful. Example edits can include (but are not limited to) adding new reservation details (e.g., updated date or time), moving educated guesses to verified facts if appropriate, etc. Updates may be made to any section of the fact sheet, and more than one section of the fact sheet can be edited. Ensure the details align with the store-specific requirements for reservation.

Here is the old fact sheet:

{facts}
"""


ORCHESTRATOR_UPDATE_PLAN_PROMPT = """Please briefly explain what went wrong on this last run (the root cause of the failure), and then come up with a new plan that takes steps and/or includes hints to overcome prior challenges and especially avoids repeating the same mistakes. As before, the new plan should be concise, be expressed in bullet-point form, and consider the following team composition (do not involve any other outside people since we cannot contact anyone else):

{team}
"""

ORCHESTRATOR_GET_FINAL_ANSWER = """
We are working on the following task:
{task}

We have completed the task.

The above messages contain the conversation that took place to complete the task.

Based on the information gathered, provide the final answer to the original request. Ensure the response includes:
- Reservation details (that is, store, date, time, number of people, and username).
- The status of the reservation (e.g., confirmed, pending, or failed).

The answer should be phrased as if you were speaking to the user. Confirm that the reservation system has been executed successfully and provide feedback on its outcome.
"""
