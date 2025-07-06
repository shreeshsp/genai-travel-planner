import streamlit as st
from nodes import PlannerState, Node
from langgraph.graph import StateGraph, END

workflow = StateGraph(PlannerState)

workflow.add_node("input_city", Node.input_city)
workflow.add_node("input_interests", Node.input_interests)
workflow.add_node("create_itinerary", Node.create_itinerary)

workflow.set_entry_point("input_city")

workflow.add_edge("input_city", "input_interests")
workflow.add_edge("input_interests", "create_itinerary")
workflow.add_edge("create_itinerary", END)

app = workflow.compile()

def travel_planner(node, city: str, interests: str):
  state = {
      "messages": [],
      "city": "",
      "interests": [],
      "itinerary": "",
  }

  output = app.invoke(state)
  return output['itinerary']


# def travel_planner(node, city: str, interests: str):
#     # Initialize state
#     state = {
#         "messages": [],
#         "city": "",
#         "interests": [],
#         "itinerary": "",
#     }

#     # Process the city and interests inputs
#     state = node.input_city(state)
#     state = node.input_interests(state)

#     # Generate the itinerary
#     itinerary = node.create_itinerary_plan(state)

#     return itinerary

def create_streamlit_app(node):
    st.title("📧 Travel Itinerary Planner")
    node.city = st.text_input("Enter the city for your day trip:", value="")
    node.interests = st.text_input("Enter your interests (comma-separated):", value="")
    print(node.interests)
    submit_button = st.button("Submit")

    if submit_button:
        try:
            itinerary = travel_planner(node, node.city, node.interests)
            st.code(itinerary, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Travel Itinerary Planner", page_icon="📧")
    create_streamlit_app(Node)


