

def count_resources_points(resources: list) -> int: 
    total_points = 0                                
    for resource in resources:                      
        if resource['name'] == 'Água':              
            points = resource['quantity'] * 4    
            total_points += points
        if resource['name'] == 'Alimentação':
            points = resource['quantity'] * 3    
            total_points += points
        if resource['name'] == 'Medicação':
            points = resource['quantity'] * 2   
            total_points += points
        if resource['name'] == 'Munição':
            points = resource['quantity'] * 1    
            total_points += points

    return total_points