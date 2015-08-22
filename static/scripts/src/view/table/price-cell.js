

define([
    'backgrid',
    'view/parser/price'
], function (Backgrid, priceParser) {

    return Backgrid.NumberCell.extend({

        render: function () {
            Backgrid.NumberCell.prototype.render.apply(this, arguments);

            this.$el
                .html(priceParser(this.$el.text()))
                .addClass(this.column.get('name'));

            return this;
        }

    });

});