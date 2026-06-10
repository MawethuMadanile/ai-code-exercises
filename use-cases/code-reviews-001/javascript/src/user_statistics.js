function calculateAverage(data, field) {
    return data.reduce((sum, item) => sum + item[field], 0) / data.length;
}

function calculateHighest(data, field) {
    return data.reduce((max, item) => item[field] > max ? item[field] : max, data[0][field]);
}

function calculateUserStatistics(userData) {
    const fields = ['age', 'income', 'score'];
    return fields.reduce((stats, field) => {
        stats[field] = {
            average: calculateAverage(userData, field),
            highest: calculateHighest(userData, field)
        };
        return stats;
    }, {});
}