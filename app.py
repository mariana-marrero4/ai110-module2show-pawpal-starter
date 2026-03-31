import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

# Initialize session state for Owner and Pet
if "owner" not in st.session_state:
    owner_name = "Jordan"
    st.session_state.owner = Owner(name=owner_name, available_time=480)
else:
    owner_name = st.session_state.owner.name

# initialize pets list from owner
if "current_pet" not in st.session_state and st.session_state.owner.pets:
    st.session_state.current_pet = st.session_state.owner.pets[0]
elif "current_pet" not in st.session_state:
    # Create a default pet if owner has no pets
    default_pet = Pet(name="Mochi", pet_type="dog", age=3)
    st.session_state.owner.add_pet(default_pet)
    st.session_state.current_pet = default_pet

# Display owner name (read from session state)
st.write(f"**Owner**: {owner_name}")

st.markdown("### Manage Your Pets")

# Show all pets owned
if st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox(
        "Select a pet to manage",
        pet_names,
        index=pet_names.index(st.session_state.current_pet.name) if st.session_state.current_pet.name in pet_names else 0
    )
    # Update current pet
    for pet in st.session_state.owner.pets:
        if pet.name == selected_pet_name:
            st.session_state.current_pet = pet
            break

# Add new pet form
st.markdown("#### Add a New Pet")
col1, col2, col3 = st.columns(3)

with col1:
    new_pet_name = st.text_input("Pet name", value="")
with col2:
    new_pet_type = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    new_pet_age = st.number_input("Age (years)", min_value=0, max_value=50, value=1, step=1)

if st.button("Add Pet"):
    if not new_pet_name.strip():
        st.error("Pet name cannot be empty!")
    else:
        try:
            # CREATE: Instance of Pet with UI input
            new_pet = Pet(name=new_pet_name, pet_type=new_pet_type, age=int(new_pet_age))
            # WIRE: Call Owner.add_pet() - business logic method
            st.session_state.owner.add_pet(new_pet)
            # UPDATE: Switch to the newly added pet
            st.session_state.current_pet = new_pet
            st.success(f"✅ Pet '{new_pet_name}' added successfully!")
            st.rerun()  # Refresh UI to show new pet in dropdown
        except ValueError as e:
            st.error(f"Cannot add pet: {e}")

st.markdown("### Owner Availability")
new_time = st.number_input(
    "Available time (minutes)", 
    min_value=1, 
    max_value=1440, 
    value=st.session_state.owner.available_time
)
if new_time != st.session_state.owner.available_time:
    st.session_state.owner.set_availability(new_time)

st.markdown(f"### Tasks for {st.session_state.current_pet.name}")
st.caption("Add tasks to your pet's care plan. These persist in the session.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    # Convert priority to numeric (1-3, where 1 is highest priority)
    priority_map = {"high": 1, "medium": 2, "low": 3}
    new_task = Task(
        task_name=task_title,
        duration=int(duration),
        priority=priority_map[priority]
    )
    try:
        st.session_state.current_pet.add_task(new_task)
        st.session_state.tasks.append(
            {"title": task_title, "duration_minutes": int(duration), "priority": priority, "task_id": new_task.task_id}
        )
        st.success(f"Task '{task_title}' added for {st.session_state.current_pet.name}!")
    except ValueError as e:
        st.error(f"Error adding task: {e}")

if st.session_state.current_pet.tasks:
    st.write(f"**{st.session_state.current_pet.name}'s tasks:**")
    task_data = [
        {"Task": t.task_name, "Duration (min)": t.duration, "Priority": ["High", "Medium", "Low"][t.priority-1]}
        for t in st.session_state.current_pet.tasks
    ]
    st.table(task_data)
    st.info(f"Total duration: {st.session_state.current_pet.get_total_duration()} minutes")
else:
    st.info(f"No tasks yet for {st.session_state.current_pet.name}. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

# Show current session state information
with st.expander("📊 Session State Information", expanded=False):
    st.markdown("**Session state** persists data while you navigate the app. Think of it as a persistent dictionary:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Owner:** {st.session_state.owner.name}")
        st.markdown(f"**Available time:** {st.session_state.owner.available_time} min")
    with col2:
        st.markdown(f"**Current Pet:** {st.session_state.current_pet.name} ({st.session_state.current_pet.pet_type})")
        st.markdown(f"**Pet tasks:** {len(st.session_state.current_pet.tasks)}")
    st.markdown(f"**Total pets owned:** {len(st.session_state.owner.pets)}")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.

**Note:** Your Owner and Pet data are now safely stored in `st.session_state` and will persist!
"""
    )
