#Testing the V1 code to make sure jobs_graph is generated correctly

import unittest
import userb_feature_v1

class TestJobsGraph(unittest.TestCase):
    @classmethod 
    def setUpClass(cls):
        cls.jobs_graph = userb_feature_v1.build_jobs_graph("data/Skills.xlsx")
    
    def test_num_nodes(self):
        self.assertEqual(self.jobs_graph.number_of_nodes(), 879)

    def test_num_edges(self):
        self.assertEqual(self.jobs_graph.number_of_edges(), 385337)

    def test_num_unique_skills(self):
        all_skills = set()

        for node, data in self.jobs_graph.nodes(data=True):
            skills_list= data.get("skills", [])
            all_skills.update(skills_list)
        
        unique_skills=len(all_skills)
        self.assertEqual(unique_skills, 35)
