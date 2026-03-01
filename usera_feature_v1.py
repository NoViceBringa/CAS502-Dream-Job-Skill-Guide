import networkx as nx

def usera_path(jobs_graph):
    """ This function allows user A to input their current job title and their dream job title, 
    and then receive the top 5 skills needed to transition from their current job to their 
    dream job. """

    current_title = input("Enter your current job title: ")
    dream_title = input("Enter your dream job title: ")
    
    # This pulls all the job titles from the jobs_graph in start_here.py to check if the user's job titles are in the dataset.
    labels = {data.get("label") for _, data in jobs_graph.nodes(data=True)}

    if current_title not in labels:
        print(f"Current job title '{current_title}' not found! View list of job titles here: https://github.com/NoViceBringa/CAS502-Dream-Job-Skill-Guide/blob/main/data/Skills.xlsx")
        return
    
    if dream_title not in labels:
        print(f"Dream job title '{dream_title}' not found! View list of job titles here: https://github.com/NoViceBringa/CAS502-Dream-Job-Skill-Guide/blob/main/data/Skills.xlsx")
        return
    
    # This finds the nodes for the current and dream job titles.
    current_node = None
    dream_node = None

    for node, data in jobs_graph.nodes(data=True):
        if data.get("label") == current_title:
            current_node = node
        if data.get("label") == dream_title:
            dream_node = node
    
    current_skills = jobs_graph.nodes[current_node]["skills"]
    dream_skills = jobs_graph.nodes[dream_node]["skills"]

    # Once we have the skills for the current and dream job
    # we can compare them to find out which skills the user is missing for their dream job.
    missing_skills = []

    for skill_id, skill_data in dream_skills.items():
        if skill_id not in current_skills:
            missing_skills.append(skill_data)
    
    # Lucky Duck! The user has all the skills for their dream job!
    if not missing_skills:
        print("You have all the skills for your dream job!")
        return
    
    # Turns out that we need to sort the missing skills by importance or it will just print them in 
    # the order they were added to the graph, which is not very helpful for the user.
    missing_skills = sorted(
        missing_skills,
        key=lambda skill: skill["importance"],
        reverse=True
    )
    print("Top 5 skills you need for your dream job:")

    for skill in missing_skills[:5]:
        print(f"{skill['name']} (Importance: {skill['importance']})")