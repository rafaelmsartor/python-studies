from functools import reduce
import json
import pickle

from utility.hash_util    import hash_block, hash_string_256
from utility.verification import Verification

from block       import Block
from transaction import Transaction
from wallet      import Wallet

# reward given to miners
MINING_REWARD = 10

class Blockchain:

    def __init__(self, public_key, node_id):
        # Starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node = public_key
        self.__peer_nodes = set()
        self.node_id = node_id

        self.load_data()


    @property
    def chain(self):
        return self.__chain[:]


    @chain.setter
    def chain(self, val):
        self.__chain = val


    def get_open_transactions(self):
        return self.__open_transactions[:]


    def load_data(self):
        """Initialize blockchain + open transactions data from file."""
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                file_content = f.readlines()
                
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    # conversion needed due to transactions use of OrderedDict
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]

                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])

                    updated_blockchain.append(updated_block)
                
                self.chain = updated_blockchain

                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for transaction in open_transactions:
                    # conversion needed due to transactions use of OrderedDict
                    updated_transaction = Transaction(
                        transaction['sender'], transaction['recipient'], transaction['signature'], transaction['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions

                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
                # file_contents = pickle.loads(f.read())

                # global blockchain
                # global open_transactions

                # blockchain = file_contents['chain']
                # open_transactions = file_contents['ot']
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup')


    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                # data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(data))
        except IOError:
            print('Error saving data')


    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        """Calculate and return the balance for a participant.
        """
        if self.hosting_node == None:
            return None

        participant = self.hosting_node
        # Fetch a list of all sent coin amounts for the given person( empty lists are returned if the person was NOT the sender )
        # This fetches sent amounts of transactions that were already included in blocks of the blockchain
        tx_sender = [[tx.amount for tx in block.transactions
                    if tx.sender == participant] for block in self.__chain]
        # This fetches the sent amounts of open transactions, avoiding double spending
        open_tx_sender = [tx.amount
                        for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                            if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
        tx_recipient = [[tx.amount for tx in block.transactions
                        if tx.recipient == participant] for block in self.__chain]

        amount_received = reduce(lambda rx_sum, rx_amt: rx_sum + sum(rx_amt)
                                if len(rx_amt) > 0 else rx_sum + 0, tx_recipient, 0)
        # return the total balance
        return amount_received - amount_sent


    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transaction(self, sender, recipient, signature, amount=1.0):
        """ Append a new value aswell as the last blockchain value to the blockchain

        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """
        if self.hosting_node == None:
            return False

        transaction = Transaction(sender, recipient, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False


    def mine_block(self):
        """ Mine the current open transactions, and add a reward transaction with coins to the miner """
        if self.hosting_node == None:
            return None
            
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        # open range selector, copies the entire list
        copied_transactions = self.__open_transactions[:]

        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return False

        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        return block


    def add_peer_node(self, node):
        """Adds a new node to the peer node set.

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()


    def remove_peer_node(self, node):
        """Removes a node from de peer node set.

        Arguments:
            :node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    
    def get_peer_nodes(self):
        """Return a list of all connected peer nodes."""
        return list(self.__peer_nodes)
