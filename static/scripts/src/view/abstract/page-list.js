

define([
    'jquery',
    'underscore',
    'backbone',
    'view/component/card',
    'view/table/grid',
    'backgrid',
    'templates',
    'view/parser/price',
    'view/parser/price-shift'
], function ($, _, Backbone, CardView, GridView, Backgrid, Templates,
        priceParser, priceShiftParser) {

    var Row = Backgrid.Row.extend({

            render: function () {
                var result = Backgrid.Row.prototype.render.apply(this, arguments);

                $('.popover:visible').remove();

                if (this.model.get('card.image_small_tag')) {
                    this.$el
                        .popover({
                            animation: false,
                            container: 'body',
                            html: true,
                            content: this.model.get('card.image_small_tag'),
                            title: '',
                            placement: 'auto top',
                            trigger: 'manual'
                        });
                }

                return result;
            }

        });

    return Backbone.View.extend({

        template: Templates['page-list'],

        events: {
            'mousemove': 'mousemove',
            'click .toggle-statistics': 'toggleStatistics'
        },

        previewOffset: 40,

        statisticColumns: [
            'count', 'price_shift', 'price_low', 'price_avg', 'price_high'
        ],

        statisticWidths: [
            'price_shift', 'price_low', 'price_avg', 'price_high'
        ],

        statisticParsers: {
            'price_shift': [priceShiftParser, 2],
            'price_low': [priceParser, 2],
            'price_avg': [priceParser, 2],
            'price_high': [priceParser, 2],
        },

        initialize: function () {
            _.bindAll(this);

            if (_.isUndefined(this.collection)) {
                throw 'Source collection is undefined';
            }

            this.$el.html(this.template());

            this.card = new CardView({
                el: this.$('.card-wrapper'),
                rootUrl: this.rootUrl
            });

            this.grid = new GridView({
                el: this.$('.table-wrapper'),
                columns: this.gridColumns,
                collection: this.collection,
                row: Row
            });

            this.$statistics = this.$('.statistics');
            this.$statisticCells = { subtotal: {}, total: {} };

            _.each(this.statisticColumns, function (column) {
                var actualColumn = column.replace(/_/g, '-');

                this.$statisticCells.subtotal[column] =
                    this.$statistics.find('.statistics-subtotal-' + actualColumn);
                this.$statisticCells.total[column] =
                    this.$statistics.find('.statistics-total-' + actualColumn);
            }, this);

            this.listenTo(this.grid.collection, 'change add remove reset',
                this.collectionChange);
            this.listenTo(this.grid.collection, 'fetched', this.showMessages);

            this.$noResults = this.$('.no-results');
            this.$emptyCollection = this.$('.empty-collection');

            this.collection.fetch().done(this.showMessages());
        },

        collectionChange: function () {
            this.hidePopovers.apply(this, arguments);

            if (this.updateStatisticsInterval) {
                clearTimeout(this.updateStatisticsInterval);
                delete this.updateStatisticsInterval;
            }

            this.updateStatisticsInterval = setTimeout(this.updateStatistics, 50);

            this.showMessages();
        },

        showMessages: function (statistics) {
            this.$emptyCollection.addClass('no-display');
            this.$noResults.addClass('no-display');

            if (statistics) {
                if (statistics.total_count === 0) {
                    this.$emptyCollection.removeClass('no-display');
                } else if (statistics.total_entries === 0) {
                    this.$noResults.removeClass('no-display');
                }
            }
        },

        hidePopovers: function ($exclude) {
            var $popovers = $('.popover:visible');

            if ($exclude) {
                $popovers = $popovers.not($exclude);
            }

            $popovers.hide();
        },

        toggleStatistics: function () {
            this.$statistics.toggle();
            this.grid.resize();
        },

        updateStatistics: function () {
            _.each(this.statisticWidths, function (column) {
                var width = this.grid.grid.$('.' + column).outerWidth();

                this.$statisticCells.subtotal[column].width(width);
                this.$statisticCells.total[column].width(width);
            }, this);

            _.each(this.collection.statistics, function (data, key) {
                var keys = key.split(/_(.+)?/),
                    parsed = data,
                    parserData,
                    parser;

                try {
                    parserData = _.clone(this.statisticParsers[keys[1]]);
                    parser = parserData[0];
                    parserData.splice(0, 1, data);

                    parsed = parser.apply(this, parserData);
                } catch (ignore) {}

                try {
                    this.$statisticCells[keys[0]][keys[1]].html(parsed);
                } catch (ignore) {}
            }, this);
        },

        mousemove: function (ev) {
            var $tr = $(ev.target).parents('tbody tr'),
                $popover;

            if ($tr.length && $tr.data('bs.popover')) {
                $popover = $tr.data('bs.popover').$tip;

                if (!$popover || !$popover.is('visible')) {
                    $tr.popover('show');
                }

                if ($popover) {
                    $popover.css('left', ev.pageX + this.previewOffset);
                }

                this.hidePopovers($popover);
            } else {
                this.hidePopovers();
            }
        },

        render: function (identifier) {
            if (identifier) {
                this.card.render(identifier);
            } else {
                this.card.hide();
            }

            return this;
        }

    });

});