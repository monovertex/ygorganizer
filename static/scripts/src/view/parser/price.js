

define(['underscore'], function (_) {

    return function (source, decimals) {
        var result = source;

        if (result) {
            result = parseFloat(String(result).replace(/,/g, ''));

            if (!_.isUndefined(decimals) && _.isNumber(decimals)) {
                result = Number(result.toFixed(decimals));
            }

            result = '$' + result;
        } else {
            result = 'N/A';
        }

        return result;
    };

});