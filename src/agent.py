import numpy as np
from src.datastructures import Restaurant, Table, Party

class SeatingAgent:
    def __init__(self, tables):
        self.tables = tables
        self.q_table = {}

    def choose_action(self, state, epsilon=0.1):
        available_actions = [
            i for i, table in enumerate(self.tables) if table.party is None
        ]
        if not available_actions:
            return -1

        if np.random.rand() < epsilon or state not in self.q_table:
            return np.random.choice(available_actions)
        
        best_action = available_actions[0]
        best_value = self.q_table[state][best_action]

        for action in available_actions:
            if self.q_table[state][action] > best_value:
                best_value = self.q_table[state][action]
                best_action = action

        return best_action

    def update_q_table(self, state, action, reward, next_state, alpha=0.1, gamma=0.9):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.tables))
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.tables))
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state][action] = (
            (1 - alpha) * self.q_table[state][action]
            + alpha * (reward + gamma * self.q_table[next_state][best_next_action])
        )

    def train(self, restaurant: Restaurant, episodes=1000, queue_time_weight=0.1, size_difference_weight=1.0):
        for _ in range(episodes):
            state = (
                tuple((table.seats, table.party is None) for table in restaurant.tables),
                tuple((party.size, party.queue_time) for party in restaurant.queue)
            )

            for i, party in enumerate(restaurant.queue):
                action = self.choose_action(state)
                if action == -1:
                    continue

                table = restaurant.tables[action]
                if party.size <= table.seats and table.party is None:
                    size_difference = table.seats - party.size
                    reward = (size_difference_weight / 5) * (1 - (size_difference / max(table.seats, 1))) - queue_time_weight * party.queue_time
                    restaurant.seat_party(party, table)
                else:
                    reward = -1 - queue_time_weight * party.queue_time

                next_state = (
                    tuple((table.seats, table.party is None) for table in restaurant.tables),
                    tuple((p.size, p.queue_time) for p in restaurant.queue[i+1:])
                )

                self.update_q_table(state, action, reward, next_state)
                state = next_state

    def seat_customers(self, restaurant: Restaurant):
        state = (
            tuple((table.seats, table.party is None) for table in restaurant.tables),
            tuple((party.size, party.queue_time) for party in restaurant.queue)
        )

        for party in restaurant.queue:
            action = self.choose_action(state, epsilon=0.0)
            if action == -1:
                continue

            if party.size <= restaurant.tables[action].seats and restaurant.tables[action].party is None:
                restaurant.seat_party(party, restaurant.tables[action])

            state = (
                tuple((table.seats, table.party is None) for table in restaurant.tables),
                tuple((p.size, p.queue_time) for p in restaurant.queue)
            )
