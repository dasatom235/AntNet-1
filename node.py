import itertools
import heapq
import globals


class Node:
    def __init__(self, id):
        # Node label
        self.id = id

        # List of pairs (neighbourNode, weight)
        self.links = []

        # Maximum number of ants in a node
        self.capacity = globals.NODE_CAPACITY

        # Current ants in the node
        self.antsInNode = self.PriorityQueue()

        # Pheromone table for neighbour nodes
        self.pheromoneTable = []

    # Storing Node instance
    def addLink(self, node, weight):
        self.links.append((node, weight))

    def initPheromoneTable(self):
        probability = 1.0 / len(self.links)

        for link in self.links:
            self.pheromoneTable.append(self.TableEntry(link, probability))

    def connectAnt(self, ant):
        # TODO Should check if node is full...but lets keep it simple for now
        self.antsInNode.add(ant)
        return True

    # Contains the probability for a neighbour node to be chosen next
    class TableEntry:
        def __init__(self, link, probability):
            self.link = link
            self.probability = probability

    class PriorityQueue:
        def __init__(self):
            # list of entries arranged in a heap
            self.ants = []

            # mapping of ants to entries
            self.antFinder = {}

            # placeholder for a removed ant
            self.REMOVED = 'REMOVED'

            # unique sequence count
            self.counter = itertools.count()

        # Takes an instance of Ant class
        def add(self, ant):
            # Add a new task or update the priority of an existing task
            if ant in self.antFinder:
                self.remove(ant)

            count = next(self.counter)
            entry = [ant.direction, count, ant]

            self.antFinder[ant] = entry

            heapq.heappush(self.ants, entry)

        def remove(self, ant):
            # Mark an existing ant as REMOVED. Raise KeyError if not found.
            entry = self.antFinder.pop(ant)
            entry[-1] = self.REMOVED

        def pop(self):
            # Remove and return the lowest priority task. Raise KeyError if empty.
            while self.ants:
                priority, count, ant = heapq.heappop(self.ants)

                if ant is not self.REMOVED:
                    del self.antFinder[ant]
                    return ant

            raise KeyError('pop from an empty priority queue')
