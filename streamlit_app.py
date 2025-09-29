import streamlit as st
import pandas as pd
import datetime
import json
from datetime import datetime, timedelta
import uuid
import random

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
            'hours_per_week': 40,
            'skills': ['meat_cutting', 'customer_service', 'ordering'],
            'color': '#FF6B6B'  # Red
        },
        {
            'id': 2,
            'name': 'Sarah Campbell',
            'position': 'Shop Assistant',
            'availability': ['Tuesday', 'Wednesday', 'Thursday', 'Saturday'],
            'unavailable_dates': [],
            'hours_per_week': 30,
            'skills': ['customer_service', 'packaging', 'cleaning'],
            'color': '#4ECDC4'  # Teal
        },
        {
            'id': 3,
            'name': 'Michael Fraser',
            'position': 'Butcher',
            'availability': ['Monday', 'Wednesday', 'Friday', 'Saturday'],
            'unavailable_dates': [],
            'hours_per_week': 35,
            'skills': ['meat_cutting', 'preparation', 'quality_control'],
            'color': '#45B7D1'  # Blue
        },
        {
            'id': 4,
            'name': 'Emma Wilson',
            'position': 'Shop Assistant',
            'availability': ['Monday', 'Tuesday', 'Friday', 'Saturday'],
            'unavailable_dates': [],
            'hours_per_week': 25,
            'skills': ['customer_service', 'cash_handling', 'cleaning'],
            'color': '#96CEB4'  # Green
        }
    ]

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {
            'order_id': 'ORD001',
            'customer_name': 'Highland Hotel',
            'customer_contact': '01463 123456',
            'customer_email': 'manager@highlandhotel.com',
            'items': [
                {'name': 'Pork Shoulder', 'quantity': 10, 'unit': 'kg', 'notes': 'Boneless'},
                {'name': 'Beef Mince', 'quantity': 5, 'unit': 'kg', 'notes': 'Lean'},
                {'name': 'Whole Chickens', 'quantity': 3, 'unit': 'each', 'notes': 'Size 1.5kg each'}
            ],
            'total_price': 285.50,
            'due_date': datetime.now() + timedelta(days=2),
            'status': 'Pending',
            'priority': 'High',
            'notes': 'Deliver to back entrance before 10 AM',
            'created_date': datetime.now() - timedelta(days=1)
        },
        {
            'order_id': 'ORD002',
            'customer_name': 'Local Cafe',
            'customer_contact': '01463 654321',
            'customer_email': 'orders@localcafe.com',
            'items': [
                {'name': 'Sausages', 'quantity': 15, 'unit': 'kg', 'notes': 'Pork and herb'},
                {'name': 'Bacon', 'quantity': 8, 'unit': 'kg', 'notes': 'Smoked back bacon'}
            ],
            'total_price': 192.75,
            'due_date': datetime.now() + timedelta(days=5),
            'status': 'In Progress',
            'priority': 'Medium',
            'notes': 'Will collect at 8:30 AM',
            'created_date': datetime.now() - timedelta(days=2)
        },
        {
            'order_id': 'ORD003',
            'customer_name': 'River Restaurant',
            'customer_contact': '01463 789012',
            'customer_email': 'chef@riverrestaurant.com',
            'items': [
                {'name': 'Lamb Legs', 'quantity': 4, 'unit': 'each', 'notes': 'Butterflied'},
                {'name': 'Beef Ribeye', 'quantity': 12, 'unit': 'kg', 'notes': 'Aged 28 days'},
                {'name': 'Chicken Breasts', 'quantity': 6, 'unit': 'kg', 'notes': 'Skinless'}
            ],
            'total_price': 420.00,
            'due_date': datetime.now() + timedelta(days=1),
            'status': 'Pending',
            'priority': 'High',
            'notes': 'Urgent - for weekend event',
            'created_date': datetime.now()
        }
    ]

if 'timetable' not in st.session_state:
    st.session_state.timetable = {}

if 'shop_jobs' not in st.session_state:
    st.session_state.shop_jobs = {
        'Monday': {
            'morning': ['meat_preparation', 'display_setup', 'order_receiving'],
            'afternoon': ['customer_service', 'cleaning', 'inventory_check'],
            'evening': ['closing_duties', 'equipment_cleaning']
        },
        'Tuesday': {
            'morning': ['butchery_work', 'display_refresh', 'supplier_meeting'],
            'afternoon': ['customer_service', 'special_orders', 'training'],
            'evening': ['closing_duties', 'waste_management']
        },
        'Wednesday': {
            'morning': ['bulk_preparation', 'quality_checks', 'marketing_prep'],
            'afternoon': ['customer_service', 'online_orders', 'cleaning'],
            'evening': ['closing_duties', 'weekly_ordering']
        },
        'Thursday': {
            'morning': ['specialty_cuts', 'display_setup', 'supplier_delivery'],
            'afternoon': ['customer_service', 'event_preparation', 'staff_meeting'],
            'evening': ['closing_duties', 'deep_cleaning']
        },
        'Friday': {
            'morning': ['weekend_prep', 'bulk_butchery', 'display_setup'],
            'afternoon': ['customer_service', 'rush_hours', 'quality_control'],
            'evening': ['closing_duties', 'weekly_review']
        },
        'Saturday': {
            'morning': ['opening_duties', 'fresh_display', 'customer_service'],
            'afternoon': ['busy_shift', 'quick_restock', 'customer_service'],
            'evening': ['early_closing', 'weekly_cleanup']
        },
        'Sunday': {
            'morning': ['closed'],
            'afternoon': ['closed'],
            'evening': ['closed']
        }
    }

if 'job_descriptions' not in st.session_state:
    st.session_state.job_descriptions = {
        'meat_preparation': 'Preparing daily meat cuts and portions for display',
        'display_setup': 'Setting up attractive meat displays in shop front',
        'order_receiving': 'Receiving and processing supplier deliveries',
        'customer_service': 'Assisting customers, taking orders, handling payments',
        'cleaning': 'Maintaining cleanliness standards throughout shop',
        'inventory_check': 'Checking stock levels and recording inventory',
        'closing_duties': 'Securing shop, cash handling, end-of-day procedures',
        'equipment_cleaning': 'Deep cleaning of butchery equipment',
        'butchery_work': 'Primary butchery work on larger cuts',
        'display_refresh': 'Refreshing and rotating display items',
        'supplier_meeting': 'Meeting with meat suppliers',
        'special_orders': 'Handling custom orders and special requests',
        'training': 'Staff training and skill development',
        'bulk_preparation': 'Preparing bulk orders for restaurants/hotels',
        'quality_checks': 'Quality control on all meat products',
        'marketing_prep': 'Preparing for promotions and marketing',
        'online_orders': 'Processing and packing online orders',
        'weekly_ordering': 'Placing weekly orders with suppliers',
        'specialty_cuts': 'Creating specialty cuts and value-added products',
        'event_preparation': 'Preparing for local events/festivals',
        'staff_meeting': 'Weekly staff coordination meeting',
        'deep_cleaning': 'Thorough cleaning of entire shop',
        'weekend_prep': 'Extra preparation for busy weekend trade',
        'bulk_butchery': 'Butchery work for weekend demand',
        'rush_hours': 'Extra staff during busy periods',
        'weekly_review': 'Reviewing week performance and planning',
        'opening_duties': 'Morning opening procedures',
        'fresh_display': 'Setting up fresh daily displays',
        'busy_shift': 'Handling Saturday customer volume',
        'quick_restock': 'Rapid restocking during busy periods',
        'early_closing': 'Saturday early closing procedures',
        'weekly_cleanup': 'Major weekly cleaning',
        'waste_management': 'Managing food waste and recycling'
    }

# Main title
st.title("🥩 David's Larder - Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Timetable & Rostering", "Worker Management", "Order Management", "New Order", "Shop Jobs"])

# Helper function to create time slots
def create_time_slots():
    times = []
    for hour in range(6, 23):  # 6 AM to 10 PM
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            times.append(time_str)
    return times

# Helper function to generate order ID
def generate_order_id():
    return f"ORD{len(st.session_state.orders) + 1:03d}"

# Helper function to get worker color
def get_worker_color(worker_id):
    worker = next((w for w in st.session_state.workers if w['id'] == worker_id), None)
    return worker['color'] if worker and 'color' in worker else '#CCCCCC'

# Enhanced Timetable & Rostering Page with color blocks
if page == "Timetable & Rostering":
    st.header("📅 Timetable & Worker Rostering")
    
    # Week selection
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("Select Week Starting", datetime.now())
    
    # Calculate week dates
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Time slots
    time_slots = create_time_slots()
    
    # Create weekly timetable
    st.subheader(f"Weekly Timetable: {start_of_week.strftime('%d %b %Y')} - {(start_of_week + timedelta(days=6)).strftime('%d %b %Y')}")
    
    # Initialize timetable for the week if not exists
    week_key = start_of_week.strftime('%Y-%W')
    if week_key not in st.session_state.timetable:
        st.session_state.timetable[week_key] = {}
        for day in days:
            st.session_state.timetable[week_key][day] = {}
            for time_slot in time_slots:
                st.session_state.timetable[week_key][day][time_slot] = []
    
    # Display timetable as a grid with color blocks
    timetable_data = []
    for time_slot in time_slots:
        row = {'Time': time_slot}
        for i, day in enumerate(days):
            date_str = week_dates[i].strftime('%d/%m')
            workers_at_slot = st.session_state.timetable[week_key][day].get(time_slot, [])
            
            # Create color blocks HTML
            if workers_at_slot:
                color_blocks = ""
                for worker_id in workers_at_slot:
                    color = get_worker_color(worker_id)
                    worker = next((w for w in st.session_state.workers if w['id'] == worker_id), None)
                    initials = ''.join([name[0] for name in worker['name'].split()]) if worker else "?"
                    color_blocks += f'<span style="background-color: {color}; color: white; padding: 2px 6px; margin: 1px; border-radius: 3px; font-size: 0.8em;" title="{worker["name"] if worker else "Unknown"}">{initials}</span>'
                row[f"{day} {date_str}"] = color_blocks
            else:
                row[f"{day} {date_str}"] = ""
        timetable_data.append(row)
    
    df = pd.DataFrame(timetable_data)
    
    # Display the dataframe with HTML rendering
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # Worker color legend
    st.subheader("Worker Color Legend")
    col_legend = st.columns(4)
    for idx, worker in enumerate(st.session_state.workers):
        with col_legend[idx % 4]:
            st.markdown(
                f'<span style="background-color: {worker["color"]}; color: white; padding: 5px 10px; border-radius: 5px; display: inline-block; margin: 2px;">{worker["name"]}</span>',
                unsafe_allow_html=True
            )
    
    # Shift assignment interface
    st.subheader("Assign Shifts")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_day = st.selectbox("Day", days)
    with col2:
        selected_worker = st.selectbox("Worker", 
                                     [f"{w['name']} ({w['position']})" for w in st.session_state.workers])
    with col3:
        start_time = st.selectbox("Start Time", time_slots, index=16)  # Default to 9:00
    with col4:
        end_time = st.selectbox("End Time", time_slots, index=22)  # Default to 12:00
    
    if st.button("Assign Shift"):
        if selected_worker and start_time and end_time:
            worker_name = selected_worker.split(" (")[0]
            worker = next((w for w in st.session_state.workers if w['name'] == worker_name), None)
            
            if worker:
                # Convert time slots to indices
                start_idx = time_slots.index(start_time)
                end_idx = time_slots.index(end_time)
                
                # Assign worker to all time slots in the shift
                for i in range(start_idx, end_idx + 1):
                    current_slot = time_slots[i]
                    if worker['id'] not in st.session_state.timetable[week_key][selected_day][current_slot]:
                        st.session_state.timetable[week_key][selected_day][current_slot].append(worker['id'])
                
                st.success(f"Assigned {worker_name} to {selected_day} from {start_time} to {end_time}")
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
        
        # Skills selection
        all_skills = list(set([skill for worker in st.session_state.workers for skill in worker.get('skills', [])] + 
                             list(st.session_state.job_descriptions.keys())))
        selected_skills = st.multiselect("Skills", all_skills)
        
        # Color selection
        color_options = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        selected_color = st.selectbox("Color for Timetable", color_options)
        
        if st.form_submit_button("Add Worker"):
            if new_name:
                new_worker = {
                    'id': max([w['id'] for w in st.session_state.workers]) + 1,
                    'name': new_name,
                    'position': new_position,
                    'availability': availability,
                    'unavailable_dates': [],
                    'hours_per_week': hours,
                    'skills': selected_skills,
                    'color': selected_color
                }
                st.session_state.workers.append(new_worker)
                st.success(f"Added {new_name} to workers!")
    
    # Display current workers
    st.subheader("Current Workers")
    for worker in st.session_state.workers:
        with st.expander(f"{worker['name']} - {worker['position']}"):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**Availability:** {', '.join(worker['availability'])}")
                st.write(f"**Hours/Week:** {worker['hours_per_week']}")
                st.write(f"**Skills:** {', '.join(worker.get('skills', []))}")
            with col2:
                st.markdown(f"**Color:** <span style='background-color: {worker['color']}; padding: 5px 10px; border-radius: 5px; color: white;'>{worker['color']}</span>", unsafe_allow_html=True)
            with col3:
                if st.button(f"Remove", key=f"remove_{worker['id']}"):
                    st.session_state.workers = [w for w in st.session_state.workers if w['id'] != worker['id']]
                    st.rerun()

# Enhanced Order Management Page
elif page == "Order Management":
    st.header("📦 Order Management")
    
    # Order filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed", "Cancelled"])
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col3:
        days_filter = st.selectbox("Due Within", ["All", "Today", "Next 2 Days", "This Week"])
    
    # Filter orders
    filtered_orders = st.session_state.orders.copy()
    
    if status_filter != "All":
        filtered_orders = [o for o in filtered_orders if o['status'] == status_filter]
    
    if priority_filter != "All":
        filtered_orders = [o for o in filtered_orders if o['priority'] == priority_filter]
    
    if days_filter != "All":
        today = datetime.now().date()
        if days_filter == "Today":
            filtered_orders = [o for o in filtered_orders if o['due_date'].date() == today]
        elif days_filter == "Next 2 Days":
            filtered_orders = [o for o in filtered_orders if o['due_date'].date() <= today + timedelta(days=2)]
        elif days_filter == "This Week":
            end_of_week = today + timedelta(days=(6 - today.weekday()))
            filtered_orders = [o for o in filtered_orders if o['due_date'].date() <= end_of_week]
    
    # Display orders
    st.subheader(f"Orders ({len(filtered_orders)} found)")
    
    for order in filtered_orders:
        with st.expander(f"📦 {order['order_id']} - {order['customer_name']} - Due: {order['due_date'].strftime('%d/%m/%Y')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Customer:** {order['customer_name']}")
                st.write(f"**Contact:** {order['customer_contact']}")
                st.write(f"**Email:** {order['customer_email']}")
                st.write(f"**Priority:** {order['priority']}")
                st.write(f"**Created:** {order['created_date'].strftime('%d/%m/%Y %H:%M')}")
                
            with col2:
                st.write(f"**Due Date:** {order['due_date'].strftime('%d/%m/%Y')}")
                st.write(f"**Status:** {order['status']}")
                st.write(f"**Total Price:** £{order['total_price']:.2f}")
                st.write(f"**Notes:** {order.get('notes', 'None')}")
            
            # Order items
            st.write("**Items:**")
            for item in order['items']:
                st.write(f"- {item['quantity']} {item['unit']} {item['name']} ({item.get('notes', 'No notes')})")
            
            # Order actions
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                new_status = st.selectbox("Update Status", 
                                        ["Pending", "In Progress", "Completed", "Cancelled"],
                                        index=["Pending", "In Progress", "Completed", "Cancelled"].index(order['status']),
                                        key=f"status_{order['order_id']}")
                if st.button("Update Status", key=f"update_{order['order_id']}"):
                    order['status'] = new_status
                    st.success(f"Updated {order['order_id']} status to {new_status}")
                    st.rerun()
            
            with col2:
                if st.button("Mark Complete", key=f"complete_{order['order_id']}"):
                    order['status'] = 'Completed'
                    st.success(f"Marked {order['order_id']} as completed")
                    st.rerun()
            
            with col3:
                if st.button("Duplicate Order", key=f"duplicate_{order['order_id']}"):
                    new_order = order.copy()
                    new_order['order_id'] = generate_order_id()
                    new_order['created_date'] = datetime.now()
                    new_order['status'] = 'Pending'
                    st.session_state.orders.append(new_order)
                    st.success(f"Duplicated order as {new_order['order_id']}")
                    st.rerun()
            
            with col4:
                if st.button("Delete Order", key=f"delete_{order['order_id']}"):
                    st.session_state.orders = [o for o in st.session_state.orders if o['order_id'] != order['order_id']]
                    st.success(f"Deleted order {order['order_id']}")
                    st.rerun()

# Enhanced New Order Page
elif page == "New Order":
    st.header("🆕 Create New Order")
    
    with st.form("new_order"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name*")
            customer_contact = st.text_input("Contact Number*")
            customer_email = st.text_input("Email Address")
            priority = st.selectbox("Priority*", ["High", "Medium", "Low"])
            
        with col2:
            due_date = st.date_input("Due Date*", datetime.now() + timedelta(days=1))
            due_time = st.time_input("Due Time", datetime.now().time())
            notes = st.text_area("Order Notes")
        
        # Order items
        st.subheader("Order Items")
        items = []
        
        with st.container():
            st.write("Add items to the order:")
            num_items = st.number_input("Number of Items", min_value=1, max_value=20, value=1)
            
            for i in range(num_items):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
                with col1:
                    item_name = st.text_input(f"Item Name {i+1}", key=f"name_{i}")
                with col2:
                    quantity = st.number_input(f"Qty {i+1}", min_value=0.1, value=1.0, step=0.1, key=f"qty_{i}")
                with col3:
                    unit = st.selectbox(f"Unit {i+1}", ["kg", "g", "each", "pack"], key=f"unit_{i}")
                with col4:
                    item_notes = st.text_input(f"Notes {i+1}", key=f"notes_{i}")
                
                if item_name:
                    items.append({
                        'name': item_name,
                        'quantity': quantity,
                        'unit': unit,
                        'notes': item_notes
                    })
        
        if st.form_submit_button("Create Order"):
            if customer_name and customer_contact and items:
                # Calculate total price (simplified - in real app you'd have price lists)
                base_price_per_kg = 15.0  # Example base price
                total_price = sum(item['quantity'] * base_price_per_kg for item in items)
                
                new_order = {
                    'order_id': generate_order_id(),
                    'customer_name': customer_name,
                    'customer_contact': customer_contact,
                    'customer_email': customer_email,
                    'items': items,
                    'total_price': total_price,
                    'due_date': datetime.combine(due_date, due_time),
                    'status': 'Pending',
                    'priority': priority,
                    'notes': notes,
                    'created_date': datetime.now()
                }
                
                st.session_state.orders.append(new_order)
                st.success(f"✅ Order {new_order['order_id']} created successfully!")
                st.balloons()
                
                # Show order summary
                st.subheader("Order Summary")
                st.json(new_order)
            else:
                st.error("Please fill in all required fields (marked with *) and add at least one item.")

# Shop Jobs Page (unchanged)
elif page == "Shop Jobs":
    st.header("🏪 Daily Shop Jobs & Tasks")
    
    tab1, tab2, tab3 = st.tabs(["View Daily Jobs", "Modify Jobs", "Job Descriptions"])
    
    with tab1:
        st.subheader("Daily Job Schedule")
        selected_day = st.selectbox("Select Day", list(st.session_state.shop_jobs.keys()))
        
        if selected_day:
            day_jobs = st.session_state.shop_jobs[selected_day]
            for time_period, jobs in day_jobs.items():
                with st.expander(f"{time_period.title()} Jobs"):
                    for job in jobs:
                        description = st.session_state.job_descriptions.get(job, "No description available")
                        st.write(f"**{job.replace('_', ' ').title()}**: {description}")
    
    with tab2:
        st.subheader("Modify Daily Jobs")
        
        col1, col2 = st.columns(2)
        with col1:
            modify_day = st.selectbox("Day to Modify", list(st.session_state.shop_jobs.keys()), key="modify_day")
            time_period = st.selectbox("Time Period", ["morning", "afternoon", "evening"])
        with col2:
            action = st.radio("Action", ["Add Job", "Remove Job"])
            
            if action == "Add Job":
                new_job = st.text_input("New Job Name")
                new_description = st.text_area("Job Description")
                
                if st.button("Add Job") and new_job:
                    job_key = new_job.lower().replace(' ', '_')
                    if time_period not in st.session_state.shop_jobs[modify_day]:
                        st.session_state.shop_jobs[modify_day][time_period] = []
                    st.session_state.shop_jobs[modify_day][time_period].append(job_key)
                    st.session_state.job_descriptions[job_key] = new_description
                    st.success(f"Added {new_job} to {modify_day} {time_period}")
            
            else:
                existing_jobs = st.session_state.shop_jobs[modify_day].get(time_period, [])
                if existing_jobs:
                    job_to_remove = st.selectbox("Select Job to Remove", existing_jobs)
                    if st.button("Remove Job"):
                        st.session_state.shop_jobs[modify_day][time_period].remove(job_to_remove)
                        st.success(f"Removed {job_to_remove} from {modify_day} {time_period}")
    
    with tab3:
        st.subheader("Job Descriptions")
        for job, description in st.session_state.job_descriptions.items():
            with st.expander(job.replace('_', ' ').title()):
                st.write(description)

# Enhanced LLM Chat Bot Section with shop job knowledge
st.sidebar.markdown("---")
st.sidebar.header("💬 David's Larder Assistant")

# Simple chat interface
user_input = st.sidebar.text_input("Ask about workers, timetables, orders, or shop jobs:")

if user_input:
    user_input_lower = user_input.lower()
    
    # Enhanced response logic with shop job knowledge
    if any(word in user_input_lower for word in ['worker', 'staff', 'employee']):
        worker_names = [worker['name'] for worker in st.session_state.workers]
        st.sidebar.write(f"**Assistant:** We have {len(worker_names)} workers: {', '.join(worker_names)}")
    
    elif any(word in user_input_lower for word in ['timetable', 'roster', 'schedule']):
        st.sidebar.write("**Assistant:** You can view and manage the detailed timetable with specific time slots in the 'Timetable & Rostering' section.")
    
    elif any(word in user_input_lower for word in ['order', 'delivery']):
        pending_orders = [o for o in st.session_state.orders if o['status'] == 'Pending']
        high_priority_orders = [o for o in st.session_state.orders if o['priority'] == 'High' and o['status'] != 'Completed']
        
        if high_priority_orders:
            next_order = high_priority_orders[0]
            st.sidebar.write(f"**Assistant:** We have {len(high_priority_orders)} high priority orders. Next urgent: {next_order['order_id']} for {next_order['customer_name']} due {next_order['due_date'].strftime('%A')}.")
        elif pending_orders:
            next_order = pending_orders[0]
            st.sidebar.write(f"**Assistant:** We have {len(pending_orders)} pending orders. Next: {next_order['order_id']} for {next_order['customer_name']} due {next_order['due_date'].strftime('%A')}.")
        else:
            st.sidebar.write("**Assistant:** No pending orders at the moment.")
    
    elif any(word in user_input_lower for word in ['job', 'task', 'work', 'duty']):
        if 'today' in user_input_lower:
            today = datetime.now().strftime('%A')
            jobs_today = st.session_state.shop_jobs.get(today, {})
            response = f"**Assistant:** Today's ({today}) jobs:\n"
            for period, jobs in jobs_today.items():
                response += f"\n{period.title()}: {', '.join([j.replace('_', ' ').title() for j in jobs])}"
            st.sidebar.write(response)
        elif any(day in user_input_lower for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']):
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                if day in user_input_lower:
                    jobs_day = st.session_state.shop_jobs.get(day.capitalize(), {})
                    response = f"**Assistant:** {day.capitalize()}'s jobs:\n"
                    for period, jobs in jobs_day.items():
                        response += f"\n{period.title()}: {', '.join([j.replace('_', ' ').title() for j in jobs])}"
                    st.sidebar.write(response)
                    break
        else:
            st.sidebar.write("**Assistant:** I can tell you about daily shop jobs. Ask about specific days or 'today's jobs'. You can also modify jobs in the 'Shop Jobs' section.")
    
    else:
        st.sidebar.write("**Assistant:** I can help you with worker management, timetables, orders, and daily shop jobs. Try asking about today's tasks or worker schedules.")

# Quick stats in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Stats")
st.sidebar.write(f"**Workers:** {len(st.session_state.workers)}")
st.sidebar.write(f"**Pending Orders:** {len([o for o in st.session_state.orders if o['status'] == 'Pending'])}")
st.sidebar.write(f"**High Priority:** {len([o for o in st.session_state.orders if o['priority'] == 'High' and o['status'] != 'Completed'])}")
st.sidebar.write(f"**Shop Jobs:** {len(st.session_state.job_descriptions)} defined")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🥩 **David's Larder** - Scottish Butcher Shop")
