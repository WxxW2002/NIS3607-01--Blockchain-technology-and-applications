import random
from typing import List
from tqdm import tqdm
from copy import deepcopy

class Block(object):
  def __init__(self, node_type: bool = None, prev_block = None):
    self.node_type = node_type
    self.prev_block = prev_block

class HonestNode(object):
  def __init__(self):
    self.public_chain: List[Block] = []

class SelfishPool(object):
  def __init__(self):
    self.public_chain: List[Block] = []
    self.private_chain: List[Block] = []
    self.private_chain_len = 0

class BlockchainSystem(object):
  def __init__(self, malicious_rate: float):
    self.malicious_rate = malicious_rate
    self.honest_node = HonestNode()
    self.selfish_pool = SelfishPool()

    gensis_block = Block(True, None)
    self.honest_node.public_chain.append(gensis_block)
    self.selfish_pool.public_chain.append(gensis_block)
    self.selfish_pool.private_chain.append(gensis_block)

  def selfish_mining(self, time_unit: int):
    """
    A time unit = 10 minutes
    """
    progress_bar = tqdm(range(time_unit))
    for r in progress_bar:
      if random.random() < self.malicious_rate:
        self.on_pool_find_a_block()
      else:
        self.on_other_find_a_block()
      if r == time_unit - 1:
        self.selfish_pool.public_chain = deepcopy(self.selfish_pool.private_chain)
      self.select_chain()
    
    block_from_pool = 0
    for block in self.honest_node.public_chain:
      if not block.node_type:
        block_from_pool += 1
    return block_from_pool/len(self.honest_node.public_chain)
    

  def on_pool_find_a_block(self):
    delta = len(self.selfish_pool.private_chain) - len(self.selfish_pool.public_chain)
    self.selfish_pool.private_chain.append(Block(False, self.selfish_pool.private_chain[-1]))
    self.selfish_pool.private_chain_len += 1
    if delta == 0 and self.selfish_pool.private_chain_len == 2:
      self.selfish_pool.public_chain = deepcopy(self.selfish_pool.private_chain)
      self.selfish_pool.private_chain_len = 0
    
  def on_other_find_a_block(self):
    self.honest_node.public_chain.append(Block(True, self.honest_node.public_chain[-1]))
    delta = len(self.selfish_pool.private_chain) - len(self.selfish_pool.public_chain)
    if delta == 0:
      self.selfish_pool.private_chain = deepcopy(self.honest_node.public_chain)
      self.selfish_pool.private_chain_len = 0
    elif delta == 1:
      self.selfish_pool.public_chain = deepcopy(self.selfish_pool.private_chain)
    elif delta == 2:
      self.selfish_pool.public_chain = deepcopy(self.selfish_pool.private_chain)
      self.selfish_pool.private_chain_len = 0
    else:
      self.selfish_pool.public_chain = deepcopy(self.selfish_pool.private_chain[:len(self.selfish_pool.public_chain)+1])

  def select_chain(self):
    if len(self.selfish_pool.public_chain) > len(self.honest_node.public_chain):
      self.honest_node.public_chain = deepcopy(self.selfish_pool.public_chain)
    elif len(self.selfish_pool.public_chain) < len(self.honest_node.public_chain):
      self.selfish_pool.public_chain = deepcopy(self.honest_node.public_chain)
    else:
      if random.random() < 0.5:
        self.honest_node.public_chain = deepcopy(self.selfish_pool.public_chain)

if __name__ == '__main__':
  time_unit = 10000
  for malicious_rate in [0.1, 0.2, 0.3, 0.4, 0.5]:
    print(f"malicious rate: {malicious_rate}")
    blockchain_system = BlockchainSystem(malicious_rate)
    print(f"selfish mining revenue: {blockchain_system.selfish_mining(time_unit)}")
