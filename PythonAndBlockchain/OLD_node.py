
from utility.verification import Verification
from blockchain import Blockchain

from wallet import Wallet

from uuid import uuid4

class Node:

    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.blockchain = Blockchain('')

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print('Please choose:')
            print('1: Add a new transaction value')
            print('2: Mine the current block')
            print('3: Ouput the blockchain blocks')
            print('4: Verify transactions validitya')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')

            user_choice = self.get_user_choice()

            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(self.wallet.public_key, recipient, signature, amount):
                    print('Transction succeeded')
                else:
                    print('Transaction failed')
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print ('Mining failed. Got no wallet?')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('Transactions are valid')
                else:
                    print('There is an invalid transaction')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid!!')

            if self.blockchain != None and (not Verification.verify_chain(self.blockchain.chain)):
                print('Invalid blockchain')
                break

        print('Done')

        
    def get_transaction_value(self):
        """ Returns hte input of the user, a new transaction (recipient, amount) """
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        return (tx_recipient, tx_amount)


    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input


    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        for block in self.blockchain.chain:
            print('Outputting block')
            print(block)

node = Node()
node.listen_for_input()