import streamlit as st
from dotenv import load_dotenv
from textwrap import dedent
from crewai import Agent, Crew

from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents

def main():
    load_dotenv()
    tasks = MarketingAnalysisTasks()
    agents = MarketingAnalysisAgents()

    st.title("Marketing Crew")
    st.markdown('---')

    product_website = st.text_input("Enter the product website:")
    product_details = st.text_input("Enter extra details about the Instagram post:")

    if st.button("Generate Marketing Strategy"):
        with st.spinner("Generating marketing strategy..."):
            # Create Agents
            product_competitor_agent = agents.product_competitor_agent()
            strategy_planner_agent = agents.strategy_planner_agent()
            creative_agent = agents.creative_content_creator_agent()

            # Create Tasks
            website_analysis = tasks.product_analysis(product_competitor_agent, product_website, product_details)
            market_analysis = tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
            campaign_development = tasks.campaign_development(strategy_planner_agent, product_website, product_details)
            write_copy = tasks.instagram_ad_copy(creative_agent)

            # Create Crew responsible for Copy
            copy_crew = Crew(
                agents=[product_competitor_agent, strategy_planner_agent, creative_agent],
                tasks=[website_analysis, market_analysis, campaign_development, write_copy],
                verbose=True
            )

            ad_copy = copy_crew.kickoff()

            st.success("Marketing strategy generated successfully!")

            st.subheader("Generated Ad Copy:")
            st.write(ad_copy)

            # Create Crew responsible for Image
            senior_photographer = agents.senior_photographer_agent()
            chief_creative_director = agents.chief_creative_director_agent()

            # Create Tasks for Image
            take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, product_website, product_details)
            approve_photo = tasks.review_photo(chief_creative_director, product_website, product_details)

            image_crew = Crew(
                agents=[senior_photographer, chief_creative_director],
                tasks=[take_photo, approve_photo],
                verbose=True
            )

            image = image_crew.kickoff()

            st.subheader("Generated Image Description:")
            st.write(image)

if __name__ == "__main__":
    main()
