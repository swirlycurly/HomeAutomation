import os


def get_project_id():
    with open("./secrets/nest_project_id.txt", "r", encoding="utf-8") as f:
        projectId = f.read()

    if projectId is None or len(projectId) == 0:
        raise Exception("NEST_PROJECT_ID is missing")

    return projectId
