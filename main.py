import random
from src.datastructures import Restaurant, Party, Table
from src.agent import SeatingAgent
from src.utils import visualize_seating
import time

def main():
    NUM_TABLES = 10
    NUM_PARTIES = 11

    # Create a restaurant
    r = Restaurant()

    for i in range(NUM_TABLES):
        r.add_table(Table(i, random.randint(2, 8)))
        
    for i in range(NUM_PARTIES):
        r.enqueue(Party(random.randint(1, 6)))
        time.sleep(0.1)

    # Create and train the agent
    agent = SeatingAgent(r.tables)
    agent.train(r, episodes=1000, queue_time_weight=1.0, size_difference_weight=0)
    agent.seat_customers(r)

    visualize_seating(r)

if __name__ == '__main__':
    main()
