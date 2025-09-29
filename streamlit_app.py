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

# Data persistence functions
def save_data():
    """Save all session data to JSON file"""
    try:
        # Convert datetime objects to strings for JSON serialization
        orders_serializable = []
        for order in st.session_state.orders:
            order_copy = order.copy()
            if isinstance(order_copy['due_date'], datetime):
                order_copy['due_date'] = order_copy['due_date'].isoformat()
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
            json.dump(data, f, indent=2)
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

# Helper function to create time slots (7:30 AM to 6:00 PM)
def create_time_slots():
    times = []
    for hour in range(7, 19):  # 7 AM to 6 PM
        for minute in [0, 30]:
            # Skip times before 7:30 AM
            if hour == 7 and minute == 0:
                continue
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
    st.subheader("📊 Visual Timetable")
    
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

def create_overlap_view(week_key, days, time_slots):
    """Create a view showing overlapping shifts"""
    st.subheader("👥 Staff Overlap View")
    
    for day in days:
        with st.expander(f"{day} - Staff Overlap"):
            # Find time slots with multiple workers
            overlap_slots = []
            for time_slot in time_slots:
                workers = st.session_state.timetable[week_key][day].get(time_slot, [])
                if len(workers) > 1:
                    overlap_slots.append((time_slot, workers))
            
            if overlap_slots:
                st.write(f"**Multiple staff working at same time:**")
                for time_slot, workers in overlap_slots:
                    worker_names = []
                    for worker_id in workers:
                        worker = next((w for w in st.session_state.workers if w['id'] == worker_id), None)
                        if worker:
                            color = st.session_state.worker_colors.get(worker_id, '#CCCCCC')
                            worker_names.append(f"<span style='background-color: {color}; padding: 2px 6px; border-radius: 3px; color: black;'>{worker['name']}</span>")
                    
                    st.markdown(f"**{time_slot}:** {' '.join(worker_names)}", unsafe_allow_html=True)
            else:
                st.info("No overlapping shifts")

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
    
    # Create overlap view
    create_overlap_view(week_key, days, time_slots)
    
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

# Worker Management Page (rest of the code remains the same)
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

# ... (Rest of the code for Order Management, New Order, Shop Jobs remains the same)
