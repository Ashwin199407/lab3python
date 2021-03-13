from SampleWallet import generateSampleWallet
from Message import Message
from TxInputList import TxInputList
from TxInput import TxInput, createTxInput
from TxOutputList import TxOutputList
from TxOutput import TxOutput
from Transaction import Transaction


class AccountBalance:
    """ AccountBalance defines an accountBalance 
        in the ledger model of bitcoins"""

    def __init__(self,accountBalanceBase = None):
        """Constructor, construct AccountBalance from accountBalanceBase
           which is a dictionary from publicKeys to the amount they have
           without arguments returns the empty AccountBalance"""
        self.publicKeyList = []
        self.accountBalanceBase = dict()
        if accountBalanceBase is not None:
            for keyName in accountBalanceBase.keys():
                self.addAccount(keyName,accountBalanceBase[keyName])

    def __repr__(self):
        """default toString method"""
        result = ""
        for publicKey in self.getPublicKeys():
            result += "(PublicKey = ",publicKey,\
                      " Amount = ",self.getBalance(publicKey)
        return result

    def __eq__ (self,other):
        return self.getAccountBalance() == other.getAccountBalance()

    def __copy__(self):
        return AccountBalance(self.getAccoutBalance())


    def addAccount(self,publicKey,balance):
        """Adds account given by publicKey with balance to the Balance
        """
        self.accountBalanceBase[publicKey] = balance
        if  publicKey not in self.publicKeyList:
            self.publicKeyList.append(publicKey)

    def hasPublicKey(self,publicKey):
        """Check whether there is an account with publicKey"""
        return (publicKey in self.getPublicKeys())

    def getPublicKeys(self):
        """get the list of Public Keys having accounts in AccountBalance
        """
        return self.getAccountBalanceBase().keys()


    def getAccountBalanceBase(self):
        """Return the underlying dictionary mapping
           publicKeys to balance"""
        return self.accountBalanceBase

    def hasAccount(self,publicKey):
        """Check whether there is an account for publicKey"""
        return publicKey in self.accountBalanceBase

    def getBalance(self,publicKey):
        """Get the balance in AccountBalance for publicKey
           if there is no account, return 0
        """
        if self.hasAccount(publicKey):
            return self.getAccountBalanceBase()[publicKey]
        else:
            return 0

    


    def setBalance(self,publicKey,balance):
        """Set the balance for publicKey to balance
           If account doesn't exist it is created with balance 
        """
        self.accountBalanceBase[publicKey] = balance
        if  publicKey not in self.publicKeyList:
            self.publicKeyList.append(publicKey)
    

    def addToBalance(self,publicKey, amount):
        """ Adds amount to balance for publicKey
           If account doesn't exist it is created with amount
        """ 
        self.setBalance(publicKey,self.getBalance(publicKey) + amount)

            
    def subtractFromBalance(self,publicKey, amount):
        """ Subtracts amount from balance for publicKey
            If account doesn't exist it is created with -amount
        """ 
        self.setBalance(publicKey,self.getBalance(publicKey) - amount)

    def checkBalance(self,publicKey,amount):
        """Checks whether the balance for publicKey is >= the amount.
           If account doesn't exist a balance of 0 is assumed 
        """
        return (self.getBalance(publicKey) >= amount)

    def checkDictPublicKeyAmountCanBeDeducted(self,dictPublicKeyAmount):
        """Check whether a map (a dictionary) from public keys to
           amounts can be deducted from AccountBalance
           This is an auxiliary function to define 
           checkTxInputListCanBeDeducted
        """
        for publicKey in dictPublicKeyAmount.keys():
            if not self.checkBalance(publicKey,dictPublicKeyAmount[publicKey]):
                return False

        return True

    def checkTxInputListCanBeDeducted(self,txInputList):
        """ Check that a list of publicKey amounts can be deducted from the 
             current accountBalance
            done by first converting the list of publicKey amounts into an 
              accountBalance
            and then checking that the resulting accountBalance can be deducted.
        """
        
        return self.checkDictPublicKeyAmountCanBeDeducted(txInputList.toDictPublicKeyAmount())

    def subtractTxInputList(self,txInputList):
        """ Subtract a list of TxInput from the accountBalance
            requires that the list to be deducted is deductable."""
        for txInput in txInputList.toList():
            self.subtractFromBalance(txInput.getSender(),txInput.getAmount())

    def addTxOutputList(self,txOutputList):
        """ Add a list of TxOutput to the accountBalance """
        for txOutput in txOutputList.toList():
            self.addToBalance(txOutput.getRecipient(),txOutput.getAmount())

    #################################################################
    #  Task 4 Check a transaction is valid.
    #
    #  this means that 
    #    the sum of outputs is less than or equal the sum of inputs
    #    all signatures are valid
    #    and the inputs can be deducted from the accountBalance.
    #
    #    This method has been set to true so that the code compiles - that should
    #    be changed
    ################################################################        

    def checkTransactionValid(self,transaction):
        # this is not the correct value, only used here so that the code
        # compiles
        return True        

    def processTransaction(self,transaction):
        """ Process a transaction
            by first deducting all the inputs
            and then adding all the outputs.
        """
        self.subtractTxInputList(transaction.toTxInputList())
        self.addTxOutputList(transaction.toTxOutputList())

    def str(self,pubKeyMap):
        """String which shows the current state of the accountBalance
           using pubKeyMap for looking up keyNames for the publicKeys
        """
        result = ""
        for publicKey in self.getPublicKeys():
            balance = self.getBalance(publicKey)
            result += ("The balance for " +
                       pubKeyMap.getKeyName(publicKey) +
                       " is " +
                       str(self.getBalance(publicKey)) +
                       "\n")
        return result

    def print(self,pubKeyMap):
        """print the current state of the accountBalance
        """
        print(self.str(pubKeyMap))
    

def test():
    """Test cases """
    exampleWallet = generateSampleWallet(["Alice"])
    pubKeyMap = exampleWallet.toPublicKeyMap()
    exampleMessage = Message()
    exampleMessage.addInteger(15)
    exampleSignature = exampleWallet.signMessage(exampleMessage,"Alice")

    ##################################################################
    #  Task 5
    #   add  to the test case the test as described in the lab sheet
    #
    #   You can use the above exampleSignature, when a sample
    #      signature is needed, which cannot be computed from the data.
    #
    ##################################################################

    

if __name__=="__main__":
    test()    
    
    

    
            

            


    
    
                

            


    

    
