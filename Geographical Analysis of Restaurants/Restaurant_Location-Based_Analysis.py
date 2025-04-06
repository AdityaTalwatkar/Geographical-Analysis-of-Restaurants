import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px

# Sample dataset
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'name': [
            'Taste of India', 'Beijing Bites', 'Mumbai Spice', 'Chennai Delight', 
            'Punjabi Dhaba', 'Italian Feast', 'Thai Orchid', 'Sushi Haven', 
            'Burger Junction', 'Cafe Latte', 'Mediterranean Grill'
        ],
        'latitude': [
            12.9716, 39.9042, 19.0760, 13.0827, 31.6340, 41.9028, 13.7563, 
            35.6895, 40.7128, 51.5074, 36.1627
        ],
        'longitude': [
            77.5946, 116.4074, 72.8777, 80.2707, 74.8723, 12.4964, 100.5018, 
            139.6917, -74.0060, -0.1278, -86.7816
        ],
        'city': [
            'Bangalore', 'Beijing', 'Mumbai', 'Chennai', 'Amritsar', 'Rome', 
            'Bangkok', 'Tokyo', 'New York', 'London', 'Nashville'
        ],
        'rating': [4.5, 4.2, 4.0, 4.7, 4.3, 4.6, 4.4, 4.8, 4.1, 4.0, 4.5],
        'cuisine': [
            'Indian', 'Chinese', 'Indian', 'South Indian', 'North Indian', 
            'Italian', 'Thai', 'Japanese', 'American', 'Cafe', 'Mediterranean'
        ],
        'price_range': [2, 3, 2, 2, 1, 3, 3, 4, 2, 2, 3]
    })
    return data

# Main function
def main():
    st.title("Restaurant Location-Based Analysis")
    data = load_data()

    # Display the dataset
    if st.checkbox("Show raw data"):
        st.write(data)

    # Step 1: Visualize restaurant distribution on a map
    st.header("Restaurant Distribution on Map")
    # Set map center around India
    map_center = [20.5937, 78.9629]  # India center coordinates
    restaurant_map = folium.Map(location=map_center, zoom_start=5)
    
    # Group data by city and count restaurants
    city_counts = data['city'].value_counts().reset_index()
    city_counts.columns = ['City', 'Number of Restaurants']
    
    # Create a dictionary to map city to restaurant count
    city_restaurant_count_dict = dict(zip(city_counts['City'], city_counts['Number of Restaurants']))

    for _, row in data.iterrows():
        city_name = row['city']
        city_restaurant_count = city_restaurant_count_dict[city_name]
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['name']} - {row['cuisine']}<br>City: {city_name}<br>Number of Restaurants in {city_name}: {city_restaurant_count}",
            tooltip=row['name']
        ).add_to(restaurant_map)
    
    folium_static(restaurant_map)

    # Step 2: Group restaurants by city and analyze concentration
    st.header("Restaurant Concentration by City")
    st.write(city_counts)

    # Visualize city-wise restaurant counts
    fig = px.bar(city_counts, x='City', y='Number of Restaurants', title="Restaurant Count by City")
    st.plotly_chart(fig)

    # Step 3: Calculate statistics by city
    st.header("Statistics by City")
    selected_city = st.selectbox("Select a city", data['city'].unique())
    city_data = data[data['city'] == selected_city]

    # Average ratings
    avg_rating = city_data['rating'].mean()
    st.write(f"Average Rating in {selected_city}: {avg_rating:.2f}")

    # Most common cuisines
    common_cuisines = city_data['cuisine'].value_counts().reset_index()
    common_cuisines.columns = ['Cuisine', 'Count']
    st.write("Most Common Cuisines:")
    st.write(common_cuisines)

    # Average price range
    avg_price = city_data['price_range'].mean()
    st.write(f"Average Price Range in {selected_city}: {avg_price:.2f}")

    # Step 4: Identify insights and patterns
    st.header("Insights and Patterns")
    st.write("1. Cities with the highest number of restaurants:")
    st.write(city_counts.head())

    st.write("2. Correlation between price range and ratings:")
    fig = px.scatter(data, x='price_range', y='rating', color='city', title="Price Range vs Rating")
    st.plotly_chart(fig)

    st.write("3. Popular cuisines across all cities:")
    popular_cuisines = data['cuisine'].value_counts().reset_index()
    popular_cuisines.columns = ['Cuisine', 'Count']
    st.write(popular_cuisines)

    # Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Restaurant Location-Based Analysis | Developed by Aditya Rajendra Talwatkar"
    "</div>",
    unsafe_allow_html=True,
)

if __name__ == "__main__":
    main()
