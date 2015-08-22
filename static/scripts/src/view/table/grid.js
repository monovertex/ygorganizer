

define([
    'jquery',
    'backbone',
    'underscore',
    'templates',
    'backgrid',
    'view/table/paginator',
    'backbone.backgrid.filter'
], function ($, Backbone, _, Templates, Backgrid, Paginator) {

    return Backbone.View.extend({

        template: Templates.table,

        rowHeight: 44,

        initialize: function (options) {
            _.bindAll(this);

            this.$el.html(this.template());

            this.collection = options.collection;

            this.grid = new Backgrid.Grid({
                row: options.row || Backgrid.Row,
                columns: options.columns,
                collection: options.collection
            });
            this.grid.render();

            this.paginator = new Paginator({
                collection: options.collection,
            });
            this.paginator.render();

            this.filter = new Backgrid.Extension.ServerSideFilter({
                collection: options.collection,
                fields: options.filterFields
            });
            this.filter.render();

            this.$('.table-container').prepend(this.grid.$el);
            this.$('.table-filter').append(this.filter.$el);
            this.$('.table-paginator').append(this.paginator.$el);

            this.resize();
            $(window).resize(this.prepareResize);
        },

        prepareResize: function () {
            if (this.resizeDelay) {
                window.clearTimeout(this.resizeDelay);
                delete this.resizeDelay;
            }

            this.resizeDelay = window.setTimeout(this.resize, 300);
        },

        resize: function () {
            var headerHeight = this.$('thead').outerHeight(),
                $tableContainer = this.$('.table-container'),
                height = $tableContainer.outerHeight() - headerHeight,
                rowCount = Math.floor(height / this.rowHeight);

            this.collection.state.pageSize = rowCount;
            this.collection.getPage(0);
        }

    });

});