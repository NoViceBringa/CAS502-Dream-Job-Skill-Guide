# This was hard...

from usera_feature_v2 import usera_path
from userb_feature_v1 import build_jobs_graph, userb_path


def prompt_user_for_dream_job(prompt):
    """
    Prompts the user with a yes/no question and returns True for 'y' and False for 'n'.
    Continues to prompt until a valid input is received. Also displays an error message for invalid inputs.
    """
    while True:
        ans = input(f"{prompt} [y/n]: ")
        # This will convert the input to lowercase to control for case sensitivity
        if ans.lower() == 'y':
            return True
        elif ans.lower() == 'n':
            return False
        print("Invalid input. Please enter the character 'y' for yes or the character 'n' for no.")


def main():
    """ 
    Controls the graph building in userb_feature_v2 and 
    routes the user to the appropriate feature based on their input. 
    """
    # Builds the graph from the userb_feature_v2 function.
    jobs_graph = build_jobs_graph("data/Skills.xlsx")

    knows = prompt_user_for_dream_job("Do you know your dream job?")

    # This simple routing took soo long to figure out, but behold its beauty!
    if knows:
        usera_path(jobs_graph)
    else:
        userb_path(jobs_graph)


if __name__ == "__main__":
    main()