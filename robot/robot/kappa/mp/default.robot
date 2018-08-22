*** Settings ***
Documentation   Kappa-mp 常规测试
Resource        ../../lib/kappa/mp.robot
Resource        ../../lib/lambda/lambda.robot
Suite Setup     生成随机用户信息

*** Variables ***
${KAPPA_MP_BACKEND_HOST}                10.1.60.114
${KAPPA_MP_BACKEND_PORT}                8081
${LAMBDA_SERVER_HOST}                   10.1.60.114
${LAMBDA_SERVER_PORT}                   8080
${LAMBDA_DB_HOST}                       10.1.60.114
${MESSAGE}       Hello, world!

${INVEST_MANAGER_USER}     18697989859
${INVEST_MANAGER_NAME}     胡云祥
${uid}       18700000004
${uname}     展期geren54
*** Test Cases ***
用户注册
   用户注册

开通存管账户
    开通借款人存管账户       ${uid}
    开通担保方存管账户       ${uid}

移交给投资经理
    用户变更投资经理    ${uname}     admin   ${INVEST_MANAGER_NAME}

完善用户信息
    完善基本用户信息  ${uname}    ${INVEST_MANAGER_USER}

新增授信

testB
    login_lambda        	\   18600000001     ${DEFAULT_PASS_WORD}
    cust_infos_id_personal_view     29

testC
    login_lambda        	\   13570927312     150315
    创建初始的信贷产品

testD
    login_lambda        	\   ${INVEST_MANAGER_USER}     ${DEFAULT_PASS_WORD}
    # 新增授信
    #loan_apply_create   33287
    # 生成授信明细
    # loan_apply_prepare_create   14665
    # 保存自贷额度信息
    loan_detail_self_save     14665     21098   种植贷     self_limit=100000




*** Keywords ***






