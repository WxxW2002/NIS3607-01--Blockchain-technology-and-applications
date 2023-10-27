import random
from tqdm import tqdm
from typing import List
import copy
import numpy as np
from pow import Node as HonestNode, Easy_Block, fix_seed, select_chain


SEED = 666
TEST_NUM = 1000
NODE_NUM = 1000
BLOCK_GEN_RATE = .0000001
MAX_ORACLE_QUERY = 100


class MaliciousNode(HonestNode):
  def __init__(self, id_: int, malicious_node_num: int):
    super().__init__(id_)
    self.num = malicious_node_num
    self.blockchain = [Easy_Block(-1, None)]

  def PoW(self, block_gen_rate, max_oracle_query):
    ctr = 0
    while ctr < max_oracle_query * self.num:
        if random.random() < block_gen_rate:
            self.blockchain.append(Easy_Block(self.id, self.blockchain[-1]))
            break
        ctr += 1


if __name__ == '__main__':
  fix_seed(SEED)
  max_len = 10

  for malicious_rate in np.linspace(0.1, 0.4, 4):
    probs = []
    
    for len_ in range(1, max_len+1):
      honest_node_num = int(NODE_NUM*(1-malicious_rate))
      malicious_node_num = NODE_NUM - honest_node_num

      success_time = 0
      progress_bar = tqdm(range(TEST_NUM))

      for _ in progress_bar:
        honest_node_list = [HonestNode(i) for i in range(honest_node_num)]
        malicious_node = MaliciousNode(honest_node_num, malicious_node_num)

        flag = False
        while not flag:
          for node in honest_node_list:
            node.PoW(BLOCK_GEN_RATE, MAX_ORACLE_QUERY)
          malicious_node.PoW(BLOCK_GEN_RATE, MAX_ORACLE_QUERY)

          cur_honest_len = select_chain(honest_node_list)
          cur_malicious_len = len(malicious_node.blockchain)
          if cur_malicious_len >= (len_+1) or cur_honest_len >= (len_+1): # consider genesis block
            flag = True
            if cur_malicious_len > cur_honest_len:
              success_time += 1
        progress_bar.set_description(f'len: {len_}, success_time: {success_time}')
      probs.append(success_time/TEST_NUM)
    print(f'malicious rate: {malicious_rate}, probs: {probs}, E(len): {sum([i*probs[i-1] for i in range(1, max_len+1)])}')
