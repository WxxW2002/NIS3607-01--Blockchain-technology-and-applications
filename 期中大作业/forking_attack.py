import random
from tqdm import tqdm
from typing import List
import copy
import numpy as np
from 期中大作业.pow_simulate import Node as HonestNode, Block, set_seed, choose_main_chain
SEED = 123
NUM_SIMULATIONS = 1000
NUM_NODES = 200
BLOCK_GEN_PROB = 0.00001
MAX_QUERIES = 100

class MaliciousNode(HonestNode):
    def __init__(self, id_: int, malicious_node_count: int):
        super().__init__(id_)
        self.count = malicious_node_count
        self.chain = [Block(-1, None)]
    
    def proof_of_work(self, block_gen_prob, max_queries):
        queries = 0
        while queries < max_queries * self.count:
            if random.random() < block_gen_prob:
                self.chain.append(Block(self.id, self.chain[-1]))
                break
            queries += 1

if __name__ == '__main__':
    set_seed(SEED)
    max_length = 10
    for malice_rate in np.linspace(0.1, 0.4, 4):
        probabilities = []
        for length in range(1, max_length+1):
            honest_count = int(NUM_NODES * (1 - malice_rate))
            malicious_count = NUM_NODES - honest_count
            success_count = 0
            progress_bar = tqdm(range(NUM_SIMULATIONS))
            for _ in progress_bar:
                honest_nodes = [HonestNode(i) for i in range(honest_count)]
                malicious_node = MaliciousNode(honest_count, malicious_count)
                flag = False
                while not flag:
                    for node in honest_nodes:
                        node.proof_of_work(BLOCK_GEN_PROB, MAX_QUERIES)
                    malicious_node.proof_of_work(BLOCK_GEN_PROB, MAX_QUERIES)
                    honest_length = choose_main_chain(honest_nodes)
                    malicious_length = len(malicious_node.chain)
                    if malicious_length >= (length + 1) or honest_length >= (length + 1):
                        flag = True
                        if malicious_length > honest_length:
                            success_count += 1
                progress_bar.set_description(f'Length: {length}, Success Count: {success_count}')
            probabilities.append(success_count / NUM_SIMULATIONS)
        print(f'Malice Rate: {malice_rate}, Probabilities: {probabilities}, E(Length): {sum([i * probabilities[i - 1] for i in range(1, max_length+1)])}')