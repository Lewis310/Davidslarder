import streamlit as st
import pandas as pd
import datetime
import json
import os
import random
from datetime import datetime, timedelta
import uuid

# Page configuration
st.set_page_config(
    page_title="David's Larder - Management System",
    page_icon="🥩",
    layout="wide"
)

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Data persistence functions
def save_data():
    """Save all session data to JSON file"""
    try:
        # Convert datetime objects to strings for JSON serialization
        orders_serializable = []
        for order in st.session_state.orders:
            order_copy = order.copy()
            # Handle due_date
            if 'due_date' in order_copy and isinstance(order_copy['due_date'], datetime):
                order_copy['due_date'] = order_copy['due_date'].isoformat()
            
            # Handle created_date
            if 'created_date' in order_copy and isinstance(order_copy['created_date'], datetime):
                order_copy['created_date'] = order_copy['created_date'].isoformat()
            
            orders_serializable.append(order_copy)
        
        data = {
            'workers': st.session_state.workers,
            'orders': orders_serializable,
            'timetable': st.session_state.timetable,
            'shop_jobs': st.session_state.shop_jobs,
            'job_descriptions': st.session_state.job_descriptions,
            'worker_colors': st.session_state.worker_colors
        }
        
        with open('davids_larder_data.json', 'w') as f:
            json.dump(data, f, cls=DateTimeEncoder, indent=2)
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
                    try:
                        order['due_date'] = datetime.fromisoformat(order['due_date'])
                    except ValueError:
                        # If ISO format fails, try other formats or set to now
                        order['due_date'] = datetime.now()
                
                if 'created_date' in order and isinstance(order['created_date'], str):
                    try:
                        order['created_date'] = datetime.fromisoformat(order['created_date'])
                    except ValueError:
                        order['created_date'] = datetime.now()
            
            return data
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return None

# Helper function to create time slots (7:30 AM to 6:00 PM)
def create_time_slots():
    times = []
    for hour in range(7, 19):  # 7 AM to 6 PM
        for minute in [0, 30]:
            # Skip times before 7:30 AM
            if hour == 7 and minute == 0:
                continue
            # Stop at 6:00 PM
            if hour == 18 and minute == 30:
                break
            time_str = f"{hour:02d}:{minute:02d}"
            times.append(time_str)
    return times

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
            },
            {
                'id': 3,
                'name': 'Michael Fraser',
                'position': 'Butcher',
                'availability': ['Monday', 'Wednesday', 'Friday', 'Saturday'],
                'unavailable_dates': [],
                'hours_per_week': 35,
                'skills': ['meat_cutting', 'preparation', 'quality_control']
            }
        ],
        'orders': [
            {
                'order_id': 'ORD001',
                'customer_name': 'Highland Hotel',
                'items': ['10kg Pork Shoulder', '5kg Beef Mince', '3 Whole Chickens'],
                'due_date': datetime.now() + timedelta(days=2),
                'status': 'Pending',
                'priority': 'High',
                'created_date': datetime.now() - timedelta(days=1)
            },
            {
                'order_id': 'ORD002',
                'customer_name': 'Local Cafe',
                'items': ['15kg Sausages', '8kg Bacon'],
                'due_date': datetime.now() + timedelta(days=5),
                'status': 'In Progress',
                'priority': 'Medium',
                'created_date': datetime.now() - timedelta(days=2)
            }
        ],
        'timetable': {},
        'shop_jobs': {
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
        },
        'job_descriptions': {
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
        },
        'worker_colors': {}
    }
    
    # Load saved data or use defaults
    saved_data = load_data()
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            if saved_data and key in saved_data:
                st.session_state[key] = saved_data[key]
            else:
                st.session_state[key] = default_value
    
    # Generate colors for workers if not exists
    if not st.session_state.worker_colors:
        colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
            '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2'
        ]
        for i, worker in enumerate(st.session_state.workers):
            st.session_state.worker_colors[worker['id']] = colors[i % len(colors)]

# Initialize the session state
initialize_session_state()

# Enhanced functions with auto-save
def add_worker(worker_data):
    st.session_state.workers.append(worker_data)
    # Generate a color for the new worker
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    used_colors = list(st.session_state.worker_colors.values())
    available_colors = [c for c in colors if c not in used_colors]
    if available_colors:
        st.session_state.worker_colors[worker_data['id']] = available_colors[0]
    else:
        st.session_state.worker_colors[worker_data['id']] = f"hsl({random.randint(0, 360)}, 70%, 80%)"
    save_data()

def remove_worker(worker_id):
    st.session_state.workers = [w for w in st.session_state.workers if w['id'] != worker_id]
    if worker_id in st.session_state.worker_colors:
        del st.session_state.worker_colors[worker_id]
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

def update_order_priority(order_id, priority):
    for order in st.session_state.orders:
        if order['order_id'] == order_id:
            order['priority'] = priority
            break
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

def remove_shift(week_key, day, worker_id):
    """Remove all shifts for a worker on a specific day"""
    if week_key in st.session_state.timetable and day in st.session_state.timetable[week_key]:
        for time_slot in st.session_state.timetable[week_key][day]:
            if worker_id in st.session_state.timetable[week_key][day][time_slot]:
                st.session_state.timetable[week_key][day][time_slot].remove(worker_id)
        save_data()

# Visual timetable functions
def create_visual_timetable(week_key, days, time_slots, week_dates):
    """Create a visual timetable with colored blocks"""
    st.subheader("📊 Weekly Timetable")
    
    # Create a container for the timetable
    timetable_container = st.container()
    
    with timetable_container:
        # Create columns for each day
        cols = st.columns(len(days))
        
        for i, (day, col) in enumerate(zip(days, cols)):
            with col:
                date_str = week_dates[i].strftime('%d/%m')
                st.write(f"**{day}**")
                st.write(f"*{date_str}*")
                
                # Get all shifts for this day
                day_shifts = {}
                for time_slot in time_slots:
                    workers = st.session_state.timetable[week_key][day].get(time_slot, [])
                    for worker_id in workers:
                        if worker_id not in day_shifts:
                            day_shifts[worker_id] = []
                        day_shifts[worker_id].append(time_slot)
                
                # Group consecutive time slots into shifts
                shifts_by_worker = {}
                for worker_id, slots in day_shifts.items():
                    if slots:
                        slots.sort()
                        shifts = []
                        current_shift = [slots[0]]
                        
                        for j in range(1, len(slots)):
                            current_time = datetime.strptime(slots[j], '%H:%M')
                            prev_time = datetime.strptime(slots[j-1], '%H:%M')
                            # If times are consecutive (30 min difference)
                            if (current_time - prev_time).seconds == 1800:  # 30 minutes in seconds
                                current_shift.append(slots[j])
                            else:
                                shifts.append(current_shift)
                                current_shift = [slots[j]]
                        
                        shifts.append(current_shift)
                        shifts_by_worker[worker_id] = shifts
                
                # Display shifts as colored blocks
                if shifts_by_worker:
                    for worker_id, shifts in shifts_by_worker.items():
                        worker = next((w for w in st.session_state.workers if w['id'] == worker_id), None)
                        if worker:
                            color = st.session_state.worker_colors.get(worker_id, '#CCCCCC')
                            for shift in shifts:
                                if len(shift) > 1:
                                    shift_text = f"{shift[0]} - {shift[-1]}"
                                else:
                                    shift_text = f"{shift[0]}"
                                
                                # Create a colored block with remove button
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    st.markdown(
                                        f"""<div style="background-color: {color}; 
                                        padding: 8px; margin: 2px 0; border-radius: 4px; 
                                        color: black; font-weight: bold; font-size: 12px;">
                                        {worker['name']}<br>{shift_text}
                                        </div>""", 
                                        unsafe_allow_html=True
                                    )
                                with col2:
                                    if st.button("❌", key=f"remove_{day}_{worker_id}_{shift[0]}", help=f"Remove {worker['name']}'s shift"):
                                        # Remove this specific shift
                                        for time_slot in shift:
                                            update_timetable(week_key, day, time_slot, worker_id, 'remove')
                                        st.rerun()
                else:
                    st.info("No shifts")
                
                # Add quick remove all for this worker on this day
                if shifts_by_worker:
                    st.markdown("---")
                    for worker_id in shifts_by_worker.keys():
                        worker = next((w for w in st.session_state.workers if w['id'] == worker_id), None)
                        if worker:
                            if st.button(f"Remove all {worker['name']}'s shifts", key=f"remove_all_{day}_{worker_id}"):
                                remove_shift(week_key, day, worker_id)
                                st.rerun()

# Main title
st.title("🥩 David's Larder - Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Timetable & Rostering", "Worker Management", "Order Management", "New Order", "Shop Jobs"])

# Add save button to sidebar
st.sidebar.markdown("---")
if st.sidebar.button("💾 Save All Data"):
    if save_data():
        st.sidebar.success("Data saved successfully!")
    else:
        st.sidebar.error("Failed to save data")

# Add data reset option
st.sidebar.markdown("---")
st.sidebar.subheader("Data Management")
if st.sidebar.button("🔄 Reset Data File"):
    if os.path.exists('davids_larder_data.json'):
        os.remove('davids_larder_data.json')
        st.sidebar.success("Data file reset! Please refresh the page.")
        st.stop()

# Enhanced Timetable & Rostering Page
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
    
    # Time slots (7:30 AM to 6:00 PM)
    time_slots = create_time_slots()
    
    # Initialize timetable for the week if not exists
    week_key = start_of_week.strftime('%Y-%W')
    if week_key not in st.session_state.timetable:
        st.session_state.timetable[week_key] = {}
        for day in days:
            st.session_state.timetable[week_key][day] = {}
            for time_slot in time_slots:
                st.session_state.timetable[week_key][day][time_slot] = []
    
    # Create visual timetable
    create_visual_timetable(week_key, days, time_slots, week_dates)
    
    # Shift assignment interface
    st.subheader("➕ Assign New Shifts")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_day = st.selectbox("Day", days)
    with col2:
        selected_worker = st.selectbox("Worker", 
                                     [f"{w['name']} ({w['position']})" for w in st.session_state.workers])
    with col3:
        start_time = st.selectbox("Start Time", time_slots, index=0)  # Default to 7:30 AM
    with col4:
        end_time = st.selectbox("End Time", time_slots, index=len(time_slots)-1)  # Default to 6:00 PM
    
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
                    update_timetable(week_key, selected_day, current_slot, worker['id'], 'add')
                
                st.success(f"Assigned {worker_name} to {selected_day} from {start_time} to {end_time}")
                st.rerun()

# Worker Management Page
elif page == "Worker Management":
    st.header("👥 Worker Management")
    
    # Display worker color legend
    st.subheader("Worker Color Legend")
    cols = st.columns(len(st.session_state.workers))
    for i, worker in enumerate(st.session_state.workers):
        with cols[i]:
            color = st.session_state.worker_colors.get(worker['id'], '#CCCCCC')
            st.markdown(
                f"""<div style="background-color: {color}; padding: 10px; 
                border-radius: 5px; text-align: center; color: black; font-weight: bold;">
                {worker['name']}
                </div>""", 
                unsafe_allow_html=True
            )
    
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
                add_worker(new_worker)
                st.success(f"Added {new_name} to workers!")
    
    # Display current workers
    st.subheader("Current Workers")
    for worker in st.session_state.workers:
        with st.expander(f"{worker['name']} - {worker['position']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Availability:** {', '.join(worker['availability'])}")
                st.write(f"**Hours/Week:** {worker['hours_per_week']}")
                st.write(f"**Skills:** {', '.join(worker.get('skills', []))}")
            with col2:
                if st.button(f"Remove {worker['name']}", key=f"remove_{worker['id']}"):
                    remove_worker(worker['id'])
                    st.rerun()

# Order Management Page
elif page == "Order Management":
    st.header("📋 Order Management")
    
    # Order filtering and sorting
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All", "Pending", "In Progress", "Completed", "Cancelled"])
    with col2:
        priority_filter = st.selectbox("Filter by Priority", 
                                     ["All", "High", "Medium", "Low"])
    with col3:
        sort_by = st.selectbox("Sort by", 
                             ["Due Date (Ascending)", "Due Date (Descending)", "Priority", "Date Created"])
    
    # Filter orders
    filtered_orders = st.session_state.orders.copy()
    
    if status_filter != "All":
        filtered_orders = [o for o in filtered_orders if o['status'] == status_filter]
    
    if priority_filter != "All":
        filtered_orders = [o for o in filtered_orders if o.get('priority', 'Medium') == priority_filter]
    
    # Sort orders
    if sort_by == "Due Date (Ascending)":
        filtered_orders.sort(key=lambda x: x['due_date'])
    elif sort_by == "Due Date (Descending)":
        filtered_orders.sort(key=lambda x: x['due_date'], reverse=True)
    elif sort_by == "Priority":
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        filtered_orders.sort(key=lambda x: priority_order.get(x.get('priority', 'Medium'), 2))
    elif sort_by == "Date Created":
        filtered_orders.sort(key=lambda x: x.get('created_date', x['due_date']))
    
    # Display orders
    st.subheader(f"Orders ({len(filtered_orders)} found)")
    
    if not filtered_orders:
        st.info("No orders found matching your filters.")
    else:
        for order in filtered_orders:
            # Calculate days until due
            days_until = (order['due_date'] - datetime.now()).days
            if days_until < 0:
                status_text = f"⚠️ OVERDUE by {abs(days_until)} days"
                status_color = "red"
            elif days_until == 0:
                status_text = "📅 Due Today"
                status_color = "orange"
            elif days_until <= 2:
                status_text = f"⏰ Due in {days_until} days"
                status_color = "orange"
            else:
                status_text = f"✅ Due in {days_until} days"
                status_color = "green"
            
            # Status badge with color
            status_badge = {
                'Pending': '🟡',
                'In Progress': '🔵', 
                'Completed': '🟢',
                'Cancelled': '🔴'
            }.get(order['status'], '⚪')
            
            # Priority badge
            priority_badge = {
                'High': '🔴',
                'Medium': '🟡',
                'Low': '🟢'
            }.get(order.get('priority', 'Medium'), '⚪')
            
            with st.expander(f"{priority_badge} {status_badge} Order {order['order_id']} - {order['customer_name']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Customer:** {order['customer_name']}")
                    st.write(f"**Due Date:** {order['due_date'].strftime('%A, %d %b %Y')}")
                    st.markdown(f"<span style='color: {status_color}'><strong>{status_text}</strong></span>", 
                              unsafe_allow_html=True)
                
                with col2:
                    st.write("**Items:**")
                    for item in order['items']:
                        st.write(f"• {item}")
                    
                    if order.get('created_date'):
                        st.write(f"**Created:** {order['created_date'].strftime('%d %b %Y')}")
                
                with col3:
                    st.write(f"**Priority:** {order.get('priority', 'Medium')}")
                    st.write(f"**Status:** {order['status']}")
                    
                    # Status update
                    new_status = st.selectbox(
                        "Update Status", 
                        ["Pending", "In Progress", "Completed", "Cancelled"],
                        index=["Pending", "In Progress", "Completed", "Cancelled"].index(order['status']),
                        key=f"status_{order['order_id']}"
                    )
                    
                    if new_status != order['status']:
                        if st.button("Update Status", key=f"update_status_{order['order_id']}"):
                            update_order_status(order['order_id'], new_status)
                            st.rerun()
                    
                    # Priority update
                    new_priority = st.selectbox(
                        "Update Priority",
                        ["High", "Medium", "Low"],
                        index=["High", "Medium", "Low"].index(order.get('priority', 'Medium')),
                        key=f"priority_{order['order_id']}"
                    )
                    
                    if new_priority != order.get('priority', 'Medium'):
                        if st.button("Update Priority", key=f"update_priority_{order['order_id']}"):
                            update_order_priority(order['order_id'], new_priority)
                            st.rerun()
                    
                    # Delete order
                    if st.button("🗑️ Delete Order", key=f"delete_{order['order_id']}"):
                        remove_order(order['order_id'])
                        st.rerun()
        
        # Order statistics
        st.subheader("Order Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_orders = len(st.session_state.orders)
            st.metric("Total Orders", total_orders)
        
        with col2:
            pending_orders = len([o for o in st.session_state.orders if o['status'] == 'Pending'])
            st.metric("Pending Orders", pending_orders)
        
        with col3:
            overdue_orders = len([o for o in st.session_state.orders if o['due_date'] < datetime.now() and o['status'] in ['Pending', 'In Progress']])
            st.metric("Overdue Orders", overdue_orders)
        
        with col4:
            high_priority = len([o for o in st.session_state.orders if o.get('priority') == 'High' and o['status'] in ['Pending', 'In Progress']])
            st.metric("High Priority", high_priority)

# New Order Page
elif page == "New Order":
    st.header("🛒 New Customer Order")
    
    with st.form("new_order"):
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name", placeholder="e.g., Highland Hotel")
            due_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))
        with col2:
            # Generate order ID automatically
            existing_ids = [int(o['order_id'][3:]) for o in st.session_state.orders if o['order_id'].startswith('ORD') and o['order_id'][3:].isdigit()]
            next_id = max(existing_ids) + 1 if existing_ids else 1
            order_id = st.text_input("Order ID", value=f"ORD{next_id:03d}", disabled=True)
            
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        st.subheader("Order Items")
        items = st.text_area("Items (one per line)", 
                           placeholder="5kg Beef Mince\n3 Whole Chickens\n2kg Pork Sausages\n...",
                           height=150)
        
        notes = st.text_area("Additional Notes", placeholder="Any special instructions or requirements...")
        
        if st.form_submit_button("Create Order"):
            if customer_name and items:
                item_list = [item.strip() for item in items.split('\n') if item.strip()]
                
                new_order = {
                    'order_id': order_id,
                    'customer_name': customer_name,
                    'items': item_list,
                    'due_date': datetime.combine(due_date, datetime.min.time()),
                    'status': 'Pending',
                    'priority': priority,
                    'created_date': datetime.now(),
                    'notes': notes if notes else None
                }
                add_order(new_order)
                st.success(f"✅ Order {order_id} created for {customer_name}!")
                
                # Show summary
                st.info(f"""
                **Order Summary:**
                - **Order ID:** {order_id}
                - **Customer:** {customer_name}
                - **Due Date:** {due_date.strftime('%A, %d %b %Y')}
                - **Priority:** {priority}
                - **Items:** {len(item_list)}
                - **Status:** Pending
                """)

# Shop Jobs Page
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
                    save_data()
                    st.success(f"Added {new_job} to {modify_day} {time_period}")
            
            else:
                existing_jobs = st.session_state.shop_jobs[modify_day].get(time_period, [])
                if existing_jobs:
                    job_to_remove = st.selectbox("Select Job to Remove", existing_jobs)
                    if st.button("Remove Job"):
                        st.session_state.shop_jobs[modify_day][time_period].remove(job_to_remove)
                        save_data()
                        st.success(f"Removed {job_to_remove} from {modify_day} {time_period}")
    
    with tab3:
        st.subheader("Job Descriptions")
        for job, description in st.session_state.job_descriptions.items():
            with st.expander(job.replace('_', ' ').title()):
                st.write(description)

# Enhanced LLM Chat Bot Section
st.sidebar.markdown("---")
st.sidebar.header("💬 David's Larder Assistant")

user_input = st.sidebar.text_input("Ask about workers, timetables, orders, or shop jobs:")

if user_input:
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['worker', 'staff', 'employee']):
        worker_names = [worker['name'] for worker in st.session_state.workers]
        st.sidebar.write(f"**Assistant:** We have {len(worker_names)} workers: {', '.join(worker_names)}")
    
    elif any(word in user_input_lower for word in ['timetable', 'roster', 'schedule']):
        st.sidebar.write("**Assistant:** You can view and manage the detailed timetable with specific time slots in the 'Timetable & Rostering' section.")
    
    elif any(word in user_input_lower for word in ['order', 'delivery']):
        pending_orders = [o for o in st.session_state.orders if o['status'] in ['Pending', 'In Progress']]
        if pending_orders:
            # Find most urgent order
            urgent_orders = [o for o in pending_orders if o['due_date'] <= datetime.now() + timedelta(days=2)]
            if urgent_orders:
                next_order = urgent_orders[0]
                st.sidebar.write(f"**Assistant:** ⚠️ {len(urgent_orders)} urgent orders! Next: {next_order['order_id']} for {next_order['customer_name']} due {next_order['due_date'].strftime('%A')}.")
            else:
                next_order = pending_orders[0]
                st.sidebar.write(f"**Assistant:** We have {len(pending_orders)} active orders. Next: {next_order['order_id']} for {next_order['customer_name']} due {next_order['due_date'].strftime('%A')}.")
        else:
            st.sidebar.write("**Assistant:** No active orders at the moment.")
    
    elif any(word in user_input_lower for word in ['job', 'task', 'work', 'duty']):
        if 'today' in user_input_lower:
            today = datetime.now().strftime('%A')
            jobs_today = st.session_state.shop_jobs.get(today, {})
            response = f"**Assistant:** Today's ({today}) jobs:\n"
            for period, jobs in jobs_today.items():
                response += f"\n{period.title()}: {', '.join([j.replace('_', ' ').title() for j in jobs])}"
            st.sidebar.write(response)
        else:
            st.sidebar.write("**Assistant:** I can tell you about daily shop jobs. Ask about specific days or 'today's jobs'. You can also modify jobs in the 'Shop Jobs' section.")
    
    else:
        st.sidebar.write("**Assistant:** I can help you with worker management, timetables, orders, and daily shop jobs. Try asking about today's tasks or urgent orders.")

# Quick stats in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Stats")
st.sidebar.write(f"**Workers:** {len(st.session_state.workers)}")
st.sidebar.write(f"**Active Orders:** {len([o for o in st.session_state.orders if o['status'] in ['Pending', 'In Progress']])}")
st.sidebar.write(f"**Overdue:** {len([o for o in st.session_state.orders if o['due_date'] < datetime.now() and o['status'] in ['Pending', 'In Progress']])}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🥩 **David's Larder** - Scottish Butcher Shop")
