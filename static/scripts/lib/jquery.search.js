

define(['jquery'], function ($) {

    $.fn.search = function (selector) {
        return this
            .filter(selector)
            .add(this.find(selector));
    }

    return $;

});