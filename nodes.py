import os
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

class PlannerState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    city: str
    interests: List[str]
    itinerary: str

# Define the LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# Define the itinerary prompt
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant. Create a day trip itinerary for {city} based on the user's interests: {interests}. Provide a brief, bulleted itinerary."),
    ("human", "Create an itinerary for my day trip."),
])

class Node(TypedDict):
    city: str
    interests: List[str]

    def input_city(state: PlannerState) -> PlannerState:
        return {
            **state,
            "city": Node.city,
            "messages": state['messages'] + [HumanMessage(content=Node.city)],
        }

    def input_interests(state: PlannerState) -> PlannerState:
        return {
            **state,
            "interests": [interest.strip() for interest in Node.interests.split(',')],
            "messages": state['messages'] + [HumanMessage(content=Node.interests)],
        }

    def create_itinerary_plan(state: PlannerState):
        response = llm.invoke(itinerary_prompt.format_messages(city=state['city'], interests=", ".join(state['interests'])))
        state["itinerary"] = response.content
        state["messages"] += [AIMessage(content=response.content)]
        return response.content

    def create_itinerary(state: PlannerState) -> PlannerState:
        response = llm.invoke(itinerary_prompt.format_messages(city = state['city'], interests = ','.join(state['interests'])))
        print(response.content)
        return {
            **state,
            "messages": state['messages'] + [AIMessage(content=response.content)],
            "itinerary" : response.content,
        }