from arc.read import parse_dir
import os

def concept_arc_problems():
    problems = []
    for problem_directory in os.listdir("ConceptARC"):
        problems.extend(parse_dir("ConceptARC/"+problem_directory))
    
    return problems

