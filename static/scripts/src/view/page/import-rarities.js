

define([
    'backbone',
    'jquery',
    'nouislider'
], function (Backbone, $) {

    return Backbone.View.extend({

        initialize: function () {
            $('input.rarity-input').each(function () {
                var $input = $(this),
                    $slider = $input.siblings('.rarity-slider'),
                    $display = $input.siblings('.rarity-slider-display');

                $slider.noUiSlider({
                    start: [0],
                    step: 1,
                    range: {
                        min: [0],
                        max: [parseInt($input.data('max'), 10)]
                    },
                    format: {
                        to: function (value) {
                            return parseInt(value, 10);
                        },
                        from: function (value) {
                            return parseFloat(value);
                        }
                    }
                });
                $slider.Link('lower').to($input);
                $slider.Link('lower').to($display);
            });
        },

    });

});