

define([
    'backgrid',
    'view/parser/price-shift'
], function (Backgrid, priceShiftParser) {

    return Backgrid.PercentCell.extend({

        multiplier: 100,

        render: function () {
            Backgrid.PercentCell.prototype.render.apply(this, arguments);

            // var value = parseFloat(this.$el.text());

            // if (value > 0) {
            //     this.$el
            //         .removeClass('text-danger').addClass('text-success')
            //         .text('+' + this.$el.text());
            // } else if (value < 0) {
            //     this.$el.removeClass('text-success').addClass('text-danger');
            // }

            this.$el
                .html(priceShiftParser(this.$el.text()))
                .addClass(this.column.get('name'));

            return this;
        }

    });

});