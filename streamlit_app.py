import streamlit as st
import pandas as pd
import datetime
import json
import os
from datetime import datetime, timedelta
import uuid

# Page configuration
st.set_page_config(
    page_title="David's Larder - Management System",
    page_icon="🥩",
    layout="wide"
)

# Data persistence functions
def save_data():
    """Save all session data to JSON file"""
    try:
        data = {
            'workers': st.session_state.workers,
            'orders': [
                {
                    **order,
                    'due_date': order['due_date'].isoformat() if isinstance(order['due_date'], datetime) else order['due_date']
                }
                for order in st.session_state.orders
            ],
            'timetable': st.session_state.timetable,
            'shop_jobs': st.session_state.shop_jobs,
            'job_descriptions': st.session_state.job_descriptions
        }
        with open('davids_larder_data.json', 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def load_data():
    """Load data from JSON file"""
    if os.path.exists('davids_larder_data.json'):
        try:
            with open('davids_larder_data.json', 'r') as f:
                data = json.load(f)
            
            # Convert date strings back to datetime objects
            for order in data.get('orders', []):
                if 'due_date' in order and isinstance(order['due_date'], str):
                    order['due_date'] = datetime.fromisoformat(order['due_date'])
            
            return data
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return None

# Initialize session state with persisted data
def initialize_session_state():
    """Initialize session state with saved data or defaults"""
    defaults = {
        'workers': [
            {
                'id': 1,
                'name': 'John MacLeod',
                'position': 'Butcher',
                'availability': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'unavailable_dates': [],
                'hours_per_week': 40,
                'skills': ['meat_cutting', 'customer_service', 'ordering']
            },
            {
                'id': 2,
                'name': 'Sarah Campbell',
                'position': 'Shop Assistant',
                'availability': ['Tuesday', 'Wednesday', 'Thursday', 'Saturday'],
                'unavailable_dates': [],
                'hours_per_week': 30,
                'skills': ['customer_service', 'packaging', 'cleaning']
            }
        ],
        'orders': [
            {
                'order_id': 'ORD001',
                'customer_name': 'Highland Hotel',
                'items': ['10kg Pork Shoulder', '5kg Beef Mince', '3 Whole Chickens'],
                'due_date': datetime.now() + timedelta(days=2),
                'status': 'Pending'
            }
        ],
        'timetable': {},
        'shop_jobs': {
            'Monday': {
                'morning': ['meat_preparation', 'display_setup', 'order_receiving'],
                'afternoon': ['customer_service', 'cleaning', 'inventory_check'],
                'evening': ['closing_duties', 'equipment_cleaning']
            },
            # ... (rest of your default shop_jobs)
        },
        'job_descriptions': {
            'meat_preparation': 'Preparing daily meat cuts and portions for display',
            # ... (rest of your default job_descriptions)
        }
    }
    
    # Load saved data or use defaults
    saved_data = load_data()
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            if saved_data and key in saved_data:
                st.session_state[key] = saved_data[key]
            else:
                st.session_state[key] = default_value

# Initialize the session state
initialize_session_state()

# Enhanced functions with auto-save
def add_worker(worker_data):
    st.session_state.workers.append(worker_data)
    save_data()

def remove_worker(worker_id):
    st.session_state.workers = [w for w in st.session_state.workers if w['id'] != worker_id]
    save_data()

def add_order(order_data):
    st.session_state.orders.append(order_data)
    save_data()

def update_order_status(order_id, status):
    for order in st.session_state.orders:
        if order['order_id'] == order_id:
            order['status'] = status
            break
    save_data()

def remove_order(order_id):
    st.session_state.orders = [o for o in st.session_state.orders if o['order_id'] != order_id]
    save_data()

def update_timetable(week_key, day, time_slot, worker_id, action='add'):
    if week_key not in st.session_state.timetable:
        st.session_state.timetable[week_key] = {}
    if day not in st.session_state.timetable[week_key]:
        st.session_state.timetable[week_key][day] = {}
    if time_slot not in st.session_state.timetable[week_key][day]:
        st.session_state.timetable[week_key][day][time_slot] = []
    
    if action == 'add':
        if worker_id not in st.session_state.timetable[week_key][day][time_slot]:
            st.session_state.timetable[week_key][day][time_slot].append(worker_id)
    elif action == 'remove':
        if worker_id in st.session_state.timetable[week_key][day][time_slot]:
            st.session_state.timetable[week_key][day][time_slot].remove(worker_id)
    
    save_data()

# Add manual save button in sidebar
def add_save_button():
    st.sidebar.markdown("---")
    if st.sidebar.button("💾 Save All Data"):
        if save_data():
            st.sidebar.success("Data saved successfully!")
        else:
            st.sidebar.error("Failed to save data")

# Rest of your existing UI code goes here...
# (Timetable, Worker Management, Order Management, Shop Jobs pages)

# Main title
st.title("🥩 David's Larder - Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Timetable & Rostering", "Worker Management", "Order Management", "New Order", "Shop Jobs"])

# Add save button to sidebar
add_save_button()

# In your existing code, replace direct session_state modifications with the new functions:
# Example in Worker Management page:
if page == "Worker Management":
    st.header("👥 Worker Management")
    
    # Add new worker - MODIFIED TO USE PERSISTENT FUNCTION
    with st.form("add_worker"):
        # ... your form fields
        if st.form_submit_button("Add Worker"):
            if new_name:
                new_worker = {
                    'id': max([w['id'] for w in st.session_state.workers]) + 1,
                    'name': new_name,
                    'position': new_position,
                    'availability': availability,
                    'unavailable_dates': [],
                    'hours_per_week': hours,
                    'skills': selected_skills
                }
                add_worker(new_worker)  # This now auto-saves
                st.success(f"Added {new_name} to workers!")
    
    # Remove worker - MODIFIED TO USE PERSISTENT FUNCTION
    for worker in st.session_state.workers:
        with st.expander(f"{worker['name']} - {worker['position']}"):
            if st.button(f"Remove {worker['name']}", key=f"remove_{worker['id']}"):
                remove_worker(worker['id'])  # This now auto-saves
                st.rerun()

# Similarly update all other pages to use the persistent functions
