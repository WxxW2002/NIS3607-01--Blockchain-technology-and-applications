import random
from tqdm import tqdm
from typing import List
import copy
import numpy as np

SEED = 123
ROUNDS = 2000
NODE_NUM = 500
MAX_ORACLE_QUERY = 100


class Node:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.blockchain = [Block(-1, None)]

    def mine_block(self, block_gen_rate, max_oracle_query):
        ctr = 0
        while ctr < max_oracle_query:
            if random.random() < block_gen_rate:
                self.blockchain.append(Block(self.node_id, self.blockchain[-1]))
                break
            ctr += 1


class Block:
    def __init__(self, creator_id: int, prev_block):
        self.creator_id = creator_id
        self.prev_block = prev_block


def select_chain(node_list: List[Node]):
    id_list = []
    max_length = 0
    for node in node_list:
        if len(node.blockchain) > max_length:
            max_length = len(node.blockchain)
    for node in node_list:
        if len(node.blockchain) == max_length:
            id_list.append(node.node_id)

    for node in node_list:
        selected_id = random.choice(id_list)
        node.blockchain = copy.deepcopy(node_list[selected_id].blockchain[:max_length])
    return max_length


def set_random_seed(seed):
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
    set_random_seed(SEED)

    honest_node_num = NODE_NUM
    nodes = [Node(node_id) for node_id in range(honest_node_num)]

    for block_gen_rate in [1e-7, 1e-6, 1e-5, 1e-4]:
        print(f"Block Generation Rate: {block_gen_rate}")
        chain_length_per_round = []

        progress_bar = tqdm(range(ROUNDS))
        for round_num in progress_bar:
            for node in nodes:
                node.mine_block(block_gen_rate, MAX_ORACLE_QUERY)
            length = select_chain(nodes)
            chain_length_per_round.append(length)
            progress_bar.set_description(f"Max Valid Chain Length: {length}, Chain Growth Rate: {(length - 1) / (round_num + 1)}")

        chain_length_per_round = np.array(chain_length_per_round)
        np.save(f"./results/chain_gen_{block_gen_rate}.npy", chain_length_per_round)
        print(f"Block Generation Rate: {block_gen_rate}, Chain Growth Rate: {(length - 1) / ROUNDS}")