import random

class variable:
    def __init__(self, name, domains, constraints):
        self.name = name
        self.domains = domains
        self.constraints = constraints


class min_conflicts:
    def __init__(self, variables, max_steps=1000):
        self.variables = variables
        self.max_steps = max_steps
        self.assignments = {}

    def conflicts(self, var, value, current):
        count = 0
        for neighbor_name in var.constraints:
            if neighbor_name in current and current[neighbor_name] == value:
                count += 1
        return count

    def min_conflicts(self, max_steps):
        current = {}
        for var in self.variables:
            current[var.name] = random.choice(var.domains)

        for i in range(1, max_steps + 1):
            conflicted_variables = []
            for var in self.variables:
                val = current[var.name]
                if self.conflicts(var, val, current) > 0:
                    conflicted_variables.append(var)
            
            if not conflicted_variables:
                return current
            
            var = random.choice(conflicted_variables)
            
            min_conflict_val = float('inf')
            best_values = []
            for v in var.domains:
                c = self.conflicts(var, v, current)
                if c < min_conflict_val:
                    min_conflict_val = c
                    best_values = [v]
                elif c == min_conflict_val:
                    best_values.append(v)
            
            value = random.choice(best_values)
            
            current[var.name] = value

        return None

    def solve(self):
        result = self.min_conflicts(self.max_steps)
        if result is not None:
            self.assignments = result
            return result
        return None


if __name__ == "__main__":
    adjacency_dict = {
        "Gò Vấp": ["Tân Bình", "Phú Nhuận", "Bình Thạnh"],
        "Bình Thạnh": ["Gò Vấp", "Phú Nhuận", "Quận 1"],
        "Phú Nhuận": ["Gò Vấp", "Bình Thạnh", "Tân Bình", "Quận 3", "Quận 1"],
        "Tân Bình": ["Gò Vấp", "Phú Nhuận", "Quận 3", "Quận 10", "Quận 11"],
        "Quận 1": ["Bình Thạnh", "Phú Nhuận", "Quận 3", "Quận 5", "Quận 4"],
        "Quận 3": ["Phú Nhuận", "Tân Bình", "Quận 1", "Quận 10", "Quận 5"],
        "Quận 10": ["Tân Bình", "Quận 3", "Quận 11", "Quận 5"],
        "Quận 11": ["Tân Bình", "Quận 10", "Quận 6", "Quận 5"],
        "Quận 5": ["Quận 10", "Quận 3", "Quận 1", "Quận 11", "Quận 6", "Quận 4"],
        "Quận 6": ["Quận 11", "Quận 5"],
        "Quận 4": ["Quận 1", "Quận 5"]
    }

    domains = ['Đỏ', 'Xanh lá', 'Vàng', 'Xanh dương']
    variables_list = []
    for name, constraints in adjacency_dict.items():
        variables_list.append(variable(name=name, domains=list(domains), constraints=constraints))

    problem = min_conflicts(variables=variables_list, max_steps=1000)
    solution = problem.solve()
    
    print("=== KẾT QUẢ KIỂM THỬ MIN-CONFLICTS ===")
    if solution:
        for var_name, color in solution.items():
            print(f"Vùng {var_name}: Tô màu {color}")
    else:
        print("Không tìm thấy lời giải hợp lệ.")
