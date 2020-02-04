from itertools import groupby
import collections, functools, operator
from operator import itemgetter
from datetime import datetime

class TaxCalculator:
    @staticmethod
    def calculate_tax(financial_operations):
        financial_operations.sort_values(inplace=True, kind='mergesort')
        grouped = [list(g) for k, g in groupby(financial_operations, lambda paper: paper.asset_name)]
        
        # Profit_loss is an array of array, because each paper has an array of profit loss by month
        profit_loss = [TaxCalculator.calculate_p_l(paper) for paper in grouped]
        
        # Merge to an unique array
        merged_p_l = []
        for l in profit_loss:
            merged_p_l += l

        # sort by year and month
        sort = sorted(merged_p_l, key = lambda i: i['date'].year * 100 + i['date'].month)

        # group by year and month
        profit_loss = [list(g) for k, g in groupby(sort, lambda p_l: p_l['date'].year * 100 + p_l['date'].month)]
        # print(profit_loss)

        # Calculate the amount of profit loss and sell by month
        by_month = []

        for pl_per_month in profit_loss:
            total_p_l = sum(pl['p_l'] for pl in pl_per_month)
            total_sell = sum(sell['sell'] for sell in pl_per_month)
            by_month.append({'total': total_p_l, 'date': pl_per_month[0]['date'], 'sell': total_sell})
        
        # Mostrar resumo das operacoes no mes
        # print(by_month)
        # [{'total': 0, 'date': datetime.datetime(2019, 7, 31, 0, 0), 'sell': 0}, {'total': 0, 'date': datetime.datetime(2019, 8, 15, 0, 0), 'sell': 0}, {'total': 0, 'date': datetime.datetime(2019, 9, 12, 0, 0), 'sell': 0}, {'total': 80788.97169811321, 'date': datetime.datetime(2020, 1, 18, 0, 0), 'sell': 202000.0}]
        # mostrar mes mapeado em cada objeto
        # print(by_month[0]["date"].strftime("%B"))
        for i in range(0,len(by_month)):
            if (by_month[i]["sell"] >= 20001):
                by_month[i]["tax"] = by_month[i]["total"] * 0.15
            else:
                by_month[i]["tax"] = 0
        
        # print(str(total_p_l))
        # print(total_sell)
        # print(str(profit_loss))
        print (by_month)
        return by_month

    # calculate profit and loss on a set of paper, operated in a range of time
    @staticmethod
    def calculate_p_l(paper):
        paper_average = {'asset_name': paper[0].asset_name, 'quantity':0, 'total_price':0,'average':0}
        reference_month = paper[0].date
        profit_loss = [{'p_l':0,'sell':0, 'date': reference_month}]
        month_index = 0
        # print operation by paper
        # print(reference_month)
        for operation in paper:
            if reference_month.year != operation.date.year or operation.date.month != reference_month.month:
                reference_month = operation.date
            # calculate average on every buy
            if operation.op_type == "C":
                
                # sum all quantity, total_price and calculate the average from every operation of each paper
                paper_average["quantity"] += operation.quantity
                paper_average["total_price"] += operation.total_price()
                paper_average["average"] = paper_average["total_price"]/paper_average["quantity"]
            elif operation.op_type == "V":

                # sum all profit_loss, sell and subtract the quantity
                if profit_loss[month_index]['date'] != reference_month:
                    month_index += 1
                    profit_loss.append({'p_l':0,'sell':0, 'date':0})

                profit_loss[month_index]['date'] = reference_month
                profit_loss[month_index]['p_l'] += (operation.total_price() - (paper_average["average"] * operation.quantity))
                profit_loss[month_index]['sell'] += operation.total_price()
                paper_average["quantity"] -= operation.quantity
                paper_average["total_price"] = paper_average["quantity"] * paper_average["average"]
        print(paper_average)
        return profit_loss

    @staticmethod
    def filter_and_sum(asset_financial_operations, search_filter='C'):
        operations = filter(lambda fo: fo.op_type == search_filter, asset_financial_operations)
        summary = {"price": sum(op.total_price() for op in operations),
                   "total_quantity": sum(op.quantity for op in operations)}
        return summary
