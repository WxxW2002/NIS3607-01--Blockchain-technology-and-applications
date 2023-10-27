import random
from tqdm import tqdm
from typing import List
import copy
import numpy as np


SEED = 666
ROUND = 30000
NODE_NUM = 1000
BLOCK_GEN_RATE = .0000001
MAX_ORACLE_QUERY = 100


class Node(object):
    """
    Node in the blockchain network
    * id_: Node's id
    * type_: True for honest node, False for malicious node
    """
    def __init__(self, id_: int):
        self.id = id_
        # Genesis block
        self.blockchain = [Easy_Block(-1, None)]
    

    def PoW(self, block_gen_rate, max_oracle_query):
        """
        Use Monte Carlo method to simulate the PoW process, not sovling the cryptographic puzzle
        """
        ctr = 0
        while ctr < max_oracle_query:
            if random.random() < block_gen_rate:
                self.blockchain.append(Easy_Block(self.id, self.blockchain[-1]))
                break
            ctr += 1


class Easy_Block(object):
    """
    Just for simulation, not the real block structure
    """
    def __init__(self, creator_id: int, prev_block):
        self.creator_id = creator_id
        self.prev_block = prev_block


def select_chain(node_list: List[Node]):
    """
    Return the longest valid chain
    Conflict resolution with the same chain length: randomly choose one
    """
    id_list = []
    max_len = 0
    for node in node_list:
        if len(node.blockchain) > max_len:
            max_len = len(node.blockchain)
    for node in node_list:
        if len(node.blockchain) == max_len:
            id_list.append(node.id)

    for node in node_list:
        id_ = random.choice(id_list)
        node.blockchain = copy.deepcopy(node_list[id_].blockchain[:max_len])
    return max_len


def fix_seed(seed):
    import os
    import numpy as np
    import torch
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


if __name__ == "__main__":
    fix_seed(SEED)
    
    honest_node_num = NODE_NUM
    node_list = [Node(i) for i in range(honest_node_num)]

    for block_gen_rate in [1e-8]:
        print(f"block gen rate: {block_gen_rate}")
        chain_len_per_round = []

        progress_bar = tqdm(range(ROUND))
        for r in progress_bar:
            for node in node_list:
                node.PoW(block_gen_rate, MAX_ORACLE_QUERY)
            len_ = select_chain(node_list)
            chain_len_per_round.append(len_)
            progress_bar.set_description(f"max valid chain length: {len_}, chain growth rate: {(len_-1)/(r+1)}")

        chain_len_per_round = np.array(chain_len_per_round)
        np.save(f"./data/chain_gen_{block_gen_rate}.npy", chain_len_per_round)
        print(f"block gen rate :{block_gen_rate}, chain growth rate: {(len_-1)/ROUND}")
