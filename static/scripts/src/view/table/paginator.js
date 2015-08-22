

define([
    'backbone',
    'backgrid',
    'backbone.backgrid.paginator'
], function (Backbone, Backgrid) {

    return Backgrid.Extension.Paginator.extend({

        render: function () {
            Backgrid.Extension.Paginator.prototype.render.apply(
                this, arguments);

            this.$('ul').addClass('pagination');

            return this;
        }

    });

});