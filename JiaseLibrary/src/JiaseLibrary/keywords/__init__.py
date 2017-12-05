import os
import sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(CURRENT_DIR)
from _lambdasysauth import _LambdaSysAuthKeywords
from _lambdasysorganize import _LambdaSysOrganizeKeywords
from _lambdasysuser import _LambdaSysUserKeywords
from _lambdacustomer import _LambdaCustomerKeywords
from _lambdaloan import _LambdaLoanKeywords
from _lambdacontract  import _LambdaContractKeywords 
from _lambdawithdrawal import _LambdaWithdrawalKeywords
from _lambdarepayment import _LambdaRepaymentKeywords

__all__ = [
    "_LambdaSysAuthKeywords",
    "_LambdaSysOrganizeKeywords",
    "_LambdaSysUserKeywords",
    "_LambdaCustomerKeywords",
    "_LambdaLoanKeywords",
    "_LambdaContractKeywords",
    "_LambdaWithdrawalKeywords",
    "_LambdaRepaymentKeywords"
]
