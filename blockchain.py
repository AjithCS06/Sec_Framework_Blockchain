import random
import sys
import base64
import json
import os
import pandas as pd
from web3 import Web3
from solcx import compile_standard
# from ipfs import upload as up1
import ipfshttpclient
import solcx
#solcx.install_solc()

compiled_sol = compile_standard({
     "language": "Solidity",
     "sources": {
         "phb.sol": {
             "content": '''
                 pragma solidity >=0.4.0 <0.8.16;
               

                contract PHB {

                    struct Bank
                    {            
                        int user_id;
                        string username;
                        string password;
                        string mobile;
                        string p_address;
                    }

                    Bank []banks;

                    function addBank(int user_id,string memory username,string memory password,string memory mobile,string memory p_address) public
                    {
                        Bank memory e
                            =Bank(user_id,
                                    username,
                                    password,
                                    mobile,
                                    p_address);
                        banks.push(e);
                    }

                    function getBank(int user_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<banks.length;i++)
                        {
                            Bank memory e
                                =banks[i];
                            
                            if(e.user_id==user_id)
                            {
                                return(e.username,
                                    e.password,
                                    e.mobile,
                                    e.p_address
                                   
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found"
                               );
                    }

                    function getBankCount() public view returns(uint256)
                    {
                        return(banks.length);
                    }


                     struct Company
                    {
       
                        int user_id;
                        string username;
                        string password;
                        string mobile;
                        string p_address;
                    }

                    Company []comps;

                    function addCompany(int user_id,string memory username,string memory password,string memory mobile,string memory p_address) public
                    {
                        Company memory e
                            =Company(user_id,
                                    username,
                                    password,
                                    mobile,
                                    p_address);
                        comps.push(e);
                    }


                    function getCompany(int user_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<comps.length;i++)
                        {
                            Company memory e
                                =comps[i];
                                 
                            
                            if(e.user_id==user_id)
                            {
                                return(e.username,
                                    e.password,
                                    e.mobile,
                                    e.p_address
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found");
                    }

                    function getCompanyCount() public view returns(uint256)
                    {
                        return(comps.length);
                    }


                    struct Loan
                    {            
                        int l_id;
                        string username;
                        string loan_amount;
                        string file_name;
                        string hash_value;

                    }

                    Loan []loans;

                    function addLoan(int l_id,string memory username, string memory loan_amount, string memory file_name, string memory hash_value) public
                    {
                        Loan memory e
                            =Loan(l_id,
                                    username,
                                    loan_amount,
                                    file_name,
                                    hash_value);
                        loans.push(e);
                    }

                    function getLoan(int l_id) public view returns(
                           
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<loans.length;i++)
                        {
                            Loan memory e
                                =loans[i];
                            
                            if(e.l_id==l_id)
                            {
                                return(e.username,
                                    e.loan_amount,
                                    e.file_name,
                                    e.hash_value
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found"
                               );
                    }

                    function getLoanCount() public view returns(uint256)
                    {
                        return(loans.length);
                    }

                    struct Transaction
                    {
                        int t_id;
                        string title;
                        string sender_name;
                        string receiver_name;
                        string sender_p_address;
                        string receiver_p_address;
                        string amount;
                        string t_hash;
                    }
                    Transaction []transactions;

                    function addTransaction(int t_id,string memory title,string memory sender_name,string memory receiver_name,string memory sender_p_address,string memory receiver_p_address,string memory amount,string memory t_hash)public
                    {
                        Transaction memory t=Transaction(t_id,
                                                        title,
                                                        sender_name,
                                                        receiver_name,
                                                        sender_p_address,
                                                        receiver_p_address,
                                                        amount,
                                                        t_hash);
                        transactions.push(t);
                    }

                    function getTransaction(int t_id) public view returns(string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory)
                    {
                        uint j;
                        for(j=0;j<transactions.length;j++)
                        {
                            Transaction memory t=transactions[j];

                            if(t.t_id==t_id)
                            {
                                return(t.title,
                                        t.sender_name,
                                        t.receiver_name,
                                        t.sender_p_address,
                                        t.receiver_p_address,
                                        t.amount,
                                        t.t_hash);
                            }

                        }

                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found");
                    }
                    function getTransactionsCount() public view returns(uint256)
                    {
                        return(transactions.length);
                    }


                }

               '''
         }
     },
     "settings":
         {
             "outputSelection": {
                 "*": {
                     "*": [
                         "metadata", "evm.bytecode"
                         , "evm.bytecode.sourceMap"
                     ]
                 }
             }
         }
 })


# web3.py instance



def verify_key(adr1,key,amount):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr1,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(amount, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        #print(web3.toHex(tx_hash))
        return "Yes"
    except Exception as e:
        print(e)  
        return "No"  



def create_contract():
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # get bytecode
    bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    pb = w3.eth.contract(abi=abi, bytecode=bytecode)

    # # Submit the transaction that deploys the contract
    tx_hash = pb.constructor().transact()

    # # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print("tx_receipt.contractAddress: ",tx_receipt.contractAddress)
    f=open('contract_address.txt','w')
    f.write(tx_receipt.contractAddress)
    f.close()


def add_bank1(user_id,username,password,mobile,p_address):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    tx_hash = p1.functions.addBank(user_id,username,password,mobile,p_address).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    #print(tx_hash) 
    print(tx_receipt)

    

def get_bank(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getBank(id1).call()
    print("store : ",store)
    return store

def get_banks():
    c=get_bank_count()
    c_names=['username','password','mobile','p_address']
    dict1={}
    for i in range(1,c+1):
        d=get_bank(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1        

def get_bank_count():
    p1=get_contract()
    store = p1.functions.getBankCount().call()
    print(store)
    return int(store)


def get_company(id1):
    id1=int(id1)
    p1=get_contract()
    print(id1,'============')
    store = p1.functions.getUser(id1).call()
    print(store)
    return store

def get_companies():
    c=get_company_count()
    c_names=['username','password','mobile','p_address']
    dict1={}
    for i in range(1,c+1):
        d=get_company(i)
        dict2={}
        for j in range(len(c_names)):
            # if j==5:
            #     dict2[c_names[j]]=d[7]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1     


def get_company_count():
    p1=get_contract()
    store = p1.functions.getCompanyCount().call()
    print(store)
    return int(store)
    

def add_company1(user_id,username,password,mobile,p_address):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    # c=get_patient_count()+1
    tx_hash = p1.functions.addCompany(user_id,username,password,mobile,p_address).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print(tx_hash)

##############################
def add_loan(loan_id,username,loan_amount,file,hash_value):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']
    p2 = w3.eth.contract(
        address=address,
        abi=abi
    )
    # c=get_patient_count()+1
    tx_hash = p2.functions.addLoan(loan_id,username,loan_amount,file,hash_value).transact()
    #tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print(tx_hash)


def get_loan(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getLoan(id1).call()
    print("store : ",store)
    return store

def get_loans():
    c=get_loan_count()
    c_names=['username','loan_amount','file_name','hash_value']
    dict1={}
    for i in range(1,c+1):
        d=get_loan(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print("File dictionary :::>",dict1)
    return dict1        

def get_loan_count():
    p1=get_contract()
    store = p1.functions.getLoanCount().call()
    print(store)
    return int(store)


def get_contract():
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]#'0x3529A6ee990639C32bEe5F841a9649cdd0c6e0FD'
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    return p1



def verify_adr(s):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    adrs = w3.eth.accounts
    print(adrs)

    if s in adrs:
        return True
    else:
        return False  



def bverify_transaction(tx):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvi
    x=w3.eth.getTransaction(tx)
    print(x)
    if x==None:
        print('Fake')
        return False
    else:
        print('Real')
        return True


###################
def add_transaction_to_table(get_id,title,username,author,sender_public_key,receiver_public_key,price,t_hash):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

    # get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    tx_hash = p1.functions.addTransaction(get_id,title,username,author,sender_public_key,receiver_public_key,price,t_hash).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    #print(tx_hash) 
    print(tx_receipt)

    

def get_transact(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getTransaction(id1).call()
    print("store : ",store)
    return store

def get_transactions():
    c=get_transactionss_count()

    c_names=['title','sender_name','receiver_name','sender_p_address','receiver_p_address','amount','t_hash']
    dict1={}
    for i in range(1,c+1):
        d=get_transact(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1        

def get_transactionss_count():
    p1=get_contract()
    store = p1.functions.getTransactionsCount().call()
    print(store)
    return int(store)



def transfer(adr1,adr2,key,amount,sender_name,receiver_name,title):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr2, #artist_address
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(amount, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        generated_hash=web3.toHex(tx_hash)
        print("generated_hash : ",generated_hash)
        return generated_hash

    except Exception as e:
        print(e)  
        return False



def approval_process(l_id,username,loan_amount,file):
    f_path = 'blk_app/static/temp_files/'+file

    # Read the CSV file using pandas
    data = pd.read_csv(f_path)

    # Extract each column into separate variables
    Day = data['Day'].values[0]
    OEE = data['OEE'].values[0]
    Total_mins_of_Interruption = data['Total mins of Interruption'].values[0]
    Mins_of_Preventive_Maintenance = data['Mins of Preventive Maintenance'].values[0]
    Mins_of_Alarms = data['Mins of Alarms'].values[0]
    Required_Production = data['Required Production'].values[0]
    Actual_Production = data['Actual Production'].values[0]
    Wastes = data['Wastes'].values[0]
    Mins_of_Real_Operation = data['Mins of Real Operation'].values[0]
    Number_of_Breakdowns = data['Number of Breakdowns'].values[0]

    # Define the threshold values for each criterion
    thresholds = {
        'OEE': 0.825,
        'Mins of Preventive Maintenance': 0.582,
        'Mins of Alarms': 0.158,
        'Mins of Real Operation': 0.304,
        'Number of Breakdowns': 6.9,
        'Required Production': 0.253,
        'Actual Production': 0.303
    }

    # Check if the company is eligible for a loan based on the criteria
    eligible_for_loan = (
        OEE >= thresholds['OEE'] and
        Mins_of_Preventive_Maintenance >= thresholds['Mins of Preventive Maintenance'] and
        Mins_of_Alarms <= thresholds['Mins of Alarms'] and
        Mins_of_Real_Operation >= thresholds['Mins of Real Operation'] and
        Number_of_Breakdowns <= thresholds['Number of Breakdowns'] and
        Required_Production >= thresholds['Required Production'] and
        Actual_Production >= thresholds['Actual Production']
    )

    # Print the result
    if eligible_for_loan:
        output_file_path ="blk_app/static/user_files/"+str(username)
        if not os.path.exists(output_file_path):
            os.makedirs(output_file_path)

        files_in_directory = os.listdir(output_file_path)
        csv_files = [file for file in files_in_directory if file.endswith(".csv")]
        print("hai")
        if len(csv_files) > 0:
            print("here")
            csv_file_path = os.path.join(output_file_path, csv_files[0])
            dt1 = pd.read_csv(csv_file_path)

            # Function to check if two values are equal or not
            def check_equal(value1, value2):
                return value1 == value2

            # Comparing the details from the first and second CSV files
            are_details_equal = True

            fields = ['OEE', 'Total mins of Interruption', 'Mins of Preventive Maintenance',
                      'Mins of Alarms', 'Required Production', 'Actual Production', 'Wastes',
                      'Mins of Real Operation', 'Number of Breakdowns']

            for field in fields:
                old_value = dt1[field].values[0]
                new_value = data[field].values[0]

                if not check_equal(old_value, new_value):
                    print(f"{field} is not equal")
                    are_details_equal = False

            # Checking if all details are equal
            if are_details_equal:
                print("All details are equal.")
                res="All details are equal. Loan Rejected"
                hash_value='-'

                if os.path.exists(f_path):
                    os.remove(f_path)

                return res,hash_value

            else:
                print("Details are not equal.")
                print("The company is eligible for a loan.")
                res="The company is eligible for a loan."

                # #file storing to IPFS
                api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
                new_file = api.add("blk_app/static/temp_files/"+str(file))
                print(new_file)
                hash_value=new_file.get('Hash')

                loan_id=int(l_id)
                add_loan(loan_id,username,loan_amount,file,hash_value)

                df = pd.read_csv(f_path)
                final_p="blk_app/static/user_files/"+str(username)+"/"+str(file)
                df.to_csv(final_p, index=False)

                if os.path.exists(csv_file_path):
                    os.remove(csv_file_path)

                if os.path.exists(f_path):
                    os.remove(f_path)

                return res,hash_value
        else:
            print("The company is eligible for a loan.")
            res="The company is eligible for a loan."

            # #file storing to IPFS
            api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
            new_file = api.add("blk_app/static/temp_files/"+str(file))
            print(new_file)
            hash_value=new_file.get('Hash')

            loan_id=int(l_id)
            add_loan(loan_id,username,loan_amount,file,hash_value)

            df = pd.read_csv(f_path)
            final_p="blk_app/static/user_files/"+str(username)+"/"+str(file)
            df.to_csv(final_p, index=False)

            if os.path.exists(f_path):
                os.remove(f_path)

            return res,hash_value

    else:
        print("Sorry, the company does not meet the criteria for a loan.")
        res="Sorry, the company does not meet the criteria for a loan."
        hash_value='-'

        if os.path.exists(f_path):
            os.remove(f_path)

        return res,hash_value

    # return res,hash_value



if __name__=="__main__":
    pass

    #create_contract()




