from csp import Constraint, CSP
from typing import Dict, List, Optional

class AirTrafficConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2
    
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment, then it is not
        # yet possible for their colors to be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # check the color assigned to place1 is not the same as the # color assigned to place2
        return assignment[self.place1] != assignment[self.place2]

if __name__ == "__main__":
    variables: List[str] = ["FORTALEZA", "SAO PAULO", "BELO HORIZONTE", "RIO DE JANEIRO", "SALVADOR"] 
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ["red", "green"]
    
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(AirTrafficConstraint("SAO PAULO", "FORTALEZA"))
    csp.add_constraint(AirTrafficConstraint("FORTALEZA", "SAO PAULO"))
    csp.add_constraint(AirTrafficConstraint("SAO PAULO", "BELO HORIZONTE"))
    csp.add_constraint(AirTrafficConstraint("BELO HORIZONTE", "SAO PAULO"))
    csp.add_constraint(AirTrafficConstraint("SAO PAULO", "RIO DE JANEIRO"))
    csp.add_constraint(AirTrafficConstraint("RIO DE JANEIRO", "SAO PAULO"))
    csp.add_constraint(AirTrafficConstraint("RIO DE JANEIRO", "SALVADOR"))
    csp.add_constraint(AirTrafficConstraint("SALVADOR", "RIO DE JANEIRO"))

solution: Optional[Dict[str, str]] = csp.backtracking_search()
if solution is None:
    print("No solution found!") 
else:
    print(solution)