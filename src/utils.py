from src.datastructures import Restaurant

def visualize_seating(restaurant: Restaurant):
    for table in restaurant.tables:
        if table.party:
            print(f"({table.id}) {table.seats} top seated with Party of {table.party.size} (queuetime: {table.party.queue_time % 10:.2f})")
        else:
            print(f"({table.id}) {table.seats} top is empty")
    
    if len(restaurant.queue) > 0:
        print("\nUnseated parties:")
        for party in restaurant.queue:
            print(f"Party of {party.size} (queuetime: {party.queue_time % 10:.2f}) still waiting")
