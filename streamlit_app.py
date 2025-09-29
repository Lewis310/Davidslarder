
from openai import OpenAI
import streamlit as st
import pandas as pd
import datetime
import json
from datetime import datetime, timedelta
import uuid

# Page configuration
st.set_page_config(
    page_title="David's Larder - Management System",
    page_icon="🥩",
    layout="wide"
)

# Initialize session state
if 'workers' not in st.session_state:
    st.session_state.workers = [
        {
            'id': 1,
            'name': 'John MacLeod',
            'position': 'Butcher',
            'availability': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'unavailable_dates': [],
            'hours_per_week': 40
        },
        {
            'id': 2,
            'name': 'Sarah Campbell',
            'position': 'Shop Assistant',
            'availability': ['Tuesday', 'Wednesday', 'Thursday', 'Saturday'],
            'unavailable_dates': [],
            'hours_per_week': 30
        },
        {
            'id': 3,
            'name': 'Michael Fraser',
            'position': 'Butcher',
            'availability': ['Monday', 'Wednesday', 'Friday', 'Saturday'],
            'unavailable_dates': [],
            'hours_per_week': 35
        }
    ]

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {
            'order_id': 'ORD001',
            'customer_name': 'Highland Hotel',
            'items': ['10kg Pork Shoulder', '5kg Beef Mince', '3 Whole Chickens'],
            'due_date': datetime.now() + timedelta(days=2),
            'status': 'Pending'
        },
        {
            'order_id': 'ORD002',
            'customer_name': 'Local Cafe',
            'items': ['15kg Sausages', '8kg Bacon'],
            'due_date': datetime.now() + timedelta(days=5),
            'status': 'Pending'
        }
    ]

if 'timetable' not in st.session_state:
    st.session_state.timetable = {}

# Main title
st.title("🥩 David's Larder - Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Timetable & Rostering", "Worker Management", "Order Management", "New Order"])

# Timetable & Rostering Page
if page == "Timetable & Rostering":
    st.header("📅 Timetable & Worker Rostering")
    
    # Date selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now())
    with col2:
        end_date = st.date_input("End Date", datetime.now() + timedelta(days=6))
    
    # Generate timetable for the selected period
    if st.button("Generate Timetable"):
        current_date = start_date
        while current_date <= end_date:
            day_name = current_date.strftime('%A')
            if day_name not in st.session_state.timetable:
                st.session_state.timetable[day_name] = []
            current_date += timedelta(days=1)
    
    # Display timetable
    st.subheader("Weekly Timetable")
    
    # Create columns for each day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cols = st.columns(7)
    
    for i, day in enumerate(days):
        with cols[i]:
            st.write(f"**{day}**")
            if day in st.session_state.timetable:
                for worker_id in st.session_state.timetable[day]:
                    worker = next((w for w in st.session_state.workers if w['id'] == worker_id), None)
                    if worker:
                        st.write(f"• {worker['name']}")
            
            # Add worker to this day
            available_workers = [w for w in st.session_state.workers if day in w['availability']]
            worker_names = [f"{w['name']} ({w['position']})" for w in available_workers]
            
            if worker_names:
                selected_worker = st.selectbox(f"Add worker to {day}", [""] + worker_names, key=f"add_{day}")
                if selected_worker:
                    worker_name = selected_worker.split(" (")[0]
                    worker = next((w for w in available_workers if w['name'] == worker_name), None)
                    if worker and worker['id'] not in st.session_state.timetable.get(day, []):
                        if day not in st.session_state.timetable:
                            st.session_state.timetable[day] = []
                        st.session_state.timetable[day].append(worker['id'])
                        st.rerun()

# Worker Management Page
elif page == "Worker Management":
    st.header("👥 Worker Management")
    
    # Add new worker
    st.subheader("Add New Worker")
    with st.form("add_worker"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name")
            new_position = st.selectbox("Position", ["Butcher", "Shop Assistant", "Manager", "Cleaner"])
        with col2:
            availability = st.multiselect("Availability", 
                                        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            hours = st.number_input("Hours per Week", min_value=10, max_value=60, value=40)
        
        if st.form_submit_button("Add Worker"):
            if new_name:
                new_worker = {
                    'id': max([w['id'] for w in st.session_state.workers]) + 1,
                    'name': new_name,
                    'position': new_position,
                    'availability': availability,
                    'unavailable_dates': [],
                    'hours_per_week': hours
                }
                st.session_state.workers.append(new_worker)
                st.success(f"Added {new_name} to workers!")
    
    # Display current workers
    st.subheader("Current Workers")
    for worker in st.session_state.workers:
        with st.expander(f"{worker['name']} - {worker['position']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Availability:** {', '.join(worker['availability'])}")
                st.write(f"**Hours/Week:** {worker['hours_per_week']}")
            with col2:
                if st.button(f"Remove {worker['name']}", key=f"remove_{worker['id']}"):
                    st.session_state.workers = [w for w in st.session_state.workers if w['id'] != worker['id']]
                    st.rerun()

# Order Management Page
elif page == "Order Management":
    st.header("📋 Order Management")
    
    # Sort orders by due date
    sorted_orders = sorted(st.session_state.orders, key=lambda x: x['due_date'])
    
    # Display orders
    for order in sorted_orders:
        days_until = (order['due_date'] - datetime.now()).days
        status_color = "🟡" if order['status'] == 'Pending' else "🟢"
        
        with st.expander(f"{status_color} Order {order['order_id']} - {order['customer_name']} (Due in {days_until} days)"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Customer:** {order['customer_name']}")
                st.write(f"**Due Date:** {order['due_date'].strftime('%Y-%m-%d')}")
            with col2:
                st.write("**Items:**")
                for item in order['items']:
                    st.write(f"• {item}")
            with col3:
                st.write(f"**Status:** {order['status']}")
                if st.button(f"Mark Complete", key=f"complete_{order['order_id']}"):
                    order['status'] = 'Completed'
                    st.rerun()
                if st.button(f"Delete Order", key=f"delete_{order['order_id']}"):
                    st.session_state.orders = [o for o in st.session_state.orders if o['order_id'] != order['order_id']]
                    st.rerun()

# New Order Page
elif page == "New Order":
    st.header("🛒 New Customer Order")
    
    with st.form("new_order"):
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name")
            due_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))
        with col2:
            order_id = st.text_input("Order ID", value=f"ORD{len(st.session_state.orders) + 1:03d}")
        
        st.subheader("Order Items")
        items = st.text_area("Items (one per line)", 
                           placeholder="e.g., 5kg Beef Mince\n3 Whole Chickens\n2kg Pork Sausages")
        
        if st.form_submit_button("Create Order"):
            if customer_name and items:
                new_order = {
                    'order_id': order_id,
                    'customer_name': customer_name,
                    'items': [item.strip() for item in items.split('\n') if item.strip()],
                    'due_date': datetime.combine(due_date, datetime.min.time()),
                    'status': 'Pending'
                }
                st.session_state.orders.append(new_order)
                st.success(f"Order {order_id} created for {customer_name}!")
                
                # Clear form
                st.rerun()

# LLM Chat Bot Section
st.sidebar.markdown("---")
st.sidebar.header("💬 David's Larder Assistant")

# Simple chat interface
user_input = st.sidebar.text_input("Ask about workers, timetables, or orders:")

if user_input:
    # Simple response logic - in a real app, you'd integrate with an actual LLM
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['worker', 'staff', 'employee']):
        worker_names = [worker['name'] for worker in st.session_state.workers]
        st.sidebar.write(f"**Assistant:** We have {len(worker_names)} workers: {', '.join(worker_names)}")
    
    elif any(word in user_input_lower for word in ['timetable', 'roster', 'schedule']):
        st.sidebar.write("**Assistant:** You can view and manage the timetable in the 'Timetable & Rostering' section. I can help assign workers based on their availability.")
    
    elif any(word in user_input_lower for word in ['order', 'delivery']):
        pending_orders = [o for o in st.session_state.orders if o['status'] == 'Pending']
        st.sidebar.write(f"**Assistant:** We have {len(pending_orders)} pending orders. The next order is {pending_orders[0]['order_id']} for {pending_orders[0]['customer_name']}.")
    
    else:
        st.sidebar.write("**Assistant:** I can help you with worker management, timetables, and orders. Try asking about specific workers, the schedule, or upcoming orders.")

# Quick stats in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Stats")
st.sidebar.write(f"**Workers:** {len(st.session_state.workers)}")
st.sidebar.write(f"**Pending Orders:** {len([o for o in st.session_state.orders if o['status'] == 'Pending'])}")
st.sidebar.write(f"**Days in Timetable:** {len(st.session_state.timetable)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🥩 **David's Larder** - Scottish Butcher Shop")
