

define(['underscore', 'jquery'], function (_, $) {

    return function (source, decimals) {
        var result = source,
            $htmlResult = $('<span></span>');

        if (result) {
            result = parseFloat(result);

            if (result > 0) {
                $htmlResult.addClass('text-success');
            } else if (result < 0) {
                $htmlResult.addClass('text-danger');
            }

            if (!_.isUndefined(decimals) && _.isNumber(decimals)) {
                result = Number(result.toFixed(decimals));
            }

            result = result + '%';
            $htmlResult.text(result);
        }

        return $htmlResult;
    };

});