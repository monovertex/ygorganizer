

define([
    'backgrid',
    'bootstrap'
], function (Backgrid) {

    return function (root, idAttribute) {
        return Backgrid.UriCell.extend({

            target: '',

            title: 'View card information',

            render: function () {
                Backgrid.UriCell.prototype.render.apply(this, arguments);

                this.$('a')
                    .attr('href', root + this.model.get(idAttribute) + '/')
                    .addClass('follow');

                return this;
            }

        });
    };

});