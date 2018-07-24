import re
s = '+1-503-555-00910'
if re.match(r'^\+1-\d{3}-\d{3}-\d{4}$',s,flags=0):
    print(s)
log.info("遍历流水开始-->"+matchDetailListBean.getFlowIds().toString());



        for (Integer flowid:cover(matchDetailListBean.getFlowIds())) {
            //查出流水
            MatchFlow mf = matchFlowService.selectByPrimaryKey(flowid);
            //初始化第一条流水
            flowamt = BigDecimalUtils.lessEqZero(flowamt) ? mf.getRemainAmt() : flowamt;
            //遍历实还额
            for (MatchDetailBean mdb:matchDetailListBean.getListMdb()) {
                log.info("遍历借据开始-->"+mdb.getLendCode());
                if (BigDecimalUtils.lessEqZero(iouamt) || BigDecimalUtils.lessEqZero(mdb.getIouTemp())){
                    break;
                }
                if(receivedFundDate == null){
                    receivedFundDate = mdb.getReceivedFundDate();
                }
                if(receivedFundDate == null){
                    MatchFlow mff = matchFlowService.selectByPrimaryKey(flowid);
                    receivedFundDate = mff.getTradingDay();
                }
                // 查询借据详情
                IouInfo iouInfo = matchKeysService.selectIouInfo(mdb.getLendCode());

                //去查询借据的情况开始
                RepaymentQueryBean query = new RepaymentQueryBean();
                query.setCustId(iouInfo.getCustId());
                query.setLendCode(mdb.getLendCode());
                query.setCustKind(RepaymentExemptCustTypeEnum.JKF.getCode());
                query.setReceivedFundDate(DateTimeUtils.truncateDateYMD(receivedFundDate));
                RepaymentDueResultBean rdrb= repaymentQueryGatewayService.getRepayDueResult(query);
                if (flowamt.compareTo(mdb.getIouTemp()) == 1){
                    mdb.setIouTemp(BigDecimal.ZERO);
                    totalamt = BigDecimalUtils.add(totalamt,mdb.getIouTemp());
                    totalcount++;
                    mdb.setMatchStatus(MatchStatusEnums.INIT.getCode());
                    mdb.setRefundAmt(new BigDecimal("0"));
                    mdb.setOperationId(mor.getId());
                    mdb.setFlowId(flowid);
                    mdb.setLendStatus(iouInfo.getIouStatus());
                    mdb.setCustId(iouInfo.getCustId());
                    mdb.setCustName(iouInfo.getCustName());
                    mdb.setIssue(rdrb.getIssue());
                    mdb.setLendPeriod(rdrb.getLendPeriod());
                    mdb.setDueDate(rdrb.getDueDate());
                    mdb.setLendAmt(iouInfo.getIouAmt());
                    mdb.setDueCapital(rdrb.getDueCapital());
                    mdb.setDueInterest(rdrb.getDueInterest());
                    mdb.setDueMngtCharge(rdrb.getDueMngtCharge());
                    mdb.setDuePenalty(rdrb.getDuePenalty());
                    mdb.setRepayTotalAmt(rdrb.getDueRepayAmt());
                    mdb.setRepayOrder(RepayOrderEnums.ORD3.getCode());
                    mdb.setMatchAmt(mdb.getMatchAmt());
                    matchDetailService.insertMatchDetail(mdb);
                    matchFlowOperationService.matchAmt(mdb.getFlowId(),mdb.getMatchAmt());

                    //削减流水
                    flowamt = flowamt.subtract(mdb.getIouTemp());
                }else if (flowamt.compareTo(mdb.getIouTemp()) == -1 || flowamt.compareTo(mdb.getIouTemp()) == 0){
                    mdb.setIouTemp(mdb.getIouTemp().subtract(flowamt));
                    iouamt = mdb.getMatchAmt().subtract(flowamt);
                    totalamt = BigDecimalUtils.add(totalamt,flowamt);
                    totalcount++;
                    mdb.setMatchStatus(MatchStatusEnums.INIT.getCode());
                    mdb.setRefundAmt(new BigDecimal("0"));
                    mdb.setOperationId(mor.getId());
                    mdb.setMatchAmt(flowamt);
                    mdb.setFlowId(flowid);
                    mdb.setLendStatus(iouInfo.getIouStatus());
                    mdb.setCustId(iouInfo.getCustId());
                    mdb.setCustName(iouInfo.getCustName());
                    mdb.setIssue(rdrb.getIssue());
                    mdb.setLendPeriod(rdrb.getLendPeriod());
                    mdb.setDueDate(rdrb.getDueDate());
                    mdb.setLendAmt(iouInfo.getIouAmt());
                    mdb.setDueCapital(rdrb.getDueCapital());
                    mdb.setDueInterest(rdrb.getDueInterest());
                    mdb.setDueMngtCharge(rdrb.getDueMngtCharge());
                    mdb.setDuePenalty(rdrb.getDuePenalty());
                    mdb.setRepayTotalAmt(rdrb.getDueRepayAmt());
                    mdb.setRepayOrder(RepayOrderEnums.ORD3.getCode());
                    matchDetailService.insertMatchDetail(mdb);
                    matchFlowOperationService.matchAmt(mdb.getFlowId(),flowamt);
                    //削减流水至0
                    flowamt = new BigDecimal(0);
                    break;
                }

            }
        }