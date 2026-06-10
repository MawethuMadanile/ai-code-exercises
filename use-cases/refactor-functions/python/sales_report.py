def validate_inputs(sales_data, report_type, output_format):
    if not sales_data or not isinstance(sales_data, list):
        raise ValueError("Sales data must be a non-empty list")
    if report_type not in ['summary', 'detailed', 'forecast']:
        raise ValueError("Report type must be 'summary', 'detailed', or 'forecast'")
    if output_format not in ['pdf', 'excel', 'html', 'json']:
        raise ValueError("Output format must be 'pdf', 'excel', 'html', or 'json'")


def filter_by_date_range(sales_data, date_range):
    if not date_range:
        return sales_data
    start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
    end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")
    return [s for s in sales_data if start_date <= datetime.strptime(s['date'], '%Y-%m-%d') <= end_date]


def apply_filters(sales_data, filters):
    if not filters:
        return sales_data
    for key, value in filters.items():
        if isinstance(value, list):
            sales_data = [s for s in sales_data if s.get(key) in value]
        else:
            sales_data = [s for s in sales_data if s.get(key) == value]
    return sales_data


def calculate_metrics(sales_data):
    total_sales = sum(s['amount'] for s in sales_data)
    return {
        'total_sales': total_sales,
        'transaction_count': len(sales_data),
        'average_sale': total_sales / len(sales_data),
        'max_sale': max(sales_data, key=lambda x: x['amount']),
        'min_sale': min(sales_data, key=lambda x: x['amount'])
    }


def group_data(sales_data, grouping, total_sales):
    if not grouping:
        return None
    grouped = {}
    for sale in sales_data:
        key = sale.get(grouping, 'Unknown')
        if key not in grouped:
            grouped[key] = {'count': 0, 'total': 0}
        grouped[key]['count'] += 1
        grouped[key]['total'] += sale['amount']
    for key in grouped:
        grouped[key]['average'] = grouped[key]['total'] / grouped[key]['count']
        grouped[key]['percentage'] = (grouped[key]['total'] / total_sales) * 100
    return grouped


def build_transactions(sales_data):
    transactions = []
    for sale in sales_data:
        t = dict(sale)
        if 'tax' in sale:
            t['pre_tax'] = sale['amount'] - sale['tax']
        if 'cost' in sale:
            t['profit'] = sale['amount'] - sale['cost']
            t['margin'] = (t['profit'] / sale['amount']) * 100
        transactions.append(t)
    return transactions


def build_forecast(sales_data):
    monthly_sales = {}
    for sale in sales_data:
        month_key = datetime.strptime(sale['date'], '%Y-%m-%d').strftime('%Y-%m')
        monthly_sales[month_key] = monthly_sales.get(month_key, 0) + sale['amount']

    sorted_months = sorted(monthly_sales)
    growth_rates = [
        ((monthly_sales[sorted_months[i]] - monthly_sales[sorted_months[i-1]])
         / monthly_sales[sorted_months[i-1]]) * 100
        for i in range(1, len(sorted_months))
        if monthly_sales[sorted_months[i-1]] > 0
    ]
    avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0

    forecast = {}
    if sorted_months:
        year, month = map(int, sorted_months[-1].split('-'))
        amount = monthly_sales[sorted_months[-1]]
        for _ in range(3):
            month += 1
            if month > 12:
                month, year = 1, year + 1
            amount *= (1 + avg_growth / 100)
            forecast[f"{year}-{month:02d}"] = amount

    return {'monthly_sales': monthly_sales, 'average_growth_rate': avg_growth, 'projected_sales': forecast}


def build_charts(sales_data, grouping, grouped_data):
    date_sales = {}
    for sale in sales_data:
        date_sales[sale['date']] = date_sales.get(sale['date'], 0) + sale['amount']

    charts = {'sales_over_time': {
        'labels': sorted(date_sales),
        'data': [date_sales[d] for d in sorted(date_sales)]
    }}
    if grouping and grouped_data:
        charts[f'sales_by_{grouping}'] = {
            'labels': list(grouped_data),
            'data': [grouped_data[k]['total'] for k in grouped_data]
        }
    return charts


def generate_sales_report(sales_data, report_type='summary', date_range=None,
                          filters=None, grouping=None, include_charts=False,
                          output_format='pdf'):
    validate_inputs(sales_data, report_type, output_format)

    sales_data = filter_by_date_range(sales_data, date_range)
    sales_data = apply_filters(sales_data, filters)

    if not sales_data:
        return {"message": "No data matches the specified criteria", "data": []} \
            if output_format == 'json' else _generate_empty_report(report_type, output_format)

    metrics = calculate_metrics(sales_data)
    grouped_data = group_data(sales_data, grouping, metrics['total_sales'])

    report = {
        'report_type': report_type,
        'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': date_range,
        'filters': filters,
        'summary': metrics
    }

    if grouped_data:
        report['grouping'] = {'by': grouping, 'groups': grouped_data}
    if report_type == 'detailed':
        report['transactions'] = build_transactions(sales_data)
    if report_type == 'forecast':
        report['forecast'] = build_forecast(sales_data)
    if include_charts:
        report['charts'] = build_charts(sales_data, grouping, grouped_data)

    formatters = {
        'json': lambda r: r,
        'html': _generate_html_report,
        'excel': _generate_excel_report,
        'pdf': _generate_pdf_report
    }
    return formatters[output_format](report) if output_format != 'json' else report